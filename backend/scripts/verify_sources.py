"""Read-only enabled-source smoke test. No DB access or policy changes."""

import argparse
import hashlib
import json
from pathlib import Path
from app.collectors.safe_http import SafeFetcher
from app.services.catalog_ingest import adapter_for
from scripts.collect_other_makers import CONFIG, WORKDIR, atomic_json, error_record
from scripts.discover_catalogs_all import pagination_links


def verify(config, fetcher):
    reports = []
    for item in config["sources"]:
        report = {
            "manufacturer": item["manufacturer"],
            "enabled": item.get("enabled", False),
            "pages": [],
        }
        reports.append(report)
        if not item.get("enabled"):
            report.update(state="disabled", reason=item.get("note"))
            continue
        for url in item.get("start_urls", []):
            record = {"url": url}
            report["pages"].append(record)
            try:
                html, final = fetcher.fetch_page(url)
                adapter = adapter_for(final)
                if adapter is None or adapter.manufacturer != item["manufacturer"]:
                    raise ValueError("ADAPTER_MISMATCH")
                links = adapter.discover(html, final)
                record.update(
                    final_url=final,
                    product_links=len(links),
                    pagination_links=len(pagination_links(html, final)),
                    html_sha256=hashlib.sha256(html.encode()).hexdigest(),
                )
                if not links:
                    raise ValueError("NO_PRODUCT_LINKS_REVIEW_HTML_OR_JS")
                product_html, product_url = fetcher.fetch_page(links[0])
                if adapter_for(
                    product_url
                ) is not adapter or not adapter.is_product_url(product_url):
                    raise ValueError("PRODUCT_REDIRECT_MISMATCH")
                row = adapter.parse(product_html, product_url)
                record.update(
                    sample_url=product_url,
                    sample_fields={
                        k: v
                        for k, v in row.items()
                        if k not in ("specifications", "source_text")
                    },
                    state="verified",
                )
            except Exception as exc:
                record.update(state="failed", **error_record(exc))
        report["state"] = (
            "verified"
            if report["pages"]
            and all(x["state"] == "verified" for x in report["pages"])
            else "failed"
        )
    return reports


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, default=CONFIG)
    p.add_argument("--output", type=Path, default=WORKDIR / "source_verification.json")
    a = p.parse_args()
    result = verify(json.loads(a.config.read_text(encoding="utf-8-sig")), SafeFetcher())
    atomic_json(a.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    enabled = [x for x in result if x["enabled"]]
    return 0 if enabled and all(x["state"] == "verified" for x in enabled) else 1


if __name__ == "__main__":
    raise SystemExit(main())
