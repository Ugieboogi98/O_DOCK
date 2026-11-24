"""Korean official Bandai collector. Preview by default; no LLM or indexing calls.

Unmatched JANs are exported for review. --commit updates only unique exact JAN
or already linked Korean URLs. --create-new explicitly permits unmatched new rows.
"""

import argparse
import hashlib
import json
import re
import time
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urljoin, urlparse

from bs4 import BeautifulSoup

BASE = "https://www.bnkrmall.co.kr"
CDN = "cdn.bnkrmall.co.kr"
LABELS = (
    "제품명",
    "상품명",
    "모델명",
    "판매코드",
    "제조사/매입처",
    "크기, 중량",
    "사용연령 또는 체중범위",
    "제조국",
    "재질",
    "색상",
    "브랜드",
    "브랜드명",
)
BANPRESTO_LINES = (
    (r"GLITTER\s*[&＆]\s*GLAMOURS|글리터\s*[&＆]\s*글래머러스", "GLITTER&GLAMOURS"),
    (r"KING\s+OF\s+ARTIST|킹\s*오브\s*아티스트", "KING OF ARTIST"),
    (r"WORLD\s+COLLECTABLE|월드\s*[콜컬]렉터블|\bWCF\b", "World Collectable Figure"),
    (r"VIBRATION\s*STARS|바이브레이션\s*스타즈", "VIBRATION STARS"),
    (r"Q\s*POSKET|큐\s*포스켓|큐포스켓", "Q posket"),
    (r"GRANDISTA|그란디스타|그랜디스타", "Grandista"),
    (r"ESPRESTO|에스프레스토", "ESPRESTO"),
    (r"EFFECTREME|이펙트림", "EFFECTREME"),
    (r"MATCH\s*MAKERS|매치\s*메이커", "MATCH MAKERS"),
    (r"G\s*[×x]\s*MATERIA|지\s*마테리아", "G×materia"),
    (r"\bDXF\b", "DXF"),
    (r"\bEXQ\b", "EXQ"),
    (r"SOLID\s*EDGE\s*WORKS|솔리드\s*엣지", "SOLID EDGE WORKS"),
    (r"BATTLE\s*RECORD|배틀\s*레코드", "BATTLE RECORD COLLECTION"),
    (r"RELAX\s*TIME|릴랙스\s*타임", "Relax time"),
    (r"AMAZING\s*HEROES|어메이징\s*히어로", "THE AMAZING HEROES"),
)
TAMASHII_LINES = (
    (r"S\s*\.?\s*H\s*\.?\s*(?:피규아트|FIGUARTS)", "S.H.Figuarts"),
    (r"FIGUARTS\s*ZERO|피규아[트츠]\s*ZERO|피규아[트츠]\s*제로", "Figuarts ZERO"),
    (r"FIGUARTS\s*MINI|피규아[트츠]\s*미니", "Figuarts mini"),
    (r"S\.?H\.?\s*(?:MONSTERARTS|몬스터아츠)", "S.H.MonsterArts"),
    (r"METAL\s*ROBOT|메탈\s*로보[트트]?\s*혼", "METAL ROBOT魂"),
    (r"ROBOT魂|ROBOT혼|로보[트트]?혼|로보[트트]?\s*혼", "ROBOT魂"),
    (r"METAL\s*BUILD|메탈\s*빌드", "METAL BUILD"),
    (r"초합금혼|SOUL\s*OF\s*CHOGOKIN", "초합금혼"),
    (r"초합금|CHOGOKIN", "초합금"),
    (r"PROPLICA|프로플리카", "PROPLICA"),
    (r"NXEDGE|넥스엣지", "NXEDGE STYLE"),
    (r"건담\s*유니버스|GUNDAM\s*UNIVERSE", "GUNDAM UNIVERSE"),
    (r"세인트\s*세이야|성투사성의신화", "성투사성의신화"),
)


