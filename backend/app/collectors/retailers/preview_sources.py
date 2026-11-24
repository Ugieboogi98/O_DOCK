"""Explicitly requested stores for one-time public previews."""
from functools import partial

from app.collectors.retailers import figurefarm, maniahouse


SOURCES = {
    'herotime': {
        'name': '히어로타임', 'url': 'https://www.herotime.co.kr/',
        'host': 'www.herotime.co.kr', 'paths': ['/', '/product/'],
        'max_html_bytes': 8_000_000,
        'discover': partial(maniahouse.discover, base='https://www.herotime.co.kr'),
        'parse': partial(maniahouse.parse_product, base='https://www.herotime.co.kr'),
    },
    'maniahouse': {
        'name': '매니아하우스', 'url': maniahouse.LIST_URL,
        'host': 'maniahouse.co.kr', 'paths': ['/product/'],
        'discover': maniahouse.discover, 'parse': maniahouse.parse_product,
    },
    'comics_art': {
        'name': '코믹스아트', 'url': 'https://comics-art.co.kr/',
        'host': 'comics-art.co.kr', 'paths': ['/', '/product/'],
        'discover': partial(maniahouse.discover, base='https://comics-art.co.kr'),
        'parse': partial(maniahouse.parse_product, base='https://comics-art.co.kr'),
    },
    'figurefarm': {
        'name': '피규어팜', 'url': figurefarm.BASE_URL + '/',
        'host': 'www.figurefarm.net', 'paths': ['/', '/shop/detail.php'],
        'discover': figurefarm.discover, 'parse': figurefarm.parse_product,
    },
}
