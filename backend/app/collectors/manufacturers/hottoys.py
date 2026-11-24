from app.collectors.manufacturers.structured import StructuredAdapter


class Adapter(StructuredAdapter):
    manufacturer = "Hot Toys"
    domains = ("www.hottoys.jp", "www.hottoys.com.hk")
    product_pattern = r"^/item/view/\d+(?:\.php)?/?(?:\?.*)?$"
    product_patterns = {
        "www.hottoys.jp": product_pattern,
        "www.hottoys.com.hk": r"^/productDetail\.php\?.*\bproductID=\d+",
    }
    title_selectors = ("h1",)