def classify_product(name, fields=None, category_group=None, category_evidence=False):
    """Category membership is evidence; series names are helpful, not an allowlist."""
    fields = fields or {}
    if re.search(
        r"(?<![A-Z0-9])(?:HG|RG|MG|PG|EG|SDCS|SDEX|30MM|30MS|30MP|SMP)(?![A-Z0-9])|30\s*MINUTES|FIGURE[ -]?RISE|피규어라이즈|프라모델|프라 모델",
        name,
        re.I,
    ):
        return False, None, None, "model_kit_excluded"
    maker = fields.get("제조사/매입처", "")
    if maker and not re.search(r"BANDAI|BANPRESTO|반다이|반프레스토", maker, re.I):
        return False, None, None, "manufacturer_review"
    # Do not silently store BANDAI Co. products as BANDAI SPIRITS.
    if maker and not re.search(r"SPIRITS|BANPRESTO|스피리츠|반프레스토", maker, re.I):
        return False, None, None, "manufacturer_review"
    text = " ".join([name, fields.get("브랜드", ""), fields.get("브랜드명", "")])
    for pattern, line in BANPRESTO_LINES:
        if re.search(pattern, text, re.I):
            return True, "BANPRESTO", line, "known_figure_line"
    if category_group == "BANPRESTO" or re.search(r"BANPRESTO|반프레스토", text, re.I):
        return (
            True,
            "BANPRESTO",
            fields.get("브랜드명") or fields.get("브랜드"),
            "figure_category",
        )
    for pattern, line in TAMASHII_LINES:
        if re.search(pattern, text, re.I):
            return True, "TAMASHII NATIONS", line, "known_figure_line"
    if category_evidence:
        return (
            True,
            category_group or "피규어",
            fields.get("브랜드명") or fields.get("브랜드"),
            "figure_category",
        )
    return False, None, None, "figure_category_unconfirmed"


def category_links(html):
    soup = BeautifulSoup(html, "html.parser")
    result = {}
    for a in soup.select('a[href*="/goods/category.do"]'):
        p = urlparse(urljoin(BASE, a["href"]))
        cate = parse_qs(p.query).get("cate", [""])[0]
        label = a.get_text(" ", strip=True) + " " + (a.get("title") or "")
        label += " " + " ".join(img.get("alt", "") for img in a.select("img"))
        if p.hostname != "www.bnkrmall.co.kr" or not cate.isdigit():
            continue
        if re.search(r"BANPRESTO|반프레스토", label, re.I):
            result[cate] = "BANPRESTO"
        elif re.fullmatch(
            r"\s*(?:피규어|타마시이네이션즈|TAMASHII\s*NATIONS)\s*", label, re.I
        ):
            result.setdefault(
                cate,
                (
                    "TAMASHII NATIONS"
                    if "타마시이" in label or "TAMASHII" in label.upper()
                    else "피규어"
                ),
            )
    return result


def listing_links(html):
    soup = BeautifulSoup(html, "html.parser")
    result = []
    for a in soup.select('a[href*="/goods/detail.do"]'):
        if a.find_parent(["header", "nav", "footer"]):
            continue
        if any(
            re.search(
                r"header(?!-next\b)|footer|gnb|navigation|mega[-_]?menu|recommend|recent[-_]?goods",
                " ".join([parent.get("id", ""), *parent.get("class", [])]),
                re.I,
            )
            for parent in a.parents
            if getattr(parent, "attrs", None)
        ):
            continue
        url = normalize_url(a["href"])
        if url:
            result.append((url, a.get_text(" ", strip=True)))
    return result


def emit(**row):
    print(json.dumps(row, ensure_ascii=False), flush=True)


def normalize_url(url):
    p = urlparse(urljoin(BASE, url))
    gno = parse_qs(p.query).get("gno", [""])[0]
    if (
        p.scheme == "https"
        and p.hostname == "www.bnkrmall.co.kr"
        and p.path == "/goods/detail.do"
        and gno.isdigit()
    ):
        return BASE + "/goods/detail.do?" + urlencode({"gno": gno})


def valid_jan(value):
    if not re.fullmatch(r"\d{13}", value):
        return False
    total = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(value[:12]))
    return (10 - total % 10) % 10 == int(value[-1])


