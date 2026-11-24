"""Public Maniahouse product facts and payment options for a bounded preview."""
import json
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import parse_qs, urljoin, urlsplit

from bs4 import BeautifulSoup


BASE_URL = 'https://maniahouse.co.kr'
LIST_URL = BASE_URL + '/product/list.html?cate_no=45'


def product_url(value, base=BASE_URL):
    try:
        parsed = urlsplit(urljoin(base, value))
        port = parsed.port
    except (TypeError, ValueError):
        return None
    hostname = urlsplit(base).hostname
    hosts = {hostname, hostname.removeprefix('www.'), 'www.' + hostname.removeprefix('www.')}
    if (parsed.scheme != 'https' or parsed.hostname not in hosts
            or parsed.username or parsed.password or port not in (None, 443)):
        return None
    ident = parse_qs(parsed.query).get('product_no', [''])[0] if parsed.path == '/product/detail.html' else ''
    if not ident:
        match = re.fullmatch(r'/product/[^/]+/(\d+)(?:/(?:category|display)/\d+|/\d+)*/?', parsed.path)
        ident = match.group(1) if match else ''
    return base + '/product/detail.html?product_no=' + ident if re.fullmatch(r'\d+', ident) else None


def discover(html, base=BASE_URL):
    root = BeautifulSoup(html, 'html.parser')
    return list(dict.fromkeys(url for node in root.select('a[href]')
                              if (url := product_url(node['href'], base))))


def amount(value):
    text = str(value or '').strip()
    if not re.fullmatch(r'(?:\d+|\d{1,3}(?:,\d{3})+)(?:\s*원)?', text):
        return None
    return int(re.sub(r'[,\s원]', '', text))


def valid_jan(value):
    if not re.fullmatch(r'\d{13}', value or ''):
        return False
    return sum(int(n) * (1 if i % 2 == 0 else 3) for i, n in enumerate(value)) % 10 == 0


def payment_basis(name):
    if re.search(r'전액\s*결제|전체\s*결제', name):
        return 'FULL_PAYMENT'
    if re.search(r'예약금|1차\s*결제|계약금', name):
        return 'DEPOSIT'
    if re.search(r'잔금|2차\s*결제', name):
        return 'BALANCE'
    return 'OPTION'


def future_release(value, today=None):
    today = today or datetime.now(ZoneInfo('Asia/Seoul')).date()
    match = re.search(r'(?<!\d)(\d{2}|20\d{2})년\s*(?:(\d{1,2})월|(\d)분기)?', value or '')
    if not match:
        return False
    year = int(match.group(1))
    if year < 100:
        year += 2000
    if year != today.year:
        return year > today.year
    month = None
    if match.group(2):
        month = int(match.group(2))
    elif match.group(3):
        month = (int(match.group(3)) - 1) * 3 + 1
    return month is not None and 1 <= month <= 12 and month > today.month


def parse_product(html, url, base=BASE_URL):
    canonical = product_url(url, base)
    if not canonical:
        raise ValueError('INVALID_PRODUCT_URL')
    root = BeautifulSoup(html, 'html.parser')
    fields = {}
    for row in root.select('.xans-product-detail tr'):
        label, value = row.select_one('th'), row.select_one('td')
        if label and value:
            fields[label.get_text(' ', strip=True)] = value.get_text(' ', strip=True)
    for row in root.select('.infoArea li'):
        label, value = row.select_one('.disnoul_left span'), row.select_one('.disnoul_right')
        if label and value:
            fields[label.get_text(' ', strip=True)] = value.get_text(' ', strip=True)
    heading = root.select_one('.infoArea .headingArea h2')
    title = fields.get('상품명') or (heading.get_text(' ', strip=True) if heading else None)
    if not title:
        raise ValueError('PRODUCT_FIELDS_MISSING')
    listed_price = amount(fields.get('판매가'))
    jan = re.sub(r'\s+', '', fields.get('JAN') or fields.get('JAN코드') or fields.get('JAN CODE') or '')
    options = []
    for script in root.select('script[type="application/ld+json"]'):
        try:
            document = json.loads(script.get_text())
        except (ValueError, TypeError):
            continue
        documents = document if isinstance(document, list) else [document]
        for product in documents:
            if not isinstance(product, dict):
                continue
            variants = product.get('hasVariant') if product.get('@type') == 'ProductGroup' else [product]
            if not isinstance(variants, list):
                continue
            for variant in variants[:20]:
                if not isinstance(variant, dict):
                    continue
                offers = variant.get('offers', [])
                offers = [offers] if isinstance(offers, dict) else offers
                for offer in offers if isinstance(offers, list) else []:
                    if not isinstance(offer, dict) or offer.get('@type') == 'AggregateOffer':
                        continue
                    if offer.get('priceCurrency') != 'KRW' or product_url(offer.get('url', canonical), base) != canonical:
                        continue
                    name = variant.get('name') or title
                    basis = payment_basis(name)
                    options.append({'title_raw': name, 'sale_price': amount(offer.get('price')),
                                    'price_basis': basis, 'availability_raw': offer.get('availability', ''),
                                    'seller_sku': variant.get('sku')})
    full = [o for o in options if o['price_basis'] == 'FULL_PAYMENT']
    selectable = full or (options if len(options) == 1 and options[0]['price_basis'] == 'OPTION' else [])
    warnings = []
    selected = selectable[0] if len(selectable) == 1 else None
    price = selected['sale_price'] if selected else listed_price if not options else None
    if options and not selected:
        warnings.append('OPTION_PRICE_REQUIRES_REVIEW')
    if selected and listed_price is not None and selected['sale_price'] != listed_price:
        price = None
        warnings.append('DISPLAYED_PRICE_CONFLICT')
    availability = 'UNKNOWN'
    if selected:
        state = selected['availability_raw'].rsplit('/', 1)[-1]
        if state in ('OutOfStock', 'SoldOut'):
            availability = 'SOLD_OUT'
        elif state == 'PreOrder' or (state == 'InStock' and ('예약' in title or future_release(fields.get('발매')))):
            availability = 'PREORDER'
        elif state == 'InStock':
            availability = 'IN_STOCK'
    if not selected and '[품절]' in title:
        availability = 'SOLD_OUT'
    if availability == 'UNKNOWN' and re.search(r'판매예정|예약예정', title):
        availability = 'COMING_SOON'
    if jan and not valid_jan(jan):
        warnings.append('INVALID_JAN')
    return {'external_product_id': parse_qs(urlsplit(canonical).query)['product_no'][0],
            'product_url': canonical, 'title_raw': title, 'manufacturer_raw': fields.get('제조사'),
            'jan_ean': jan if valid_jan(jan) else None, 'jan_raw': jan or None,
            'model_code': fields.get('모델명') or fields.get('모델번호'),
            'currency': 'KRW', 'list_price': amount(fields.get('소비자가') or fields.get('정가')),
            'displayed_sale_price': listed_price, 'sale_price': price,
            'availability': availability, 'payment_options': options,
            'has_shop_bonus': bool(re.search(r'샵특전|MH특전|단독특전', title)),
            'conditional_price': bool(re.search(r'예약금|잔금|쿠폰|회원가', title)),
            'warnings': warnings, 'evidence': fields}
