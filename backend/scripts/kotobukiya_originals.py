"""Collect original image bytes into a staging bundle; apply separately. No resets."""

import argparse
import hashlib
import json
import re
import shutil
import struct
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

BASE = "https://www.kotobukiya.co.jp"


def emit(**data):
    print(json.dumps(data, ensure_ascii=False), flush=True)


def save_json(path, obj):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def image_info(raw):
    if raw.startswith(b"\x89PNG\r\n\x1a\n") and len(raw) >= 24:
        w, h = struct.unpack(">II", raw[16:24])
        return "png", w, h
    if raw.startswith(b"\xff\xd8"):
        i = 2
        while i + 4 <= len(raw):
            if raw[i] != 255:
                raise ValueError("INVALID_JPEG")
            while i < len(raw) and raw[i] == 255:
                i += 1
            marker = raw[i]
            i += 1
            if marker in (216, 217) or 208 <= marker <= 215:
                continue
            length = int.from_bytes(raw[i : i + 2], "big")
            if length < 2:
                break
            if marker in (
                192,
                193,
                194,
                195,
                197,
                198,
                199,
                201,
                202,
                203,
                205,
                206,
                207,
            ):
                h, w = struct.unpack(">HH", raw[i + 3 : i + 7])
                return "jpg", w, h
            i += length
    raise ValueError("UNSUPPORTED_OR_INVALID_IMAGE")


def original_candidates(html, page, sku):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main") or soup
    result = {}
    # Require an actual product code in the image folder; omit unrelated recommendations.
    if not sku:
        raise ValueError("SKU_REQUIRED_FOR_IMAGE_ISOLATION")
    for tag in main.find_all(["a", "img", "source"]):
        for attr in ("href", "data-zoom-image", "data-original", "data-src", "src"):
            val = tag.get(attr)
            if not val:
                continue
            absolute = urljoin(page, val)
            p = urlparse(absolute)
            if p.hostname != "www.kotobukiya.co.jp" or p.scheme != "https":
                continue
            if not re.search(
                r"(?<![A-Za-z0-9])" + re.escape(sku) + r"(?![A-Za-z0-9])", p.path, re.I
            ):
                continue
            # _ is a delimiter in manufacturer image folder names.
            if p.path.startswith("/sm_files_thumbnail/"):
                m = re.fullmatch(
                    r"/sm_files_thumbnail/(.+\.(?:jpg|jpeg|png))/\d+\.(?:jpg|png)",
                    p.path,
                    re.I,
                )
                if not m:
                    continue
                target = BASE + "/sm_files/" + m[1]
                result.setdefault(
                    target,
                    {
                        "source_url": target,
                        "discovered_url": absolute,
                        "selection": "original_path_candidate_verified_by_download",
                    },
                )
            elif p.path.startswith("/sm_files/") and re.search(
                r"\.(jpg|jpeg|png)$", p.path, re.I
            ):
                result[absolute] = {
                    "source_url": absolute,
                    "discovered_url": absolute,
                    "selection": "page_original_link",
                }
    return list(result.values())


def download(fetcher, candidate, folder, cap_mb):
    import httpx

    url = candidate["source_url"]
    host, rule = fetcher.validate(url)
    fetcher.check_robots(url, host)
    fetcher._pace(host, rule)
    with httpx.Client(
        timeout=40, follow_redirects=False, headers={"User-Agent": fetcher.s.user_agent}
    ) as c:
        with c.stream("GET", url) as r:
            r.raise_for_status()
            if r.is_redirect:
                raise ValueError("IMAGE_REDIRECT_REVIEW")
            data = bytearray()
            for part in r.iter_bytes():
                data.extend(part)
                if len(data) > cap_mb * 1024 * 1024:
                    raise ValueError("IMAGE_SIZE_LIMIT_NO_RESIZE")
    raw = bytes(data)
    ext, w, h = image_info(raw)
    if min(w, h) < 1:
        raise ValueError("INVALID_DIMENSIONS")
    digest = hashlib.sha256(raw).hexdigest()
    name = digest + "." + ext
    dest = folder / name
    if not dest.exists():
        tmp = dest.with_suffix(".part")
        tmp.write_bytes(raw)
        tmp.replace(dest)
    return dict(
        candidate,
        file="media/" + name,
        sha256=digest,
        bytes=len(raw),
        width=w,
        height=h,
        transformed=False,
    )