def parse_product(html, url, category_group=None, category_evidence=False):
    soup = BeautifulSoup(html, "html.parser")
    if "request rejected" in soup.get_text(" ", strip=True).lower():
        raise ValueError("REQUEST_REJECTED")
    fields = {}
    for row in soup.select("table tr"):
        cells = [
            re.sub(r"\s+", " ", c.get_text(" ", strip=True))
            for c in row.find_all(["th", "td"])
        ]
        for i, text in enumerate(cells[:-1]):
            if text in LABELS:
                fields.setdefault(text, cells[i + 1])
    tag = soup.select_one('meta[property="og:description"]')
    name = (
        fields.get("제품명")
        or fields.get("상품명")
        or (tag.get("content", "").strip() if tag else "")
    )
    if not name:
        raise ValueError("PRODUCT_NAME_MISSING")
    accepted, group, line, scope_reason = classify_product(
        name, fields, category_group, category_evidence
    )
    jan_text = fields.get("모델명", "")
    jan_candidates = re.findall(r"(?<!\d)\d{13}(?!\d)", jan_text)
    jan = next((x for x in jan_candidates if valid_jan(x)), None)
    images = []
    og = soup.select_one('meta[property="og:image"]')
    if og:
        candidate = urljoin(url, og.get("content", ""))
        p = urlparse(candidate)
        if (
            p.scheme == "https"
            and p.hostname == CDN
            and p.path.startswith("/live/data/base/goods/big/")
        ):
            images.append(candidate)
    for img in soup.select("img"):
        candidate = urljoin(url, img.get("data-src") or img.get("src") or "")
        p = urlparse(candidate)
        if (
            p.scheme == "https"
            and p.hostname == CDN
            and p.path.startswith("/live/data/base/editor/")
            and re.search(r"\.(jpg|jpeg|png|webp)$", p.path, re.I)
            and candidate not in images
        ):
            images.append(candidate)
    from app.collectors.bnkr_prices import parse_prices, PriceError

    try:
        parsed_price = parse_prices(html)
        price = str(parsed_price["sale_krw"])
        price_state = "displayed_sale_price"
    except PriceError as exc:
        price = None
        price_state = str(exc)
    return dict(
        url=url,
        name_ko=name,
        accepted=accepted,
        jan_code=jan,
        brand_group=group,
        product_line=line,
        scope_reason=scope_reason,
        specifications=fields,
        images=images,
        price_krw=price,
        price_state=price_state,
    )


def make_fetcher():
    from app.collectors.safe_http import SafeFetcher

    fetcher = SafeFetcher()
    # This job configures only the requested official source; it does not edit
    # the shared source_policy.json used by other running jobs.
    fetcher.policy["www.bnkrmall.co.kr"] = {
        "enabled": True,
        "paths": ["/main/figure_index.do", "/goods/category.do", "/goods/detail.do"],
        "delay_seconds": 2,
    }
    return fetcher


def match_variant(db, row):
    from sqlalchemy import select
    from app.models.entities import Figure, FigureVariant, Manufacturer, SourceDocument

    maker = Manufacturer.name == "Bandai Spirits"
    linked = list(
        db.scalars(
            select(FigureVariant)
            .join(Figure)
            .join(Manufacturer)
            .where(maker)
            .where(
                FigureVariant.id.in_(
                    select(SourceDocument.variant_id).where(
                        SourceDocument.url == row["url"]
                    )
                )
            )
        )
    )
    if not linked:
        linked = list(
            db.scalars(
                select(FigureVariant)
                .join(Figure)
                .join(Manufacturer)
                .where(maker, Figure.official_url == row["url"])
            )
        )
    jan_matches = (
        list(
            db.scalars(
                select(FigureVariant)
                .join(Figure)
                .join(Manufacturer)
                .where(maker, FigureVariant.jan_code == row["jan_code"])
            )
        )
        if row["jan_code"]
        else []
    )
    if len(linked) > 1 or len(jan_matches) > 1:
        return None, "ambiguous_match"
    if linked:
        variant = linked[0]
        if variant.jan_code and row["jan_code"] and variant.jan_code != row["jan_code"]:
            return None, "jan_conflict"
        if jan_matches and jan_matches[0].id != variant.id:
            return None, "jan_conflict"
        return variant, "linked_url"
    if jan_matches:
        return jan_matches[0], "exact_jan"
    return None, "unmatched_jan" if row["jan_code"] else "jan_missing"


