"""Collect up to N new FuRyu products, then fill their product images.

Run in the existing backend container as ``python -m scripts.collect_furyu_with_images``.
Uses the catalog checkpoint and the image repairer's own checkpoint; never
starts translation and never restarts the backend service.
"""

import argparse
import fcntl
import json
from pathlib import Path
from types import SimpleNamespace

from app.collectors.safe_http import SafeFetcher
from app.core.config import get_settings
from scripts.collect_other_makers import CONFIG, WORKDIR, read_json, source_job
from scripts.repair_assets import run as repair_images


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-new",
        type=int,
        default=100,
        help="Maximum new database products in this run (default: 100)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=20,
        help="Maximum listing pages checked in this run (default: 20)",
    )
    parser.add_argument(
        "--max-images",
        type=int,
        default=10,
        help="Maximum usable images per product (default: 10)",
    )
    parser.add_argument(
        "--refresh-catalog",
        action="store_true",
        help="Scan listing pages again to find recently added products",
    )
    parser.add_argument(
        "--retry-failed-images",
        action="store_true",
        help="Retry image failures recorded by an earlier run",
    )
    args = parser.parse_args()
    if min(args.max_new, args.max_pages, args.max_images) < 1:
        parser.error("All maximum values must be positive")

    config = read_json(CONFIG, None)
    if not isinstance(config, dict) or not isinstance(config.get("sources"), list):
        parser.error("FuRyu source configuration is missing")
    source = next(
        (s for s in config["sources"] if s.get("manufacturer") == "FuRyu"), None
    )
    if not source or not source.get("enabled") or not source.get("start_urls"):
        parser.error("FuRyu catalog is not enabled or has no start URL")

    lock_path = get_settings().media_dir / ".locks" / "furyu-product-images.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print(
                json.dumps(
                    {"state": "busy", "detail": "A FuRyu collection is already running"}
                )
            )
            return 1

        # This stage persists each product/URL and skips existing product IDs.
        print("PHASE 1/2: FuRyu product information", flush=True)
        metadata = source_job(
            "FuRyu",
            source["start_urls"],
            SafeFetcher(),
            args.max_pages,
            args.max_new,
            True,
            False,
            False,
            WORKDIR,
            args.refresh_catalog,
        )
        print(
            json.dumps({"product_collection": metadata}, ensure_ascii=False), flush=True
        )
        if metadata.get("state") in ("busy", "failed", "invalid_config"):
            return 1

        # Include the initial 76 FuRyu products and products saved on previous
        # interrupted runs. An existing single cover does not skip its gallery.
        print("PHASE 2/2: FuRyu product images", flush=True)
        image_args = SimpleNamespace(
            mode="images",
            only_missing=False,
            manufacturer="FuRyu",
            figure_id=None,
            after_id=0,
            limit=0,
            max_images=args.max_images,
            max_retries=0,
            request_interval=2,
            no_index=True,
            retry_failed=args.retry_failed_images,
            state_file=get_settings().media_dir / "asset_repair" / "checkpoint.json",
        )
        images, image_code = repair_images(image_args)
        print(json.dumps({"image_collection": images}, ensure_ascii=False), flush=True)
        return image_code


if __name__ == "__main__":
    raise SystemExit(main())
