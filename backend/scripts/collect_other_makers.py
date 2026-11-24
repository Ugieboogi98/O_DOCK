"""Bounded sequential official catalog importer; checkpoints live on media_data."""

from __future__ import annotations
import argparse
import fcntl
import json
import re
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urldefrag
from app.collectors.safe_http import SafeFetcher
from app.core.config import get_settings
from app.services.catalog_ingest import (
    adapter_for,
    collect_one as _collect_one,
    retry_pending_indexes,
)
from scripts.discover_catalogs_all import pagination_links

WORKDIR = get_settings().media_dir / "maker_catalogs"
CONFIG = get_settings().data_dir / "other_makers_sources.json"


def normalized(url):
    return urldefrag(url.strip())[0]


def read_json(path, default):
    return (
        json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else default
    )


def atomic_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(path)


def atomic_lines(path, values):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text("".join(url + "\n" for url in sorted(values)), encoding="utf-8")
    tmp.replace(path)


def error_record(exc):
    result = {"error": type(exc).__name__}
    if type(exc).__name__ == "CollectionDenied":
        result["reason"] = str(exc)
    if getattr(exc, "response", None) is not None:
        result["http_status"] = exc.response.status_code
    return result


def valid(fetcher, url):
    try:
        fetcher.validate(url)
        return True
    except Exception:
        return False


def is_product_url(url, adapter):
    return adapter.is_product_url(url)