def store_product(row, args, fetcher):
    from sqlalchemy import select, text
    from app.core.database import SessionLocal
    from app.core.config import get_settings
    from app.models.entities import (
        Figure,
        FigureVariant,
        Manufacturer,
        ProductLine,
        SourceDocument,
        ProductImage,
        ReleasePrice,
        now,
    )
    from app.services.enrichment import download_image, usable_image
    from app.services.import_pipeline import commit_import

    with SessionLocal() as db:
        if args.commit and db.bind.dialect.name == "postgresql":
            db.execute(text("SELECT pg_advisory_xact_lock(2026102203)"))
        variant, match = match_variant(db, row)
        report = {"match": match, "figure_id": variant.figure_id if variant else None}
        if not args.commit:
            return report
        if not variant and (not args.create_new or match != "unmatched_jan"):
            return dict(report, state="needs_review")
        created = False
        if variant is None:
            maker = db.scalar(
                select(Manufacturer).where(Manufacturer.name == "Bandai Spirits")
            )
            if maker is None:
                raise ValueError("BANDAI_MANUFACTURER_MISSING")
            line = None
            if row.get("product_line"):
                line = db.scalar(
                    select(ProductLine).where(
                        ProductLine.manufacturer_id == maker.id,
                        ProductLine.name == row["product_line"],
                    )
                )
                if line is None:
                    line = ProductLine(
                        manufacturer_id=maker.id, name=row["product_line"]
                    )
                    db.add(line)
                    db.flush()
            figure = Figure(
                manufacturer_id=maker.id,
                product_line_id=line.id if line else None,
                name_original=row["name_ko"],
                name_ko=row["name_ko"],
                official_url=row["url"],
                type="figure",
                quality="official_metadata",
            )
            db.add(figure)
            db.flush()
            variant = FigureVariant(
                figure_id=figure.id, variant_key="source-page", jan_code=row["jan_code"]
            )
            db.add(variant)
            db.flush()
            created = True
        figure = variant.figure
        # Keep existing original URL, Japanese source and user-edited Korean name.
        if not figure.name_ko:
            figure.name_ko = row["name_ko"]
        if not variant.jan_code and row["jan_code"]:
            variant.jan_code = row["jan_code"]
        body = "\n".join(
            [
                row["name_ko"],
                "브랜드 구분: " + (row.get("brand_group") or "미확인"),
                "상품 라인: " + (row.get("product_line") or "미확인"),
            ]
            + [
                f"{key}: {value}"
                for key, value in row["specifications"].items()
                if key != "판매코드"
            ]
        )
        document = db.scalar(
            select(SourceDocument).where(
                SourceDocument.variant_id == variant.id,
                SourceDocument.url == row["url"],
            )
        )
        if document is None:
            document = SourceDocument(variant_id=variant.id, url=row["url"])
            db.add(document)
        document.title = row["name_ko"]
        document.language = "ko"
        document.source_type = "official_korean_metadata"
        document.usage_status = "factual_metadata_only"
        document.body = body
        document.content_hash = hashlib.sha256(body.encode()).hexdigest()
        document.collected_at = now()
        if row["price_krw"]:
            price = db.scalar(
                select(ReleasePrice).where(
                    ReleasePrice.variant_id == variant.id,
                    ReleasePrice.source_url == row["url"],
                    ReleasePrice.price_kind == "korea_official_sale",
                )
            )
            if price is None:
                price = ReleasePrice(
                    variant_id=variant.id,
                    source_url=row["url"],
                    price_kind="korea_official_sale",
                    currency="KRW",
                )
                db.add(price)
            price.price_amount = Decimal(row["price_krw"])
            price.checked_at = now()
        staging = commit_import(db, [figure])
        added, failures = 0, []
        for source in row["images"][: args.max_images]:
            old = db.scalar(
                select(ProductImage).where(
                    ProductImage.variant_id == variant.id,
                    ProductImage.source_url == source,
                )
            )
            if old and (old.usage_status == "duplicate_hidden" or usable_image(old)):
                continue
            try:
                fetcher.check_robots(source, CDN)
                local = download_image(source, get_settings().media_dir)
                if old is None:
                    old = ProductImage(variant_id=variant.id, source_url=source)
                    db.add(old)
                old.image_url = local
                old.usage_status = "personal_local"
                db.commit()
                added += 1
            except Exception as exc:
                db.rollback()
                failures.append(type(exc).__name__)
            time.sleep(2)
        return dict(
            report,
            state="saved",
            figure_id=figure.id,
            created=created,
            images_added=added,
            image_failures=failures,
            indexed=False,
            **staging,
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Accepted figure products, not all scanned URLs",
    )
    parser.add_argument("--max-pages", type=int, default=1)
    parser.add_argument("--max-images", type=int, default=15)
    parser.add_argument("--commit", action="store_true")
    parser.add_argument(
        "--create-new",
        action="store_true",
        help="Permit new rows for unmatched valid JANs; inspect preview for overlaps first",
    )
    parser.add_argument(
        "--scope",
        choices=("all", "banpresto", "tamashii"),
        default="all",
        help="Default: whole figure tab, with BANPRESTO first",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Revisit URLs already saved by this Korean collector",
    )
    parser.add_argument(
        "--url", action="append", help="Inspect a specific official product detail URL"
    )
    parser.add_argument("--category", type=int)
    args = parser.parse_args()
    if min(args.limit, args.max_pages, args.max_images) < 1:
        parser.error("limits must be positive")
    from app.core.config import get_settings

    folder = get_settings().media_dir / "maker_catalogs" / "bnkrmall"
    folder.mkdir(parents=True, exist_ok=True)
    import fcntl

    with (folder / ".run.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            emit(state="busy")
            return 1
        fetcher = make_fetcher()
        candidates = {}

        def add_candidate(url, label="", group=None, evidence=False):
            inferred, hint_group, _, _ = classify_product(label)
            rank = 0 if group == "BANPRESTO" or hint_group == "BANPRESTO" else 1
            old = candidates.get(url)
            candidate = dict(
                rank=rank, category_group=group, category_evidence=evidence
            )
            if (
                old is None
                or rank < old["rank"]
                or (evidence and not old["category_evidence"])
            ):
                candidates[url] = candidate

        if args.url:
            for raw in args.url:
                url = normalize_url(raw)
                if not url:
                    parser.error("official Korean product URL required")
                add_candidate(url)
        else:
            html, _ = fetcher.fetch_page(BASE + "/main/figure_index.do")
            categories = category_links(html)
            categories.setdefault("1607", "피규어")
            if args.category:
                categories = {str(args.category): "피규어"}
            if "BANPRESTO" not in categories.values():
                emit(
                    warning="BANPRESTO_CATEGORY_LINK_NOT_FOUND",
                    detail="Only discovered figure links can be inspected; do not assume full Banpresto coverage",
                )
            if not args.category:
                for url, label in listing_links(html):
                    add_candidate(url, label)
            pages = [
                (BASE + f"/goods/category.do?cate={cate}&page={i}", group)
                for cate, group in sorted(
                    categories.items(), key=lambda x: x[1] != "BANPRESTO"
                )
                for i in range(1, args.max_pages + 1)
            ]
            emit(figure_categories=categories, scope=args.scope, priority="BANPRESTO")
            for page, group in pages:
                html, _ = fetcher.fetch_page(page)
                for url, label in listing_links(html):
                    add_candidate(url, label, group, True)
        urls = sorted(candidates, key=lambda url: candidates[url]["rank"])
        state_file = folder / "saved_urls.json"
        saved_urls = (
            set(json.loads(state_file.read_text(encoding="utf-8")))
            if state_file.exists()
            else set()
        )
        stats = dict(
            discovered=len(urls),
            scanned=0,
            accepted=0,
            skipped=0,
            already_saved=0,
            saved=0,
            failed=0,
        )
        output = folder / ("last_commit.jsonl" if args.commit else "last_preview.jsonl")
        with output.open("w", encoding="utf-8") as log:
            for url in urls:
                if stats["accepted"] >= args.limit:
                    break
                if args.commit and not args.refresh and url in saved_urls:
                    stats["already_saved"] += 1
                    continue
                try:
                    html, final = fetcher.fetch_page(url)
                    if normalize_url(final) != url:
                        raise ValueError("DETAIL_REDIRECT_REVIEW")
                    info = candidates[url]
                    row = parse_product(
                        html, url, info["category_group"], info["category_evidence"]
                    )
                    stats["scanned"] += 1
                    scope_matches = args.scope == "all" or row["brand_group"] == {
                        "banpresto": "BANPRESTO",
                        "tamashii": "TAMASHII NATIONS",
                    }.get(args.scope)
                    if not row["accepted"] or not scope_matches:
                        stats["skipped"] += 1
                        emit(
                            url=url,
                            name=row["name_ko"],
                            state="outside_scope",
                            reason=(
                                row["scope_reason"]
                                if not row["accepted"]
                                else "scope_filter"
                            ),
                        )
                        continue
                    result = store_product(row, args, fetcher)
                    stats["accepted"] += 1
                    stats["saved"] += int(result.get("state") == "saved")
                    log.write(json.dumps({**row, **result}, ensure_ascii=False) + "\n")
                    log.flush()
                    if result.get("state") == "saved" and not result.get(
                        "image_failures"
                    ):
                        saved_urls.add(url)
                        temp = state_file.with_suffix(".tmp")
                        temp.write_text(
                            json.dumps(sorted(saved_urls)), encoding="utf-8"
                        )
                        temp.replace(state_file)
                    emit(**row, **result)
                except Exception as exc:
                    stats["failed"] += 1
                    emit(
                        url=url,
                        error=type(exc).__name__,
                        reason=str(exc)[:100] if isinstance(exc, ValueError) else None,
                    )
        emit(
            **stats,
            mode="COMMIT" if args.commit else "PREVIEW",
            log_file=str(output),
            indexed=False,
        )
        return 1 if stats["failed"] else 0


def refresh_source(source, max_pages, limit):
    """Bounded automatic pass, serialized with the manual BNKR command."""
    import fcntl
    from types import SimpleNamespace
    from app.core.config import get_settings

    folder = get_settings().media_dir / "maker_catalogs" / "bnkrmall"
    folder.mkdir(parents=True, exist_ok=True)
    summary = dict(new_products=0, processed_products=0, failed=0, checked_pages=0)
    with (folder / ".run.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return dict(summary, state="busy")
        fetcher = make_fetcher()
        args = SimpleNamespace(commit=True, create_new=True, max_images=1000)
        state_file = folder / "saved_urls.json"
        saved = (
            set(json.loads(state_file.read_text())) if state_file.exists() else set()
        )
        seen = set()
        category = int(source["category"])
        for page in range(1, max_pages + 1):
            html, _ = fetcher.fetch_page(
                BASE + f"/goods/category.do?cate={category}&page={page}"
            )
            summary["checked_pages"] += 1
            links = listing_links(html)
            if not links:
                raise ValueError("NO_PRODUCT_LINKS_REVIEW_HTML_OR_JS")
            for url, label in links:
                if url in seen or url in saved:
                    continue
                seen.add(url)
                if summary["processed_products"] >= limit:
                    return dict(
                        summary, state="partial" if summary["failed"] else "completed"
                    )
                summary["processed_products"] += 1
                try:
                    html, final = fetcher.fetch_page(url)
                    if normalize_url(final) != url:
                        raise ValueError("DETAIL_REDIRECT_REVIEW")
                    row = parse_product(html, url, category_evidence=True)
                    if not row["accepted"]:
                        continue
                    result = store_product(row, args, fetcher)
                    summary["new_products"] += int(result.get("created", False))
                    if (
                        result.get("state") == "saved"
                        and not result.get("image_failures")
                        and row["price_krw"]
                    ):
                        saved.add(url)
                        temp = state_file.with_suffix(".tmp")
                        temp.write_text(json.dumps(sorted(saved)))
                        temp.replace(state_file)
                    if (
                        result.get("state") != "saved"
                        or result.get("image_failures")
                        or not row["price_krw"]
                    ):
                        summary["failed"] += 1
                except Exception:
                    summary["failed"] += 1
        return dict(summary, state="partial" if summary["failed"] else "completed")