def collect(args, root):
    from app.collectors.safe_http import SafeFetcher, CollectionDenied
    from app.collectors.manufacturers.kotobukiya import Adapter
    from app.models.entities import now
    from bs4 import BeautifulSoup

    fetcher = SafeFetcher()
    fetcher.policy["www.kotobukiya.co.jp"] = dict(
        enabled=True, paths=["/product/detail/", "/sm_files/"], delay_seconds=3
    )
    urls = []
    for line in Path(args.input).read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        url = row["official_url"]
        if (
            re.fullmatch(r"https://www\.kotobukiya\.co\.jp/product/detail/p\d+/", url)
            and url not in urls
        ):
            urls.append(url)
    done = 0
    for url in urls:
        path = root / "products" / (url.rstrip("/").split("/")[-1] + ".json")
        if path.exists() and not args.retry:
            old = json.loads(path.read_text())
            if old.get("status") == "ready" and all(
                (root / im["file"]).is_file() for im in old["images"]
            ):
                continue
        if done >= args.limit:
            break
        record = dict(official_url=url, status="failed", images=[], image_failures=[])
        try:
            html, final = fetcher.fetch_page(url)
            if final.rstrip("/") != url.rstrip("/"):
                raise ValueError("DETAIL_REDIRECT_REVIEW")
            if re.search(
                r"Waiting Room|Request Rejected|challenge-platform", html, re.I
            ):
                raise CollectionDenied("CHALLENGE_OR_WAITING_ROOM")
            soup = BeautifulSoup(html, "html.parser")
            main = soup.find("main") or soup
            if (
                not main.find("a", href=re.compile(r"^/(?:en/)?product/figures/"))
                and "フィギュア" not in main.get_text()
            ):
                raise ValueError("FIGURE_CATEGORY_UNCONFIRMED")
            row = Adapter().parse(html, url)
            fields = row.get("specifications", {})
            maker = fields.get("メーカー")
            if maker and not re.search(r"コトブキヤ|壽屋|KOTOBUKIYA", maker, re.I):
                raise ValueError("OTHER_MANUFACTURER")
            sku = fields.get("品番", "").strip()
            if not re.fullmatch(r"[A-Za-z]{1,8}\d{2,8}", sku):
                raise ValueError("PRODUCT_CODE_REVIEW")
            row["sku"] = sku
            # Do not use prices from navigation blogs or related products.
            text = main.get_text(" ", strip=True)
            prices = set(re.findall(r"([\d,]+)円\s*[（(]税込[）)]", text))
            if len(prices) != 1:
                raise ValueError("PRICE_MISSING_OR_AMBIGUOUS")
            row.update(
                price_amount=int(next(iter(prices)).replace(",", "")),
                currency="JPY",
                price_kind="official_list",
                tax_included=True,
            )
            scale = fields.get("スケール", "")
            if re.fullmatch(r"\d+\s*/\s*\d+", scale):
                row["scale"] = scale.replace(" ", "")
            row["franchise"] = fields.get("作品") or row.get("franchise")
            row.update(checked_at=now().isoformat(), source_url=url)
            row["source_text"] = json.dumps(
                {k: v for k, v in row.items() if k != "source_text"}, ensure_ascii=False
            )
            candidates = original_candidates(html, url, sku)
            if not candidates:
                raise ValueError("ORIGINAL_IMAGE_CANDIDATES_MISSING")
            record.update(
                metadata=row, candidates=len(candidates), checked_at=row["checked_at"]
            )
            for candidate in candidates:
                if len(record["images"]) >= args.max_images:
                    break
                try:
                    record["images"].append(
                        download(fetcher, candidate, root / "media", args.max_image_mb)
                    )
                except Exception as exc:
                    record["image_failures"].append(
                        dict(
                            source_url=candidate["source_url"], error=type(exc).__name__
                        )
                    )
                    if isinstance(exc, CollectionDenied) or getattr(
                        getattr(exc, "response", None), "status_code", 0
                    ) in (401, 403, 429):
                        raise
            record["status"] = (
                "ready"
                if record["images"] and not record["image_failures"]
                else "partial"
            )
            done += 1
        except Exception as exc:
            record["error"] = type(exc).__name__
            if isinstance(exc, (ValueError, CollectionDenied)):
                record["reason"] = str(exc)[:150]
            save_json(path, record)
            emit(
                url=url,
                status=record["status"],
                error=record["error"],
                reason=record.get("reason"),
            )
            if isinstance(exc, CollectionDenied) or getattr(
                getattr(exc, "response", None), "status_code", 0
            ) in (401, 403, 429):
                emit(state="stopped_access_restriction", resume_supported=True)
                return 2
            done += 1
            continue
        save_json(path, record)
        emit(
            url=url,
            status=record["status"],
            images=len(record["images"]),
            dimensions=[[x["width"], x["height"]] for x in record["images"]],
        )
    emit(state="collection_pass_finished", processed=done, bundle=str(root))


