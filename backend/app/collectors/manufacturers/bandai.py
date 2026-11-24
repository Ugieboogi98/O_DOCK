from app.collectors.manufacturers.structured import StructuredAdapter


class Adapter(StructuredAdapter):
    manufacturer = "Bandai Spirits"
    domains = ("www.bandaispirits.co.jp", "tamashiiweb.com", "bsp-prize.jp")
    product_pattern = r"^/item/\d+/?(?:\?.*)?$"
    product_patterns = {
        "tamashiiweb.com": product_pattern,
        "bsp-prize.jp": r"^/item/\d+/?(?:\?.*)?$",
        "www.bandaispirits.co.jp": r"^/products/detail\.php\?.*\b(?:product_id|id)=\d+",
    }
    title_selectors = ("h1 .itemName", "h1.headLine1", "h1", ".productName")
