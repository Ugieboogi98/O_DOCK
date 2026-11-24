import re, unicodedata
from bs4 import BeautifulSoup
from app.collectors.manufacturers.base import ManufacturerAdapter


class StructuredAdapter(ManufacturerAdapter):
    title_selectors = ()

    def parse(self, html, url):
        try:
            return super().parse(html, url)
        except ValueError:
            pass
        soup = BeautifulSoup(html, "html.parser")
        title = None
        for selector in self.title_selectors:
            node = soup.select_one(selector)

            if not node:
                continue

            # meta 태그이면 content 속성에서 제품명 추출
            if node.name == "meta":
                candidate = node.get("content", "").strip()

            # 일반 HTML 태그이면 텍스트 추출
            else:
                candidate = node.get_text(" ", strip=True)

            if candidate:
                title = candidate
                break

        if not title:
            raise ValueError("PRODUCT_TITLE_SELECTOR_NOT_FOUND")
        fields = {}
        for dt in soup.select("dt"):
            dd = dt.find_next_sibling("dd")
            if dd:
                fields[dt.get_text(" ", strip=True)] = dd.get_text(" ", strip=True)
        for tr in soup.select("tr"):
            th, td = tr.find("th"), tr.find("td")
            if th and td:
                fields[th.get_text(" ", strip=True)] = td.get_text(" ", strip=True)
        title = unicodedata.normalize("NFKC", title)
        row = {
            "name_original": title,
            "manufacturer": self.manufacturer,
            "official_url": url,
            "specifications": fields,
            "quality": "official_metadata",
        }
        if (
            fields.get("メーカー")
            and self.manufacturer == "Hot Toys"
            and fields["メーカー"] != "ホットトイズ"
        ):
            raise ValueError("OTHER_MANUFACTURER")
        material = (
            fields.get("商品素材") or fields.get("素材") or fields.get("Material")
        )
        size = (
            fields.get("商品サイズ")
            or fields.get("サイズ")
            or fields.get("製品サイズ")
            or fields.get("Size")
            or ""
        )
        height = re.search(
            r"(?:全高|高さ|height)\s*[:：]?\s*(?:約)?\s*(\d+(?:\.\d+)?)\s*(mm|cm|センチ)",
            size,
            re.I,
        )
        if height:
            row["height_mm"] = round(
                float(height[1]) * (10 if height[2] in ("cm", "センチ") else 1)
            )
        scale = re.search(
            r"1\s*/\s*\d+",
            unicodedata.normalize(
                "NFKC", fields.get("スケール") or fields.get("Scale") or title
            ),
        )
        if scale:
            row["scale"] = scale[0].replace(" ", "")
        if material:
            row["material"] = material
        row["franchise"] = (
            fields.get("登場作品") or fields.get("作品名") or fields.get("Series")
        )
        row["product_line"] = fields.get("ブランド名") or fields.get("シリーズ")
        # A displayed catalog price is deliberately not labeled the initial release price.
        amount = fields.get("メーカー希望小売価格") or fields.get("希望小売価格") or ""
        price = re.search(r"[¥￥]\s*([\d,]+)|([\d,]+)円", amount)
        if price:
            row.update(
                price_amount=(price[1] or price[2]).replace(",", ""),
                currency="JPY",
                price_kind="official_list",
                tax_included=True if "税込" in amount else None,
            )
        return row