def source_job(
    name,
    start_urls,
    fetcher,
    max_pages,
    max_new,
    commit,
    reset_state,
    retry_failed,
    workdir,
    refresh_catalog=False,
):
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    folder = workdir / slug
    folder.mkdir(parents=True, exist_ok=True)
    # Nonblocking OS lock is released by the kernel on interruption/container exit.
    with (folder / ".run.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {"manufacturer": name, "state": "busy"}
        return _source_job(
            name,
            start_urls,
            fetcher,
            max_pages,
            max_new,
            commit,
            reset_state,
            retry_failed,
            folder,
            refresh_catalog,
        )


def _source_job(
    name,
    start_urls,
    fetcher,
    max_pages,
    max_new,
    commit,
    reset_state,
    retry_failed,
    folder,
    refresh_catalog,
):
    state_file, urls_file = folder / "checkpoint.json", folder / "product_urls.txt"
    state = {} if reset_state else read_json(state_file, {})
    done = set(state.get("done", []))
    queue = deque(state.get("queue", []))
    failures = dict(state.get("failed_products", {}))
    failed_pages = list(state.get("failed_pages", []))
    products = (
        set(urls_file.read_text(encoding="utf-8").splitlines())
        if urls_file.exists()
        else set()
    )
    products.discard("")
    # Successful DB identities are still checked by the DB; no metadata is overwritten.
    if refresh_catalog:
        done.clear()
    if retry_failed:
        for record in failed_pages:
            page = record.get("url")
            if page and page not in queue:
                done.discard(page)
                queue.append(page)
        failed_pages = []
    for start in start_urls:
        start = normalized(start)
        a = adapter_for(start)
        if not a or a.manufacturer != name:
            raise ValueError("START_URL_ADAPTER_MISMATCH")
        failed_starts = {x.get("url") for x in failed_pages}
        if (
            start not in done
            and start not in queue
            and (start not in failed_starts or retry_failed or refresh_catalog)
        ):
            queue.append(start)
    stats = {
        "manufacturer": name,
        "checked_pages": 0,
        "discovered_new_urls": 0,
        "new_db_products": 0,
        "existing_db_products": 0,
        "failed_products": 0,
        "index_pending": 0,
        "mode": "COMMIT" if commit else "DISCOVERY_ONLY",
    }

    def persist():
        atomic_lines(urls_file, products)
        pending_pages = list(queue)
        if (
            current_page
            and current_page not in done
            and current_page not in pending_pages
        ):
            pending_pages.insert(0, current_page)
        atomic_json(
            state_file,
            {
                "done": sorted(done),
                "queue": pending_pages,
                "failed_pages": failed_pages,
                "failed_products": failures,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
        )

    attempted = set()

    def ingest(url):
        a = adapter_for(url)
        if (
            not commit
            or url in attempted
            or not a
            or a.manufacturer != name
            or not a.is_product_url(url)
            or stats["new_db_products"] >= max_new
            or (
                url in failures
                and not retry_failed
                and not (
                    isinstance(failures[url], dict)
                    and failures[url].get("error") == "INDEX_PENDING"
                )
            )
        ):
            return
        attempted.add(url)
        try:
            fetcher.validate(url)
            result = _collect_one(fetcher, url)
            if result in ("created", "created_index_pending"):
                stats["new_db_products"] += 1
            elif result in ("existing", "existing_index_pending"):
                stats["existing_db_products"] += 1
            else:
                raise ValueError("UNEXPECTED_INGEST_RESULT")
            if result in ("created_index_pending", "existing_index_pending"):
                stats["index_pending"] += 1
                failures[url] = {"error": "INDEX_PENDING"}
            else:
                failures.pop(url, None)
        except Exception as exc:
            stats["failed_products"] += 1
            failures[url] = error_record(exc)
        # Critical: checkpoint after EVERY ingested saved URL as well as discovered URLs.
        persist()

    current_page = None
    try:
        if commit:
            for url in sorted(products):
                if stats["new_db_products"] >= max_new:
                    break
                ingest(url)
        attempts = 0
        while (
            queue
            and attempts < max_pages
            and (not commit or stats["new_db_products"] < max_new)
        ):
            current_page = queue.popleft()
            if current_page in done:
                current_page = None
                continue
            attempts += 1  # Failed page attempts also consume the bound.
            a = adapter_for(current_page)
            try:
                if a is None or a.manufacturer != name:
                    raise ValueError("PAGE_ADAPTER_MISMATCH")
                html, final_url = (
                    fetcher.fetch_page(current_page)
                    if hasattr(fetcher, "fetch_page")
                    else (fetcher.fetch(current_page), current_page)
                )
                if adapter_for(final_url) is not a:
                    raise ValueError("CATALOG_REDIRECT_HOST_MISMATCH")
                urls = [normalized(x) for x in a.discover(html, final_url)]
                stats["checked_pages"] += 1
                if not urls:
                    raise ValueError("NO_PRODUCT_LINKS_REVIEW_HTML_OR_JS")
                for url in urls:
                    if (
                        adapter_for(url) is a
                        and a.is_product_url(url)
                        and valid(fetcher, url)
                    ):
                        if url not in products:
                            products.add(url)
                            stats["discovered_new_urls"] += 1
                # Save ALL discovered URLs before spending the per-run product budget.
                persist()
                for url in urls:
                    if url in products:
                        ingest(url)
                    if commit and stats["new_db_products"] >= max_new:
                        break
                for nxt in pagination_links(html, final_url):
                    nxt = normalized(nxt)
                    n = urlparse(nxt)
                    approved = any(
                        n.hostname == urlparse(s).hostname
                        and (
                            n.path == urlparse(s).path
                            or n.path.startswith(urlparse(s).path.rstrip("/") + "/")
                        )
                        for s in start_urls
                    )
                    if (
                        approved
                        and adapter_for(nxt) is a
                        and nxt not in done
                        and nxt not in queue
                    ):
                        queue.append(nxt)
                done.add(current_page)
            except Exception as exc:
                failed_pages.append({"url": current_page, **error_record(exc)})
            current_page = None
            persist()
    except KeyboardInterrupt:
        if current_page and current_page not in done:
            queue.appendleft(current_page)
        stats["interrupted"] = True
        raise
    finally:
        persist()
        stats.update(
            discovered_total=len(products),
            remaining_pages=len(queue),
            stored_failed_products=len(failures),
            failed_page_count=len(failed_pages),
        )
        stats["state"] = "partial" if failures or failed_pages else "completed"
        atomic_json(folder / "last_run.json", stats)
    return stats


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, default=CONFIG)
    p.add_argument("--manufacturer", action="append")
    p.add_argument(
        "--max-pages", type=int, default=3, help="Page attempts per maker per run"
    )
    p.add_argument(
        "--max-new", type=int, default=30, help="New products per maker per run"
    )
    p.add_argument("--commit", action="store_true")
    p.add_argument(
        "--reset-state",
        action="store_true",
        help="Reset page checkpoint, retain URL file and DB",
    )
    p.add_argument(
        "--refresh-catalog",
        action="store_true",
        help="Rescan catalog for newly released products",
    )
    p.add_argument("--retry-failed", action="store_true")
    p.add_argument("--workdir", type=Path, default=WORKDIR)
    p.add_argument(
        "--retry-index-only",
        action="store_true",
        help="Repair pending Chroma jobs without fetching websites",
    )
    args = p.parse_args()
    if args.max_pages < 1 or args.max_new < 1:
        p.error("--max-pages and --max-new must be positive")
    if args.retry_index_only:
        result = retry_pending_indexes()
        print(json.dumps(result))
        return 1 if result["failed"] else 0
    config = read_json(args.config, None)
    if not isinstance(config, dict) or not isinstance(config.get("sources"), list):
        p.error("Missing or invalid source configuration")
    names = {x.get("manufacturer") for x in config["sources"]}
    if args.manufacturer and set(args.manufacturer) - names:
        p.error("Unknown manufacturer name")
    fetcher = SafeFetcher()
    summary = []
    index_summary = retry_pending_indexes() if args.commit else {"failed": 0}
    for item in config["sources"]:
        name = item.get("manufacturer")
        if args.manufacturer and name not in args.manufacturer:
            continue
        if not item.get("enabled"):
            print(f'SKIP {name}: {item.get("note", "disabled")}', flush=True)
            continue
        urls = [x.strip() for x in item.get("start_urls", []) if x.strip()]
        if not urls:
            summary.append({"manufacturer": name, "state": "invalid_config"})
            continue
        try:
            result = source_job(
                name,
                urls,
                fetcher,
                args.max_pages,
                args.max_new,
                args.commit,
                args.reset_state,
                args.retry_failed,
                args.workdir,
                args.refresh_catalog,
            )
        except KeyboardInterrupt:
            return 130
        except Exception as exc:
            result = {"manufacturer": name, "state": "failed", **error_record(exc)}
        summary.append(result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    atomic_json(
        args.workdir / "last_summary.json",
        {"sources": summary, "index_retry": index_summary},
    )
    print("SUMMARY", json.dumps(summary, ensure_ascii=False), flush=True)
    if not summary:
        print(
            "NO_ENABLED_SOURCES: no collection performed; see docs/HANDOVER.md",
            flush=True,
        )
        return 2
    return (
        1
        if index_summary["failed"] or any(s["state"] != "completed" for s in summary)
        else 0
    )


if __name__ == "__main__":
    raise SystemExit(main())
