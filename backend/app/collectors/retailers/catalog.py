"""Public store category and pagination discovery with canonical URL identities."""
import re
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup

from app.collectors.pagination import pagination_links, PAGE_KEYS
from app.collectors.retailers import figurefarm, maniahouse
from app.collectors.retailers.preview_sources import SOURCES


CATEGORY_PATHS = {
    '/product/list.html', '/msf/msf_pd_list.html', '/msf/msf_index.html',
    '/goods/goods_index.html', '/statue/statue_index.html', '/shop/big_section.php',
}
CATEGORY_KEYS = {'cate_no', 'cno1', 'cno2', 'cno3'}
EXCLUDED_LABEL = re.compile(r'개인\s*결제|잔금\s*결제|배송비\s*결제|테스트')


def canonical_page(value, source):
    host = SOURCES[source]['host']
    aliases = {host, host.removeprefix('www.'), 'www.' + host.removeprefix('www.')}
    try:
        parsed = urlsplit(urljoin('https://' + host + '/', value))
        if (parsed.scheme != 'https' or parsed.hostname not in aliases or parsed.port not in (None, 443)
                or parsed.username or parsed.password):
            return None
    except (TypeError, ValueError):
        return None
    if parsed.path == '/' and not parsed.query:
        return 'https://' + host + '/'
    if parsed.path not in CATEGORY_PATHS:
        return None
    query = parse_qs(parsed.query)
    keys = CATEGORY_KEYS & query.keys()
    if not keys or any(not re.fullmatch(r'\d+', query[key][0]) for key in keys):
        return None
    values = {key: query[key][0] for key in keys}
    for key in PAGE_KEYS & query.keys():
        if not re.fullmatch(r'\d+', query[key][0]):
            return None
        if int(query[key][0]) > 1:
            values[key] = str(int(query[key][0]))
    return urlunsplit(('https', host, parsed.path, urlencode(sorted(values.items())), ''))


def canonical_product(value, source):
    if source == 'figurefarm':
        return figurefarm.product_url(value)
    return maniahouse.product_url(value, 'https://' + SOURCES[source]['host'])


def discover_page(html, url, source):
    root = BeautifulSoup(html, 'html.parser')
    pages, products = set(), set()
    # Product anchors can appear multiple times in the same card and across categories.
    for anchor in root.select('a[href]'):
        if EXCLUDED_LABEL.search(anchor.get_text(' ', strip=True)):
            continue
        target = urljoin(url, anchor['href'])
        product = canonical_product(target, source)
        if product:
            products.add(product)
        page = canonical_page(target, source)
        if page:
            pages.add(page)
    for target in pagination_links(html, url):
        page = canonical_page(target, source)
        if page:
            pages.add(page)
    pages.discard(canonical_page(url, source))
    return sorted(pages), sorted(products)
