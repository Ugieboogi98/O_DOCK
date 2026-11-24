from app.collectors.manufacturers.structured import StructuredAdapter


class Adapter(StructuredAdapter):
    manufacturer = "Kotobukiya"
    domains = ("www.kotobukiya.co.jp",)
    product_pattern = r"^/(?:en/)?product/detail/[^/?]+/?(?:\?.*)?$"
    title_selectors = ("h1.productDetail_title", "h1.productTitle", "main h1", "h1")
