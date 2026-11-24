from decimal import Decimal, InvalidOperation
from app.collectors.manufacturers.base import product_json


def parse_offers(html, url):
    result = []
    for p in product_json(html):
        offers = p.get("offers", [])
        offers = [offers] if isinstance(offers, dict) else offers
        brand = p.get("manufacturer") or p.get("brand") or {}
        maker = brand.get("name") if isinstance(brand, dict) else brand
        for o in offers:
            # AggregateOffer.lowPrice is not a confirmed single-shop offer.
            if o.get("@type") == "AggregateOffer" or "price" not in o:
                continue
            try:
                amount = Decimal(str(o["price"]).replace(",", ""))
            except InvalidOperation:
                continue
            if not amount.is_finite() or amount < 0:
                continue
            status = str(o.get("availability", "")).split("/")[-1]
            result.append(
                {
                    "title": p.get("name", ""),
                    "manufacturer": maker,
                    "sku": p.get("sku"),
                    "jan_code": p.get("gtin13"),
                    "amount": str(amount),
                    "currency": o.get("priceCurrency"),
                    "product_url": url,
                    "availability": {
                        "InStock": "in_stock",
                        "PreOrder": "preorder",
                        "OutOfStock": "out_of_stock",
                        "SoldOut": "sold_out",
                    }.get(status, "unknown"),
                    "price_type": "displayed",
                    "shipping": None,
                }
            )
    return result
