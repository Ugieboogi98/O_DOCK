"""Repair missing images/Korean product names without recollecting product records."""

import argparse
import fcntl
import json
import time
from pathlib import Path
from urllib.parse import urlparse
from sqlalchemy import select
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import Figure, Manufacturer
from app.collectors.safe_http import SafeFetcher
from app.services.enrichment import (
    enrich_html,
    translate_name,
    image_count,
    TranslationUnavailable,
)
from app.services.catalog_ingest import retry_pending_indexes
from scripts.collect_other_makers import atomic_json, read_json, error_record

PROVIDER_ERRORS = {
    "QUOTA_EXHAUSTED",
    "AUTH_OR_PERMISSION_ERROR",
    "MODEL_OR_ENDPOINT_NOT_FOUND",
    "TRANSLATION_REQUEST_REJECTED",
    "RATE_LIMIT_EXHAUSTED",
    "PROVIDER_UNAVAILABLE",
    "RETRY_AFTER_REQUIRES_LATER_RUN",
    "LLM_API_KEY_REQUIRED",
    "TRANSLATION_REQUEST_FAILED",
}


def run(args):
    args.state_file.parent.mkdir(parents=True, exist_ok=True)
    with args.state_file.with_suffix(".lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {"state": "busy"}, 1
        return _run(args)


def _run(args):
    state = read_json(args.state_file, {"products": {}})
    records = state.setdefault("products", {})
    stats = {
        "processed": 0,
        "images_ready": 0,
        "translated": 0,
        "already_complete": 0,
        "failed_images": 0,
        "failed_translations": 0,
        "skipped_failures": 0,
        "translation_blocked": None,
    }
    images = args.mode in ("images", "both")
    translations = args.mode in ("translations", "both")
    # Translation-only work never constructs a fetcher or resolves source websites.
    fetcher = SafeFetcher() if images else None
    last_request = None
    with SessionLocal() as db:
        query = select(Figure).where(Figure.id > args.after_id).order_by(Figure.id)
        if args.figure_id:
            query = query.where(Figure.id == args.figure_id)
        if args.manufacturer:
            query = query.join(Manufacturer).where(
                Manufacturer.name == args.manufacturer
            )
        ids = list(db.scalars(query.with_only_columns(Figure.id)))
        try:
            for fid in ids:
                f = db.get(Figure, fid)
                variants = [v.id for v in f.variants]
                needs_images = images and (
                    not args.only_missing or image_count(db, variants) == 0
                )
                needs_translation = translations and not (
                    f.name_ko and f.name_ko.strip()
                )
                if not needs_images and not needs_translation:
                    stats["already_complete"] += 1
                    continue
                if args.limit and stats["processed"] >= args.limit:
                    break
                record = records.setdefault(str(fid), {})
                stats["processed"] += 1
                print(f"product {fid}", flush=True)
                if needs_images:
                    old = record.get("images", {})
                    if old.get("state") == "failed" and not args.retry_failed:
                        stats["skipped_failures"] += 1
                    else:
                        try:
                            if not variants:
                                raise ValueError("NO_PRODUCT_VARIANT")
                            # Same official-page allowlist, robots and redirects as regular collection.
                            html, final = fetcher.fetch_page(f.official_url)
                            if urlparse(final).hostname not in (
                                urlparse(f.official_url).hostname,
                            ):
                                original = (
                                    urlparse(f.official_url).hostname or ""
                                ).removeprefix("www.")
                                if (urlparse(final).hostname or "").removeprefix(
                                    "www."
                                ) != original:
                                    raise ValueError("UNEXPECTED_PAGE_REDIRECT")
                            outcome = enrich_html(
                                db,
                                f,
                                f.variants[0],
                                html,
                                final,
                                True,
                                media_only=True,
                                max_images=args.max_images or None,
                            )
                            ready = image_count(db, variants)
                            record["images"] = {
                                "state": "completed" if ready else "failed",
                                "available": ready,
                                "found": outcome["images_found"],
                                "added": outcome["images_added"],
                                "failures": outcome["image_failures"],
                            }
                            if ready:
                                stats["images_ready"] += 1
                            else:
                                stats["failed_images"] += 1
                                record["images"]["reason"] = "NO_USABLE_PRODUCT_IMAGE"
                        except Exception as exc:
                            db.rollback()
                            record["images"] = {"state": "failed", **error_record(exc)}
                            stats["failed_images"] += 1
                        atomic_json(args.state_file, state)
                if needs_translation and not stats["translation_blocked"]:
                    old = record.get("translation", {})
                    if (
                        old.get("state") == "failed"
                        and old.get("reason") not in PROVIDER_ERRORS
                        and not args.retry_failed
                    ):
                        stats["skipped_failures"] += 1
                    else:
                        if last_request is not None:
                            time.sleep(
                                max(
                                    0,
                                    args.request_interval
                                    - (time.monotonic() - last_request),
                                )
                            )
                        last_request = time.monotonic()
                        try:
                            outcome = translate_name(
                                db, f, max_retries=args.max_retries
                            )
                            record["translation"] = {"state": "completed"}
                            stats["translated"] += int(outcome == "translated")
                        except TranslationUnavailable as exc:
                            db.rollback()
                            record["translation"] = {
                                "state": "failed",
                                "reason": exc.reason,
                            }
                            stats["failed_translations"] += 1
                            if exc.reason in PROVIDER_ERRORS:
                                stats["translation_blocked"] = exc.reason
                        except Exception as exc:
                            db.rollback()
                            record["translation"] = {
                                "state": "failed",
                                **error_record(exc),
                            }
                            stats["failed_translations"] += 1
                        atomic_json(args.state_file, state)
                print(
                    json.dumps({"figure_id": fid, **record}, ensure_ascii=False),
                    flush=True,
                )
                if stats["translation_blocked"] and not images:
                    break
        except KeyboardInterrupt:
            stats["interrupted"] = True
            atomic_json(args.state_file, state)
            return stats, 130
    if translations and not args.no_index:
        stats["index_retry"] = retry_pending_indexes()
    failed = (
        stats["failed_images"]
        or stats["failed_translations"]
        or stats["skipped_failures"]
        or stats.get("index_retry", {}).get("failed")
    )
    stats["state"] = "partial" if failed else "completed"
    atomic_json(args.state_file.with_name("last_run.json"), stats)
    return stats, 1 if failed else 0


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode", choices=("images", "translations", "both"), required=True)
    p.add_argument(
        "--only-missing",
        action="store_true",
        help="Skip products with a usable image; translations always preserve existing Korean names",
    )
    p.add_argument(
        "--manufacturer", help="Exact configured manufacturer name, e.g. MegaHouse"
    )
    p.add_argument("--figure-id", type=int)
    p.add_argument("--after-id", type=int, default=0)
    p.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Number of products needing work, 0 means all",
    )
    p.add_argument(
        "--max-images",
        type=int,
        default=1,
        help="Usable images per product; 0 means no limit",
    )
    p.add_argument(
        "--request-interval",
        type=float,
        default=2,
        help="Minimum translation request spacing in seconds",
    )
    p.add_argument("--max-retries", type=int, default=3)
    p.add_argument("--retry-failed", action="store_true")
    p.add_argument(
        "--no-index",
        action="store_true",
        help="Keep durable reindex requests for later repair",
    )
    p.add_argument(
        "--state-file",
        type=Path,
        default=get_settings().media_dir / "asset_repair" / "checkpoint.json",
    )
    return p


def main():
    p = parser()
    args = p.parse_args()
    if (
        args.limit < 0
        or args.after_id < 0
        or args.max_images < 0
        or not 0 <= args.max_retries <= 5
        or not 1 <= args.request_interval <= 60
    ):
        p.error(
            "Invalid limit, ID, image count, retry count or interval (1..60 seconds)"
        )
    result, code = run(args)
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
