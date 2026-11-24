"""BNKR displayed selling price; never use cart totals or list price as sale price."""

import re
from bs4 import BeautifulSoup


class PriceError(ValueError):
    pass


def numbers(nodes):
    values = set()
    for node in nodes:
        raw = node.get("value") if node.name == "input" else node.get_text(strip=True)
        if raw and re.fullmatch(r"(?:\d+|\d{1,3}(?:,\d{3})+)", raw):
            value = int(raw.replace(",", ""))
            if 0 < value <= 999999999:
                values.add(value)
    return values


def parse_prices(html):
    soup = BeautifulSoup(html, "html.parser")
    if "request rejected" in soup.get_text(" ", strip=True).lower():
        raise PriceError("REQUEST_REJECTED")
    sales = numbers(soup.select(".price_result .num"))
    if len(sales) != 1:
        raise PriceError("SALE_PRICE_MISSING" if not sales else "SALE_PRICE_AMBIGUOUS")
    sale = next(iter(sales))
    origins = numbers(soup.select(".price_origin .num, .price_origin"))
    inputs = numbers(soup.select('input[name="price"]'))
    if len(origins) > 1 or len(inputs) > 1:
        raise PriceError("ORIGIN_PRICE_AMBIGUOUS")
    if origins and inputs and origins != inputs:
        raise PriceError("ORIGIN_PRICE_CONFLICT")
    reference = origins or inputs
    origin = next(iter(reference)) if reference else None
    if origin is not None and sale > origin:
        raise PriceError("SALE_ABOVE_ORIGIN_REVIEW")
    return {"sale_krw": sale, "origin_krw": origin, "selector": ".price_result .num"}
