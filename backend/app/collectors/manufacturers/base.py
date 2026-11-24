import json, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag


def product_json(html):
    soup = BeautifulSoup(html, "html.parser")

    def walk(obj):
        if isinstance(obj, list):
            for value in obj:
                yield from walk(value)
        elif isinstance(obj, dict):
            t = obj.get("@type", [])
            t = [t] if isinstance(t, str) else t
            if "Product" in t:
                yield obj
            if "@graph" in obj:
                yield from walk(obj["@graph"])

    for script in soup.select('script[type="application/ld+json"]'):
        try:
            yield from walk(json.loads(script.string or script.get_text()))
        except (json.JSONDecodeError, TypeError):
            continue


class ManufacturerAdapter:
    manufacturer = ""
    domains = ()
    product_pattern = ""

    def is_product_url(self, url):
        p = urlparse(url)
        if p.scheme != "https" or p.hostname not in self.domains:
            return False
        patterns = getattr(self, "product_patterns", {})
        pattern = patterns.get(p.hostname, self.product_pattern)
        target = p.path + ("?" + p.query if p.query else "")
        return bool(pattern and re.search(pattern, target))

    def discover(self, html, url):
        soup = BeautifulSoup(html, "html.parser")
        links = (urldefrag(urljoin(url, a["href"]))[0] for a in soup.select("a[href]"))
        return list(dict.fromkeys(link for link in links if self.is_product_url(link)))

    def parse(self, html, url):
        for p in product_json(html):
            brand = p.get("manufacturer") or p.get("brand") or {}
            brand = brand.get("name") if isinstance(brand, dict) else brand
            if brand and self.manufacturer.casefold() not in brand.casefold():
                continue
            row = {
                "name_original": p["name"],
                "manufacturer": self.manufacturer,
                "official_url": url,
                "sku": p.get("sku"),
                "jan_code": p.get("gtin13"),
                "quality": "jsonld_metadata",
                "specifications": {},
                "source_type": "official_metadata_extract",
            }
            offers = p.get("offers") or []
            if isinstance(offers, dict):
                offers = [offers]
            from decimal import Decimal, InvalidOperation

            values = set()
            for offer in offers:
                try:
                    amount = Decimal(str(offer.get("price", "")).replace(",", ""))
                    currency = offer.get("priceCurrency")
                    if (
                        amount.is_finite()
                        and amount > 0
                        and currency in ("JPY", "KRW", "USD", "HKD")
                    ):
                        values.add((amount, currency))
                except (InvalidOperation, TypeError, AttributeError):
                    continue
            if len(values) == 1:
                amount, currency = values.pop()
                row.update(
                    price_amount=str(amount),
                    currency=currency,
                    price_kind="official_list",
                )
            return row
        raise ValueError("NO_VERIFIED_PRODUCT_SCHEMA: selector review required")
