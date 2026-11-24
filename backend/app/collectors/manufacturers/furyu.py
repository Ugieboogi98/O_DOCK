"""FuRyu Shopify HTML: verified product identity and factual specification cells."""

import re
import json
import unicodedata
from decimal import Decimal, InvalidOperation
from bs4 import BeautifulSoup
from app.collectors.manufacturers.structured import StructuredAdapter
from app.collectors.manufacturers.base import product_json


class Adapter(StructuredAdapter):
    manufacturer = "FuRyu"
    domains = ("furyu-hm.com", "furyuprize.com")
    product_pattern = r"^/products/[^/?]+/?(?:\?.*)?$"
    product_patterns = {
        "furyu-hm.com": product_pattern,
        "furyuprize.com": r"^/(?:prize/[^/?]+|item/\d+)/?(?:\?.*)?$",
    }
    title_selectors = (
        "h1.product-title",
        "h1.product__title",
        ".product-title h1",
        "h1",
    )

    def discover(self, html, url):
        urls = super().discover(html, url)
        match = re.search(r'const\s+jsonData\s*=\s*', html)
        if match and 'furyuprize.com' in url:
            data, _ = json.JSONDecoder().raw_decode(html[match.end():])
            for week in data.get('data', {}).values():
                for item in week.get('items', []):
                    if any(k in item.get('name_item', '') for k in ('フィギュア', 'Figure')) and self.is_product_url(item.get('url', '')):
                        urls.append(item['url'])
        return list(dict.fromkeys(urls))

    def parse(self, html, url):
        if "furyu-hm.com" not in url:
            soup = BeautifulSoup(html, 'html.parser')
            work, name = soup.select_one('h2.name'), soup.select_one('h3.about')
            if work and name:
                row = {'manufacturer': self.manufacturer, 'official_url': url,
                       'name_original': work.get_text(' ', strip=True) + ' ' + name.get_text(' ', strip=True),
                       'franchise': work.get_text(' ', strip=True), 'quality': 'official_metadata', 'specifications': {}}
                date = soup.select_one('.infoblk .date')
                if date:
                    row['specifications']['release_week'] = date.get_text(' ', strip=True)
                    match = re.search(r'(\d{4})年(\d{1,2})月', date.get_text())
                    if match:
                        row.update(release_date=f'{match[1]}-{int(match[2]):02d}', release_precision='month')
                return row
            return super().parse(html, url)
        soup = BeautifulSoup(html, "html.parser")
        fields = {}
        for node in soup.select(".tw-table-row"):
            cells = node.select(":scope > .tw-table-cell")
            if len(cells) == 2:
                fields[cells[0].get_text(" ", strip=True).strip("【】")] = cells[
                    1
                ].get_text(" ", strip=True)
        # Store only our maker's own products; a store's brand name is not its manufacturer.
        if fields.get("発売元") not in ("フリュー株式会社", "フリュー"):
            raise ValueError("OTHER_OR_UNVERIFIED_MANUFACTURER")
        title = fields.get("商品名")
        if not title:
            raise ValueError("PRODUCT_TITLE_SELECTOR_NOT_FOUND")
        row = {
            "name_original": unicodedata.normalize("NFKC", title),
            "manufacturer": self.manufacturer,
            "official_url": url,
            "specifications": {
                k: fields[k]
                for k in (
                    "作品名",
                    "商品サイズ",
                    "仕様",
                    "SKU",
                    "お届け時期",
                    "ブランド",
                    "発売元",
                )
                if k in fields
            },
            "quality": "official_metadata",
            "franchise": fields.get("作品名"),
            "sku": fields.get("SKU"),
            "product_line": fields.get("ブランド"),
        }
        scale = re.search(r"1/\d+", row["name_original"])
        if scale:
            row["scale"] = scale[0]
        size = unicodedata.normalize("NFKC", fields.get("商品サイズ", ""))
        height = re.search(r"全高\s*[:：]?\s*約?\s*(\d+(?:\.\d+)?)\s*(mm|cm)", size)
        if height:
            row["height_mm"] = round(
                float(height[1]) * (10 if height[2] == "cm" else 1)
            )
        spec = fields.get("仕様", "")
        materials = [
            x for x in ("PVC", "ABS", "プラスチック", "ポリエステル") if x in spec
        ]
        if materials:
            row["material"] = " / ".join(materials)
        delivery = fields.get("お届け時期", "")
        date = re.fullmatch(
            r"\s*(\d{4})年(\d{1,2})月\s*(?:発送予定|発売予定)?\s*", delivery
        )
        if date and 1 <= int(date[2]) <= 12:
            row.update(
                release_date=f"{date[1]}-{int(date[2]):02d}", release_precision="month"
            )
        for product in product_json(html):
            # Require agreement with the visible product rather than unrelated JSON-LD.
            if product.get("sku") != row.get("sku"):
                continue
            jan = str(product.get("gtin13") or "")
            if re.fullmatch(r"\d{13}", jan):
                row["jan_code"] = jan
            offers = product.get("offers", [])
            if isinstance(offers, dict):
                offers = [offers]
            for offer in offers:
                if offer.get("priceCurrency") != "JPY":
                    continue
                try:
                    amount = Decimal(str(offer.get("price", "")).replace(",", ""))
                except InvalidOperation:
                    continue
                if amount.is_finite() and amount > 0:
                    row.update(
                        price_amount=str(amount),
                        currency="JPY",
                        price_kind="official_list",
                    )
                    break
        return row
