"""Preview BNKR displayed sale prices, or update prices of already saved products.

Does not change collect_bnkrmall.py, product metadata, images, translations or indexes.
Use --url repeatedly for a three-product preview. --all-saved reads stored product
links from DB. Writes require --commit; run writes after current collection ends.
"""

import argparse
import json
import os
import re
from contextlib import ExitStack, nullcontext
from datetime import datetime, timezone
from decimal import Decimal
from urllib.parse import parse_qs, urlencode, urlparse

from bs4 import BeautifulSoup

BASE = "https://www.bnkrmall.co.kr"


def emit(**fields):
    print(json.dumps(fields, ensure_ascii=False), flush=True)


def canonical(url):
    p = urlparse(url)
    gno = parse_qs(p.query).get("gno", [""])
    if (
        p.scheme != "https"
        or p.hostname != "www.bnkrmall.co.kr"
        or p.username
        or p.password
        or p.port not in (None, 443)
        or p.path != "/goods/detail.do"
        or len(gno) != 1
        or not gno[0].isdigit()
    ):
        raise PriceError("OFFICIAL_PRODUCT_URL_REQUIRED")
    return BASE + "/goods/detail.do?" + urlencode({"gno": gno[0]})


from app.collectors.bnkr_prices import parse_prices, PriceError


def targets():
    from sqlalchemy import select
    from app.core.database import SessionLocal
    from app.models.entities import Figure, FigureVariant, Manufacturer, SourceDocument

    result = {}
    with SessionLocal() as db:
        queries = [
            select(SourceDocument.url, FigureVariant.id)
            .select_from(SourceDocument)
            .join(FigureVariant, SourceDocument.variant_id == FigureVariant.id)
            .join(Figure)
            .join(Manufacturer)
            .where(
                Manufacturer.name == "Bandai Spirits",
                SourceDocument.url.like(BASE + "/goods/detail.do?gno=%"),
            ),
            select(Figure.official_url, FigureVariant.id)
            .select_from(FigureVariant)
            .join(Figure)
            .join(Manufacturer)
            .where(
                Manufacturer.name == "Bandai Spirits",
                Figure.official_url.like(BASE + "/goods/detail.do?gno=%"),
            ),
        ]
        for query in queries:
            for url, vid in db.execute(query):
                try:
                    result.setdefault(canonical(url), set()).add(vid)
                except PriceError:
                    continue
    return result


def update_price(url, variant_id, amount, backup):
    from sqlalchemy import select
    from app.core.database import SessionLocal
    from app.models.entities import ReleasePrice, now

    with SessionLocal() as db:
        row = db.scalar(
            select(ReleasePrice)
            .where(
                ReleasePrice.variant_id == variant_id,
                ReleasePrice.source_url == url,
                ReleasePrice.price_kind == "korea_official_sale",
            )
            .with_for_update()
        )
        if row is not None and row.currency != "KRW":
            raise PriceError("EXISTING_PRICE_CURRENCY_CONFLICT")
        previous = (
            None
            if row is None
            else {
                "id": row.id,
                "amount": str(row.price_amount),
                "currency": row.currency,
                "checked_at": row.checked_at.isoformat() if row.checked_at else None,
            }
        )
        backup.write(
            json.dumps(
                {
                    "url": url,
                    "variant_id": variant_id,
                    "previous": previous,
                    "new_sale_krw": amount,
                },
                ensure_ascii=False,
            )
            + "\n"
        )
        backup.flush()
        os.fsync(backup.fileno())
        if row is None:
            row = ReleasePrice(
                variant_id=variant_id,
                source_url=url,
                price_kind="korea_official_sale",
                currency="KRW",
            )
            db.add(row)
        row.price_amount = Decimal(amount)
        row.checked_at = now()
        db.commit()
    return "saved"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", action="append")
    group.add_argument("--all-saved", action="store_true")
    p.add_argument(
        "--limit", type=int, default=3, help="URL count; 0 = all selected URLs"
    )
    p.add_argument("--commit", action="store_true")
    args = p.parse_args()
    if args.limit < 0:
        p.error("limit must be nonnegative")
    # Explicit URL preview does not even open a DB session.
    mapping = targets() if args.all_saved or args.commit else {}
    urls = (
        list(dict.fromkeys(canonical(url) for url in args.url))
        if args.url
        else sorted(mapping)
    )
    if args.limit:
        urls = urls[: args.limit]
    from app.collectors.safe_http import SafeFetcher
    from app.core.config import get_settings

    fetcher = SafeFetcher()
    fetcher.policy["www.bnkrmall.co.kr"] = {
        "enabled": True,
        "paths": ["/goods/detail.do"],
        "delay_seconds": 2,
    }
    folder = get_settings().media_dir / "maker_catalogs" / "bnkrmall"
    folder.mkdir(parents=True, exist_ok=True)
    import fcntl

    with ExitStack() as guards, (folder / ".price_repair.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            emit(state="busy")
            return 1
        if args.commit:
            collection_lock = guards.enter_context((folder / ".run.lock").open("a"))
            try:
                fcntl.flock(collection_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                emit(
                    state="collection_running",
                    detail="Price preview is allowed; defer DB writes until collection finishes",
                )
                return 1
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup_path = folder / f"price_before_{stamp}.jsonl"
        stats = {"selected": len(urls), "parsed": 0, "saved": 0, "failed": 0}
        # Preview creates no price backup file and never writes DB.
        with (
            backup_path.open("x", encoding="utf-8")
            if args.commit
            else nullcontext(None)
        ) as backup:
            for url in urls:
                try:
                    html, final = fetcher.fetch_page(url)
                    if canonical(final) != url:
                        raise PriceError("DETAIL_REDIRECT_REVIEW")
                    price = parse_prices(html)
                    stats["parsed"] += 1
                    state = "preview"
                    if args.commit:
                        vids = mapping.get(url, set())
                        if len(vids) != 1:
                            raise PriceError("SAVED_VARIANT_NOT_UNIQUE")
                        state = update_price(
                            url, next(iter(vids)), price["sale_krw"], backup
                        )
                        stats["saved"] += 1
                    emit(url=url, **price, state=state)
                except Exception as exc:
                    stats["failed"] += 1
                    emit(
                        url=url,
                        error=(
                            str(exc)
                            if isinstance(exc, PriceError)
                            else type(exc).__name__
                        ),
                    )
        emit(
            **stats,
            mode="COMMIT" if args.commit else "PREVIEW",
            backup=str(backup_path) if args.commit else None,
            indexed=False,
        )
        return 1 if stats["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
