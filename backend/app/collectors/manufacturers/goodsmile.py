import re, json
import unicodedata
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from app.collectors.manufacturers.base import ManufacturerAdapter


class GoodSmileAdapter(ManufacturerAdapter):
    manufacturer = "Good Smile Company"
    domains = ("www.goodsmile.com",)
    product_pattern = r"/product/\d+"

    def parse(self, html, url):
        soup = BeautifulSoup(html, "html.parser")
        fields = {}
        for dl in soup.select("#specification dl"):
            dt, dd = dl.find("dt"), dl.find("dd")
            if dt and dd:
                fields[dt.get_text(" ", strip=True)] = dd.get_text(" ", strip=True)
        if (fields.get("Manufacturer") or fields.get("メーカー")) not in ("Good Smile Company", "グッドスマイルカンパニー"):
            raise ValueError("OTHER_MANUFACTURER")
        title = soup.find("h1")
        if not title:
            raise ValueError("NO_TITLE")
        spec = unicodedata.normalize('NFKC', fields.get("Specifications") or fields.get("仕様", ""))
        height = (re.search(r"全高[:：]?\s*約?\s*(\d+(?:\.\d+)?)\s*mm", spec)
                  or re.search(r"(\d+(?:\.\d+)?)\s*mm\s*(?:in height|tall)", spec, re.I))
        scale = re.search(r"1/\d+", spec)
        product_id = re.search(r'/product/(\d+)', urlsplit(url).path)
        language = 'ja' if '/ja/' in urlsplit(url).path else 'en'
        name = title.get_text(" ", strip=True)
        row = {
            "name_original": title.get_text(" ", strip=True),
            "manufacturer": self.manufacturer,
            "official_url": f'https://www.goodsmile.com/{language}/product/{product_id[1]}',
            "franchise": fields.get("Series") or fields.get("作品名"),
            "scale": scale[0] if scale else None,
            "height_mm": int(float(height[1])) if height else None,
            "material": " / ".join(
                x
                for x in ("PVC", "ABS", "POM", "PS", "ATBC-PVC")
                if re.search(r"\b" + x + r"\b", spec)
            )
            or None,
            "product_line": (
                "Nendoroid"
                if "Nendoroid" in name or "ねんどろいど" in name
                else "POP UP PARADE" if "POP UP PARADE" in title.get_text() else None
            ),
            "specifications": fields,
            "quality": "official_metadata",
            "source_type": "official_metadata_extract",
        }
        from app.collectors.manufacturers.base import product_json
        for product in product_json(html):
            if str(product.get('productID', '')) != product_id[1] and product.get('name') != name:
                continue
            jan = str(product.get('gtin13') or product.get('gtin') or '')
            if re.fullmatch(r'\d{8}|\d{12,14}', jan):
                row['jan_code'] = jan
            offers = product.get('offers') or []
            offers = [offers] if isinstance(offers, dict) else offers
            prices = {(str(o.get('price')), o.get('priceCurrency')) for o in offers if isinstance(o, dict)}
            if len(prices) == 1:
                amount, currency = prices.pop()
                if currency == 'JPY' and re.fullmatch(r'\d+(?:\.\d+)?', amount):
                    row.update(price_amount=amount, currency=currency, price_kind='official_list', tax_included=True)
            row['description'] = product.get('description')
            break
        return row
