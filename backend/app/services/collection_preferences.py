"""User exclusions apply to official sources and domestic retailer observations."""
import re
import unicodedata

DOMESTIC_SOURCES = ('maniahouse', 'herotime', 'figurefarm', 'comics_art')
EXCLUDED_MAKERS = ('Hot Toys', '핫토이', 'ホットトイズ')

def excluded_manufacturer(value):
    def normalized(text):
        return re.sub(r'[^\w]', '', unicodedata.normalize('NFKC', text or '').casefold())
    value = normalized(value)
    return any(normalized(alias) in value for alias in EXCLUDED_MAKERS)

def excluded_retail_product(row):
    return excluded_manufacturer(row.get('manufacturer_raw')) or excluded_manufacturer(row.get('title_raw'))
