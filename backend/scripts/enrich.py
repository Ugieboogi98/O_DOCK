"""Refresh existing DB products incrementally, including images and translations."""

import argparse, json, time
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.collectors.safe_http import SafeFetcher
from app.services.enrichment import enrich_html, translate_name, TranslationUnavailable
from scripts.repair_assets import PROVIDER_ERRORS


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--figure-id", type=int)
    p.add_argument("--translate", action="store_true")
    p.add_argument("--translation-only", action="store_true")
    p.add_argument("--no-images", action="store_true")
    a = p.parse_args()
    fetcher = SafeFetcher()
    counts = {
        "pages": 0,
        "images_added": 0,
        "translated": 0,
        "failed": 0,
        "skipped_disabled": 0,
    }
    with SessionLocal() as db:
        query = select(Figure).order_by(Figure.id)
        if a.figure_id:
            query = query.where(Figure.id == a.figure_id)
        if a.limit > 0:
            query = query.limit(a.limit)
        figures = list(db.scalars(query))
        total = len(figures)
        for i, f in enumerate(figures, 1):
            fid = f.id
            print(f"[{i}/{total}] product {fid}: {f.name_original}", flush=True)
            if not a.translation_only:
                try:
                    from urllib.parse import urlparse

                    if not fetcher.policy.get(
                        urlparse(f.official_url).hostname, {}
                    ).get("enabled"):
                        print(
                            "SKIPPED source disabled (not a new download failure)",
                            flush=True,
                        )
                        counts["skipped_disabled"] += 1
                    else:
                        html = fetcher.fetch(f.official_url)
                        result = enrich_html(
                            db, f, f.variants[0], html, f.official_url, not a.no_images
                        )
                        counts["pages"] += 1
                        counts["images_added"] += result["images_added"]
                        print(json.dumps(result, ensure_ascii=False), flush=True)
                except Exception as exc:
                    db.rollback()
                    counts["failed"] += 1
                    print(
                        f"PAGE_FAILED {type(exc).__name__}: {str(exc)[:250]}",
                        flush=True,
                    )
            if a.translate or a.translation_only:
                try:
                    if not f.name_ko:
                        time.sleep(2)
                    result = translate_name(db, f)
                    counts["translated"] += int(result == "translated")
                    print(result, flush=True)
                except TranslationUnavailable as exc:
                    db.rollback()
                    counts["failed"] += 1
                    print(f"TRANSLATION_FAILED {exc.reason}", flush=True)
                    if exc.reason in PROVIDER_ERRORS:
                        print(
                            "TRANSLATION_STOPPED: provider configuration or quota must be resolved before retry",
                            flush=True,
                        )
                        break
                except Exception as exc:
                    db.rollback()
                    counts["failed"] += 1
                    print(f"TRANSLATION_FAILED {type(exc).__name__}", flush=True)
        print(json.dumps(counts, ensure_ascii=False), flush=True)
        return 1 if counts["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
