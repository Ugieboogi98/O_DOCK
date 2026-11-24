"""Figurefarm public product facts, scoped to the purchase form."""
import re
from urllib.parse import parse_qs, urljoin, urlsplit

from bs4 import BeautifulSoup

from app.collectors.retailers.maniahouse import amount, payment_basis, valid_jan


BASE_URL = 'https://www.figurefarm.net'


def product_url(value):
    try:
        parsed = urlsplit(urljoin(BASE_URL, value))
        if (parsed.scheme != 'https' or parsed.hostname != 'www.figurefarm.net'
                or parsed.port not in (None, 443) or parsed.username or parsed.password
                or parsed.path != '/shop/detail.php'):
            return None
    except (TypeError, ValueError):
        return None
    ident = parse_qs(parsed.query).get('pno', [''])[0]
    return BASE_URL + '/shop/detail.php?pno=' + ident.upper() if re.fullmatch(r'[a-fA-F0-9]{32}', ident) else None


def discover(html):
    root = BeautifulSoup(html, 'html.parser')
    return list(dict.fromkeys(url for node in root.select('.ff-products a[href]')
                              if (url := product_url(node['href']))))


def visible(node):
    for ancestor in [node, *node.parents]:
        style = re.sub(r'\s+', '', ancestor.get('style', '')).lower()
        if ancestor.has_attr('hidden') or 'displaynone' in ancestor.get('class', []) or 'display:none' in style:
            return False
    return True


def parse_product(html, url):
    canonical = product_url(url)
    root = BeautifulSoup(html, 'html.parser')
    form = root.select_one('#detail form[name="prdFrm"]')
    if not canonical or not form:
        raise ValueError('PRODUCT_FIELDS_MISSING')
    title_node = form.select_one('.info h3.name')
    price_node = form.select_one('.info .price .sell strong')
    if not title_node:
        raise ValueError('PRODUCT_TITLE_MISSING')
    title = title_node.get_text(' ', strip=True)
    displayed = amount(price_node.get_text(strip=True)) if price_node else None
    fields = {}
    for row in form.select('table.list tr'):
        label, value = row.select_one('th'), row.select_one('td')
        if label and value and not value.select_one('input, select'):
            fields[label.get_text(' ', strip=True)] = value.get_text(' ', strip=True)
    maker = fields.get('제조사', '')
    codes = re.findall(r'(?<!\d)\d{13}(?!\d)', maker)
    verified = list(dict.fromkeys(code for code in codes if valid_jan(code)))
    jan = verified[0] if len(verified) == 1 else None
    manufacturer = re.sub(r'(?<!\d)\d{13}(?!\d)', '', maker).strip() or None
    options = []
    price = displayed
    warnings = []
    selects = form.select('select[name^="option"]')
    for select in selects:
        for option in select.select('option[value]'):
            if not option['value']:
                continue
            name = option.get_text(' ', strip=True)
            basis = payment_basis(name)
            full_price = re.search(r'(?:전액|전체)\s*결제\s*\(([\d,]+)원\)', name)
            options.append({'title_raw': name, 'price_basis': basis,
                            'sale_price': amount(full_price.group(1)) if full_price else None,
                            'disabled': option.has_attr('disabled')})
    full = [o for o in options if o['price_basis'] == 'FULL_PAYMENT']
    if selects and (len(selects) != 1 or len(full) != 1):
        price = None
        warnings.append('OPTION_PRICE_REQUIRES_REVIEW')
    elif full and full[0]['sale_price'] != displayed:
        price = None
        warnings.append('DISPLAYED_PRICE_CONFLICT')
    controls = [node.get_text(' ', strip=True) for node in form.select('a[href*="addCart"]')
                if ',2)' in node['href'] and visible(node)]
    availability = 'UNKNOWN'
    if '품절' in controls or '판매종료' in controls or (full and full[0]['disabled']):
        availability = 'SOLD_OUT'
    elif '바로구매' in controls:
        preorder = bool(re.search(r'\[\d{2}년.*입고\]|예약', title))
        availability = 'PREORDER' if preorder else 'IN_STOCK'
    return {'external_product_id': parse_qs(urlsplit(canonical).query)['pno'][0],
            'product_url': canonical, 'title_raw': title, 'manufacturer_raw': manufacturer,
            'jan_ean': jan, 'jan_raw': ' / '.join(codes) or None, 'model_code': None,
            'currency': 'KRW', 'list_price': None, 'displayed_sale_price': displayed,
            'sale_price': price, 'availability': availability, 'payment_options': options,
            'has_shop_bonus': bool(re.search(r'샵특전|단독특전', title)),
            'conditional_price': bool(re.search(r'예약금|잔금|쿠폰|회원가', title)),
            'warnings': warnings, 'evidence': fields}
