from app.collectors.manufacturers.structured import StructuredAdapter


class Adapter(StructuredAdapter):
    manufacturer = "TAITO"
    domains = ("www.taito.co.jp",)
    product_pattern = r"^/(?:en/)?taito-prize/\d+/?(?:\?.*)?$"
    title_selectors = ("h2.prize-detail-title",)
