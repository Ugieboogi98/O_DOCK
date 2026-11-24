"""Public catalog discovery for the bundled starter's three largest sources.
Requires explicit source_policy.json permission; never bypasses robots or login.
Only factual catalog fields are retained. Details can then be enriched with collect.py.
"""

import argparse, re, json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.collectors.safe_http import SafeFetcher
from app.models.entities import now
from app.core.database import SessionLocal
from scripts.seed import seed


def parse_catalog(html, url, manufacturer):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    if manufacturer == "Kotobukiya":
        for li in soup.select("li.productList_item"):
            a = li.select_one('a[href*="/product/detail/"]')
            name = li.select_one(".productList_title")
            category = li.select_one(".productList_category")
            kind = category.get_text(strip=True) if category else ""
            if (
                not a
                or not name
                or kind not in ["Figures", "Model Kits", "Action Figures"]
            ):
                continue
            line = li.select_one(".productList_name")
            date = li.select_one("time")
            rows.append(
                {
                    "name_original": name.get_text(" ", strip=True),
                    "official_url": urljoin(url, a["href"]),
                    "product_line": line.get_text(" ", strip=True) if line else None,
                    "type": "model_kit" if kind == "Model Kits" else "figure",
                    "release_date": (
                        date.get_text(strip=True).replace(".", "-") if date else None
                    ),
                    "release_precision": "month",
                }
            )
    elif manufacturer == "FuRyu":
        for a in soup.select('a.product-block__title-link[href*="/products/"]'):
            name = a.get_text(" ", strip=True)
            if not any(x in name for x in ["フィギュア", "TENITOL"]):
                continue
            scale = re.search(r"1/\d+", name)
            rows.append(
                {
                    "name_original": name,
                    "official_url": urljoin(url, a["href"]).split("?")[0],
                    "scale": scale[0] if scale else None,
                    "product_line": "TENITOL" if "TENITOL" in name else "F:NEX",
                }
            )
    elif manufacturer == "MegaHouse":
        for a in soup.select('a[href*="/products/item/"]'):
            text = a.get_text(" ", strip=True)
            name = text.split("発売日")[0].strip()
            date = re.search(r"(\d{4})年(\d+)月", text)
            price = re.search(r"希望小売価格：\s*([\d,]+)円", text)
            rows.append(
                {
                    "name_original": name,
                    "official_url": urljoin(url, a["href"]),
                    "release_date": f"{date[1]}-{int(date[2]):02}" if date else None,
                    "release_precision": "month",
                    "price_amount": price[1].replace(",", "") if price else None,
                    "price_kind": "official_list",
                    "currency": "JPY",
                    "tax_included": True,
                }
            )
    else:
        raise ValueError("Unsupported catalog format")
    unique = {}
    for row in rows:
        row.update(
            manufacturer=manufacturer,
            source_url=url,
            quality="catalog_metadata",
            checked_at=now().isoformat(),
        )
        row["source_text"] = "\n".join(
            f"{k}: {v}" for k, v in row.items() if v is not None
        )
        unique[row["official_url"]] = row
    return list(unique.values())


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "--manufacturer", required=True, choices=["Kotobukiya", "FuRyu", "MegaHouse"]
    )
    p.add_argument("--url", required=True)
    a = p.parse_args()
    # Domain must match the declared manufacturer; no arbitrary text can be labeled official.
    from urllib.parse import urlparse

    domains = {
        "Kotobukiya": ["www.kotobukiya.co.jp"],
        "FuRyu": ["furyu-hm.com"],
        "MegaHouse": ["megahobby.jp", "www.megahobby.jp"],
    }
    if urlparse(a.url).hostname not in domains[a.manufacturer]:
        raise SystemExit("Manufacturer/source domain mismatch")
    rows = parse_catalog(SafeFetcher().fetch(a.url), a.url, a.manufacturer)
    with SessionLocal() as db:
        print({"discovered": len(rows), "new": seed(db, rows, refresh=True)})
