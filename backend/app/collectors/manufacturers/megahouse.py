from app.collectors.manufacturers.structured import StructuredAdapter


class Adapter(StructuredAdapter):
    manufacturer = "MegaHouse"

    domains = (
        "megahobby.jp",
        "www.megahobby.jp",
    )

    product_pattern = r"/products/item/\d+"

    title_selectors = (
        ".item_detail h1",
        ".product_detail h1",
        "h1",
        'meta[property="og:title"]',
    )
