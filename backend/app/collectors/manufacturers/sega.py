from app.collectors.manufacturers.structured import StructuredAdapter


class Adapter(StructuredAdapter):
    manufacturer = "SEGA"
    domains = ("segaplaza.jp",)
    product_pattern = r"^/prize/[A-Za-z]?\d+/?(?:\?.*)?$"
    title_selectors = ("main h3:not(.category)", ".itemDetail h3")

    def parse(self, html, url):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        name = next(
            (
                n
                for n in soup.select("h3")
                if any(
                    k in n.get_text() for k in ["Luminasta", "フィギュア", "FIGURIZM", "GigantiX", "XStellar", "XrossLink", "Yumemirize"]
                )
            ),
            None,
        )
        if name:
            return {
                "name_original": name.get_text(" ", strip=True),
                "manufacturer": self.manufacturer,
                "official_url": url,
                "product_line": "Luminasta" if "Luminasta" in name.get_text() else None,
                "quality": "official_metadata",
                "specifications": {},
            }
        return super().parse(html, url)
