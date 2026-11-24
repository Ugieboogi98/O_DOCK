"""Collect official S.H.Figuarts pages through related-product links and repair images.

Place at backend/scripts/collect_bandai_with_images.py. This job does not translate.
Default mode is read-only. --commit saves products and their local image copies.
"""

import argparse
import fcntl
import json
import re
import time
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from sqlalchemy import select

from app.collectors.manufacturers.bandai import Adapter
from app.collectors.safe_http import SafeFetcher
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import Figure, Manufacturer, ProductImage
from app.services.catalog_ingest import collect_one
from app.services.enrichment import download_image, usable_image

HOST = "tamashiiweb.com"
HEADER_PREFIX = f"https://{HOST}/assets/img/header/"
PRODUCT = re.compile(r"^https://tamashiiweb\.com/item/(\d+)/?$", re.I)


def emit(**fields):
    print(json.dumps(fields, ensure_ascii=False), flush=True)


def save_json(path, value):
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(path)


def product_url(url):
    match = PRODUCT.fullmatch(url.split("#", 1)[0])
    return f"https://{HOST}/item/{int(match.group(1))}/" if match else None


def product_images(html, url):
    """Select this page's numbered gallery or main/sub gallery, not header cards."""
    product_id = int(PRODUCT.fullmatch(url).group(1))
    prefix = f"/storage/images/products/imported/item_{product_id:010d}_"
    soup = BeautifulSoup(html, "html.parser")
    images = []
    for tag in soup.select("main img"):
        for attr in ("data-src", "data-original", "src"):
            src = tag.get(attr)
            if not src:
                continue
            candidate = urljoin(url, src)
            path = urlparse(candidate).path
            page_gallery = (
                path.startswith(prefix)
                or path.startswith("/storage/images/products/main/")
                or path.startswith("/storage/images/products/sub/")
            )
            if (
                urlparse(candidate).hostname == HOST
                and page_gallery
                and re.search(r"\.(?:jpg|jpeg|png|webp)$", path, re.I)
                and candidate not in images
            ):
                images.append(candidate)
    if not images:
        # The official Open Graph image belongs to this page; use it only when
        # the numbered gallery is absent, never related-item thumbnails.
        tag = soup.select_one('meta[property="og:image"]')
        candidate = urljoin(url, tag.get("content", "")) if tag else ""
        parsed = urlparse(candidate)
        main_sources = {
            urljoin(url, image.get("data-src") or image.get("src") or "")
            for image in soup.select("main img")[:20]
        }
        if (
            parsed.hostname == HOST
            and parsed.path.startswith("/storage/images/products/thumbnail/")
            and candidate in main_sources
        ):
            images.append(candidate)
    return images


def is_shfiguarts(html):
    soup = BeautifulSoup(html, "html.parser")
    return any(
        (tag.get("alt") or "").strip() == "S.H.Figuarts"
        for tag in soup.select("main img[alt]")
    )


def existing_figure(url):
    with SessionLocal() as db:
        return db.scalar(select(Figure.id).where(Figure.official_url == url))


def repair_images(fetcher, figure_id, html, url, max_images):
    candidates = product_images(html, url)[:max_images]
    with SessionLocal() as db:
        figure = db.get(Figure, figure_id)
        if not figure or not figure.variants:
            return {"state": "no_variant"}
        variant_ids = [v.id for v in figure.variants]
        images = list(
            db.scalars(
                select(ProductImage).where(ProductImage.variant_id.in_(variant_ids))
            )
        )
        old_bad = [img for img in images if img.source_url.startswith(HEADER_PREFIX)]
        good_urls = {img.source_url for img in images if usable_image(img)}
        added, failed = 0, []
        for source in candidates:
            if source in good_urls:
                continue
            try:
                # The website policy permits product pages; downloaded image
                # hosts/paths are narrowed above and robots are checked here.
                fetcher.check_robots(source, HOST)
                local = download_image(source, get_settings().media_dir)
                record = next((img for img in images if img.source_url == source), None)
                if record:
                    record.image_url = local
                    record.usage_status = "personal_local"
                else:
                    record = ProductImage(
                        variant_id=figure.variants[0].id,
                        source_url=source,
                        image_url=local,
                        usage_status="personal_local",
                    )
                    db.add(record)
                db.commit()
                good_urls.add(source)
                added += 1
                time.sleep(max(1, get_settings().collection_delay_seconds))
            except Exception as exc:
                db.rollback()
                failed.append({"url": source, "error": type(exc).__name__})
        # Never remove old rows before at least one page-specific image exists.
        valid_page_image = bool(set(candidates) & good_urls)
        removed = 0
        if valid_page_image:
            for img in old_bad:
                db.delete(img)
                removed += 1
            db.commit()
        return {
            "state": "completed" if valid_page_image else "no_verified_image",
            "found": len(candidates),
            "added": added,
            "removed_header_rows": removed,
            "failures": failed,
        }


