"""Collect URLs with progress and per-product commits."""

import argparse, json
from urllib.parse import urlparse
from sqlalchemy import select
from app.collectors.safe_http import SafeFetcher
from app.collectors.manufacturers import ADAPTERS
from app.core.database import SessionLocal
from app.models.entities import CollectionJob, Figure, now
from app.services.enrichment import enrich_html, translate_name
from scripts.seed import seed


def run(urls, images=False, translate=False):
    urls = list(dict.fromkeys(urls))
    fetcher = SafeFetcher()
    count = 0
    failures = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}", flush=True)
        with SessionLocal() as db:
            try:
                adapter = next(
                    a for a in ADAPTERS if urlparse(url).hostname in a.domains
                )
                html = fetcher.fetch(url)
                row = adapter.parse(html, url)
                row.update(
                    source_url=url,
                    checked_at=now().isoformat(),
                    source_text=json.dumps(row, ensure_ascii=False),
                    usage_status="personal_local",
                )
                seed(db, [row], refresh=True)
                count += 1
                f = db.scalar(
                    select(Figure).where(Figure.official_url == row["official_url"])
                )
                print(
                    json.dumps(
                        enrich_html(db, f, f.variants[0], html, url, images),
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                if translate:
                    print(translate_name(db, f), flush=True)
            except Exception as exc:
                db.rollback()
                failure = {"url": url, "error_type": type(exc).__name__}
                if hasattr(exc, "response"):
                    failure["http_status"] = exc.response.status_code
                if type(exc).__name__ == "CollectionDenied":
                    failure["reason"] = str(exc)
                failures.append(failure)
                print(json.dumps(failure), flush=True)
    with SessionLocal() as db:
        db.add(
            CollectionJob(
                collector="explicit_url_collection",
                status="partial" if failures else "completed",
                ended_at=now(),
                count=count,
                error_summary=json.dumps(failures),
            )
        )
        db.commit()
    return {"collected": count, "failures": failures}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--urls-file", required=True)
    p.add_argument("--images", action="store_true")
    p.add_argument("--translate", action="store_true")
    a = p.parse_args()
    with open(a.urls_file, encoding="utf-8-sig") as file:
        urls = [x.strip() for x in file if x.strip() and not x.lstrip().startswith("#")]
    if not urls:
        raise SystemExit(
            "URL file is empty; use scripts.enrich to process existing DB products."
        )
    print(json.dumps(run(urls, a.images, a.translate), ensure_ascii=False, indent=2))
