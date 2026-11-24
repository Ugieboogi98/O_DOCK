"""Discover official figure detail URLs from allowed catalog listing pages.

This is a discovery-only stage: it never modifies PostgreSQL.
Use scripts.collect separately after reviewing its output file.

The configured SafeFetcher applies host/path allowlists, robots.txt and pacing.
A source_policy.json enabled flag is NOT evidence of permission; verify site terms.
"""

import argparse
import json
import re
from collections import deque
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urldefrag, urlparse

from bs4 import BeautifulSoup

from app.collectors.safe_http import CollectionDenied, SafeFetcher
from app.core.config import get_settings
from app.collectors.manufacturers import ADAPTERS


from app.collectors.pagination import canonical, pagination_links


def source_adapter(url):
    host = (urlparse(url).hostname or "").lower()
    matches = [a for a in ADAPTERS if host in a.domains]
    return matches[0] if matches else None


def can_fetch(fetcher, url):
    try:
        fetcher.validate(url)
        return True
    except (CollectionDenied, OSError, ValueError):
        return False


def read_previous(path):
    if not path.exists():
        return set()
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def main():
    p = argparse.ArgumentParser(
        description="Discover product URLs; does not touch database"
    )
    p.add_argument(
        "--start-url",
        action="append",
        required=True,
        help="Verified official catalog listing URL, repeatable",
    )
    p.add_argument("--output", default=None)
    p.add_argument("--state", default=None)
    p.add_argument(
        "--max-pages",
        type=int,
        default=100,
        help="Safety cap on catalog pages per run; re-run to continue",
    )
    p.add_argument(
        "--reset-state",
        action="store_true",
        help="Reset listing queue ONLY; existing product URL file is preserved",
    )
    args = p.parse_args()
    if args.max_pages < 1:
        p.error("--max-pages must be positive")

    fetcher = SafeFetcher()
    data_dir = get_settings().data_dir
    out = Path(args.output) if args.output else data_dir / "discovered_products.txt"
    state_path = (
        Path(args.state) if args.state else data_dir / "catalog_discovery_state.json"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    products = read_previous(out)
    done = set()
    queue = deque()
    failures = []
    if state_path.exists() and not args.reset_state:
        data = json.loads(state_path.read_text(encoding="utf-8"))
        done = set(data.get("done", []))
        queue.extend(data.get("queue", []))
        failures = data.get("failures", [])

    for url in args.start_url:
        url = canonical(url.strip())
        if not source_adapter(url):
            print(f"SKIP missing manufacturer adapter: {url}", flush=True)
            continue
        if not can_fetch(fetcher, url):
            print(f"SKIP outside enabled allowlist: {url}", flush=True)
            continue
        if url not in done and url not in queue:
            queue.append(url)

    def save():
        # Atomic replacements avoid data loss when interrupted during write.
        temp_out = out.with_name(out.name + ".tmp")
        temp_out.write_text(
            "\n".join(sorted(products)) + ("\n" if products else ""), encoding="utf-8"
        )
        temp_out.replace(out)
        state = {"done": sorted(done), "queue": list(queue), "failures": failures}
        temp_state = state_path.with_name(state_path.name + ".tmp")
        temp_state.write_text(
            json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        temp_state.replace(state_path)

    processed = 0
    try:
        while queue and processed < args.max_pages:
            url = queue.popleft()
            if url in done:
                continue
            adapter = source_adapter(url)
            if adapter is None or not can_fetch(fetcher, url):
                print(f"SKIP disallowed or unsupported listing: {url}", flush=True)
                done.add(url)
                save()
                continue
            try:
                html = fetcher.fetch(url)
                candidates = adapter.discover(html, url)
                added = 0
                for found in candidates:
                    found = canonical(found)
                    if source_adapter(found) is not adapter or not can_fetch(
                        fetcher, found
                    ):
                        continue
                    if found not in products:
                        products.add(found)
                        added += 1
                # Never cross into a different manufacturer's domain while paging.
                pages = pagination_links(html, url)
                queued = 0
                for nxt in pages:
                    if nxt == url or nxt in done or nxt in queue:
                        continue
                    if source_adapter(nxt) is not adapter or not can_fetch(
                        fetcher, nxt
                    ):
                        continue
                    queue.append(nxt)
                    queued += 1
                done.add(url)
                processed += 1
                print(
                    f"[{processed}] {adapter.manufacturer}: +{added} URLs, "
                    f"+{queued} listing pages, total={len(products)} | {url}",
                    flush=True,
                )
            except Exception as exc:
                failures.append(
                    {
                        "url": url,
                        "error_type": type(exc).__name__,
                        "message": str(exc)[:200],
                    }
                )
                # Retry failed listing URLs manually after investigating cause.
                done.add(url)
                print(f"FAILED {type(exc).__name__}: {url}", flush=True)
            save()
    except KeyboardInterrupt:
        print("Interrupted. Saving checkpoint.", flush=True)
    finally:
        save()
        print(
            json.dumps(
                {
                    "processed_pages_this_run": processed,
                    "discovered_product_urls": len(products),
                    "remaining_pages": len(queue),
                    "failed_pages": len(failures),
                    "output": str(out),
                    "state": str(state_path),
                },
                ensure_ascii=False,
                indent=2,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