def seeds():
    with SessionLocal() as db:
        figures = db.scalars(
            select(Figure)
            .join(Manufacturer)
            .where(Manufacturer.name == "Bandai Spirits")
            .order_by(Figure.id)
        ).all()
        return [url for f in figures if (url := product_url(f.official_url))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true")
    parser.add_argument(
        "--repair-only",
        action="store_true",
        help="Only examine the existing Bandai product pages",
    )
    parser.add_argument("--max-pages", type=int, default=3)
    parser.add_argument("--max-new", type=int, default=20)
    parser.add_argument("--max-images", type=int, default=15)
    args = parser.parse_args()
    if min(args.max_pages, args.max_new, args.max_images) < 1:
        parser.error("All limits must be positive")
    start = seeds()
    if not start:
        parser.error("No official Bandai product detail seed URLs in DB")
    folder = get_settings().media_dir / "maker_catalogs" / "bandai_verified"
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / ".run.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            emit(state="busy")
            return 1
        checkpoint = folder / "checkpoint.json"
        state = (
            json.loads(checkpoint.read_text(encoding="utf-8"))
            if args.commit and checkpoint.exists()
            else {}
        )
        queue = deque(start if args.repair_only else state.get("queue", start))
        done = set() if args.repair_only else set(state.get("done", []))
        fetcher = SafeFetcher()
        adapter = Adapter()
        stats = {
            "pages": 0,
            "new_products": 0,
            "repaired": 0,
            "removed_header_rows": 0,
            "errors": [],
        }

        def persist():
            if args.commit and not args.repair_only:
                save_json(checkpoint, {"queue": list(queue), "done": sorted(done)})

        while (
            queue
            and stats["pages"] < args.max_pages
            and stats["new_products"] < args.max_new
        ):
            url = queue.popleft()
            if url in done or not product_url(url):
                continue
            try:
                html, final = fetcher.fetch_page(url)
                if product_url(final) != url:
                    raise ValueError("PRODUCT_REDIRECT_REVIEW")
                if not is_shfiguarts(html):
                    emit(url=url, state="outside_shfiguarts")
                    done.add(url)
                    persist()
                    continue
                candidate_images = product_images(html, url)
                related = [
                    link for link in adapter.discover(html, url) if product_url(link)
                ]
                related = list(dict.fromkeys(product_url(link) for link in related))
                figure_id = existing_figure(url)
                if args.commit:
                    if figure_id is None:
                        result = collect_one(fetcher, url)
                        figure_id = existing_figure(url)
                        stats["new_products"] += int(result.startswith("created"))
                    if figure_id:
                        result = repair_images(
                            fetcher, figure_id, html, url, args.max_images
                        )
                        stats["repaired"] += int(result["state"] == "completed")
                        stats["removed_header_rows"] += result.get(
                            "removed_header_rows", 0
                        )
                        emit(figure_id=figure_id, url=url, images=result)
                else:
                    emit(
                        url=url,
                        existing_figure_id=figure_id,
                        own_images=candidate_images[: args.max_images],
                        related_count=len(related),
                        related_sample=related[:5],
                    )
                stats["pages"] += 1
                done.add(url)
                if not args.repair_only:
                    for link in related:
                        if link not in done and link not in queue:
                            queue.append(link)
                persist()
            except Exception as exc:
                stats["errors"].append({"url": url, "error": type(exc).__name__})
                # Keep the failed page out of the immediate queue, but visible
                # in the summary for targeted diagnosis and a later retry.
                done.add(url)
                persist()
                emit(url=url, error=type(exc).__name__)
        emit(
            **stats,
            remaining_pages=len(queue),
            mode="COMMIT" if args.commit else "PREVIEW",
        )
        return 1 if stats["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