def apply(args, root):
    from sqlalchemy import select, text, or_
    from app.core.database import SessionLocal
    from app.core.config import get_settings
    from app.models.entities import (
        Figure,
        FigureVariant,
        Manufacturer,
        ProductImage,
        ReleasePrice,
        CollectionJob,
    )
    from scripts.seed import seed
    from app.services.catalog_ingest import INGEST_LOCK, INDEX_JOB

    count = 0
    for path in sorted((root / "products").glob("*.json")):
        if count >= args.limit:
            break
        rec = json.loads(path.read_text(encoding="utf-8"))
        if rec.get("status") != "ready":
            continue
        row = rec["metadata"]
        # Validate all file contents before any DB write or file copy.
        for im in rec["images"]:
            src = (root / im["file"]).resolve()
            if not src.is_relative_to((root / "media").resolve()):
                raise ValueError("UNSAFE_BUNDLE_PATH")
            raw = src.read_bytes()
            if hashlib.sha256(raw).hexdigest() != im["sha256"]:
                raise ValueError("HASH_MISMATCH")
            ext, w, h = image_info(raw)
            if [w, h] != [im["width"], im["height"]] or src.name != im[
                "sha256"
            ] + "." + ext:
                raise ValueError("IMAGE_MANIFEST_MISMATCH")
        with SessionLocal() as db:
            if args.commit and db.bind.dialect.name == "postgresql":
                db.execute(text("SELECT pg_advisory_xact_lock(:k)"), {"k": INGEST_LOCK})
            f = db.scalar(
                select(Figure).where(Figure.official_url == row["official_url"])
            )
            if f and f.manufacturer.name != "Kotobukiya":
                raise ValueError("MANUFACTURER_CONFLICT")
            if not f:
                duplicate = db.scalar(
                    select(Figure.id)
                    .join(FigureVariant)
                    .join(Manufacturer, Manufacturer.id == Figure.manufacturer_id)
                    .where(
                        Manufacturer.name == "Kotobukiya",
                        FigureVariant.sku == row["sku"],
                    )
                )
                if duplicate:
                    emit(
                        url=row["official_url"],
                        state="duplicate_sku_review",
                        figure_id=duplicate,
                    )
                    continue
            if f and len(f.variants) != 1:
                emit(url=row["official_url"], state="variant_review")
                continue
            if f and f.variants[0].sku and f.variants[0].sku != row["sku"]:
                raise ValueError("SKU_CONFLICT")
            if not args.commit:
                emit(
                    url=row["official_url"],
                    state="preview",
                    images=len(rec["images"]),
                    new_product=f is None,
                )
                count += 1
                continue
            if not f:
                seed(db, [row], refresh=False)
                f = db.scalar(
                    select(Figure).where(Figure.official_url == row["official_url"])
                )
            v = f.variants[0]
            if not v.sku:
                v.sku = row["sku"]
            folder = get_settings().media_dir
            folder.mkdir(parents=True, exist_ok=True)
            for im in rec["images"]:
                src = root / im["file"]
                dest = folder / src.name
                if (
                    dest.exists()
                    and hashlib.sha256(dest.read_bytes()).hexdigest() != im["sha256"]
                ):
                    raise ValueError("EXISTING_MEDIA_HASH_CONFLICT")
                if not dest.exists():
                    tmp = dest.with_suffix(".importing")
                    shutil.copyfile(src, tmp)
                    tmp.replace(dest)
                image = db.scalar(
                    select(ProductImage).where(
                        ProductImage.variant_id == v.id,
                        ProductImage.source_url == im["source_url"],
                    )
                )
                if not image:
                    image = ProductImage(variant_id=v.id, source_url=im["source_url"])
                    db.add(image)
                image.image_url = "/api/media/" + src.name
                image.usage_status = "personal_local"
            price = db.scalar(
                select(ReleasePrice).where(
                    ReleasePrice.variant_id == v.id,
                    ReleasePrice.source_url == row["official_url"],
                    ReleasePrice.price_kind == "official_list",
                )
            )
            if not price:
                price = ReleasePrice(
                    variant_id=v.id,
                    source_url=row["official_url"],
                    price_kind="official_list",
                )
                db.add(price)
            from datetime import datetime

            price.price_amount = row["price_amount"]
            price.currency = "JPY"
            price.tax_included = True
            price.checked_at = datetime.fromisoformat(row["checked_at"])
            if not db.scalar(
                select(CollectionJob.id).where(
                    CollectionJob.collector == INDEX_JOB,
                    CollectionJob.status == "pending",
                    CollectionJob.error_summary.contains(row["official_url"]),
                )
            ):
                db.add(
                    CollectionJob(
                        collector=INDEX_JOB,
                        status="pending",
                        count=0,
                        error_summary=json.dumps({"url": row["official_url"]}),
                    )
                )
            db.commit()
            count += 1
            emit(
                figure_id=f.id,
                state="applied",
                images=len(rec["images"]),
                index="pending",
            )
    emit(state="apply_finished", processed=count, commit=args.commit)


def main():
    import fcntl

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--stage", choices=["collect", "apply"], required=True)
    p.add_argument("--input", default="/app/koto_input/all_candidates.jsonl")
    p.add_argument("--bundle", default="/app/media/kotobukiya_original_bundle")
    p.add_argument("--limit", type=int, default=3)
    p.add_argument("--max-images", type=int, default=15)
    p.add_argument("--max-image-mb", type=int, default=100)
    p.add_argument("--retry", action="store_true")
    p.add_argument("--commit", action="store_true")
    args = p.parse_args()
    if min(args.limit, args.max_images, args.max_image_mb) < 1:
        p.error("Limits must be positive")
    root = Path(args.bundle)
    root.mkdir(parents=True, exist_ok=True)
    for name in ["media", "products"]:
        (root / name).mkdir(exist_ok=True)
    with (root / ".lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            emit(state="busy")
            return 1
        return collect(args, root) if args.stage == "collect" else apply(args, root)


if __name__ == "__main__":
    raise SystemExit(main())
