import json

import httpx
import pytest

from app.collectors.retailers.maniahouse import discover, parse_product, valid_jan
from app.collectors.safe_http import CollectionDenied
from scripts.preview_domestic_prices import PreviewFetcher


URL = 'https://maniahouse.co.kr/product/detail.html?product_no=26604'


def page(options, title='[예약판매] 샵특전 블랑', price='239,100원', jan='6927254807350'):
    data = {'@type': 'ProductGroup', 'hasVariant': [
        {'name': title + ' ' + name, 'offers': {'@type': 'Offer', 'priceCurrency': 'KRW',
         'price': value, 'availability': 'https://schema.org/' + status, 'url': URL}}
        for name, value, status in options]}
    return ('<div class="xans-product-detail"><table>'
            f'<tr><th>상품명</th><td>{title}</td></tr>'
            '<tr><th>제조사</th><td>Good Smile Arts Shanghai</td></tr>'
            f'<tr><th>JAN</th><td>{jan}</td></tr><tr><th>판매가</th><td>{price}</td></tr>'
            '</table></div><script type="application/ld+json">' + json.dumps(data) + '</script>')


def test_full_payment_beats_deposit_and_balance():
    row = parse_product(page([('예약금', 30000, 'InStock'), ('잔금', 209100, 'OutOfStock'),
                              ('전액결제', 239100, 'InStock')]), URL)
    assert row['sale_price'] == 239100
    assert row['availability'] == 'PREORDER'
    assert row['has_shop_bonus'] and len(row['payment_options']) == 3
    assert row['jan_ean'] == '6927254807350' and row['model_code'] is None


def test_deposit_only_and_option_ranges_are_not_general_prices():
    row = parse_product(page([('예약금', 30000, 'InStock')]), URL)
    assert row['sale_price'] is None
    assert row['availability'] == 'UNKNOWN'
    assert 'OPTION_PRICE_REQUIRES_REVIEW' in row['warnings']
    row = parse_product(page([('A', 10000, 'InStock'), ('B', 20000, 'InStock')]), URL)
    assert row['sale_price'] is None


def test_full_payment_sold_out_wins_over_preorder_title():
    row = parse_product(page([('전액결제', 239100, 'OutOfStock')]), URL)
    assert row['availability'] == 'SOLD_OUT'


def test_discount_reference_and_price_conflict_and_bad_jan():
    html = page([('전액결제', 239100, 'InStock')], jan='6927254807351')
    html = html.replace('</table>', '<tr><th>소비자가</th><td>300,000원</td></tr></table>')
    row = parse_product(html, URL)
    assert row['list_price'] == 300000 and row['jan_ean'] is None
    assert 'INVALID_JAN' in row['warnings']
    assert not valid_jan('7350')
    row = parse_product(page([('전액결제', 200000, 'InStock')]), URL)
    assert row['sale_price'] is None and 'DISPLAYED_PRICE_CONFLICT' in row['warnings']


def test_url_aliases_deduplicate_and_reject_foreign_pages():
    html = (f'<a href="{URL}&amp;cate_no=1">A</a>'
            '<a href="/product/title/26604/category/45/">B</a>'
            '<a href="https://evil.example/product/detail.html?product_no=26604">C</a>')
    html += '<a href="/product/title/26604/45/">D</a>'
    html += '<a href="https://maniahouse.co.kr:bad/product/detail.html?product_no=1">E</a>'
    assert discover(html) == [URL]


@pytest.mark.parametrize('status', [403, 429, 302])
def test_preview_stops_immediately_without_retries(monkeypatch, status):
    calls = []
    original_client = httpx.Client
    def respond(request):
        calls.append(request)
        return httpx.Response(status)
    monkeypatch.setattr(httpx, 'Client', lambda **kwargs: original_client(transport=httpx.MockTransport(respond)))
    fetcher = PreviewFetcher()
    monkeypatch.setattr(fetcher, 'validate', lambda url: ('maniahouse.co.kr', {}))
    monkeypatch.setattr(fetcher, 'check_robots', lambda *args: None)
    monkeypatch.setattr(fetcher, '_pace', lambda *args: None)
    with pytest.raises(CollectionDenied, match='HTTP_' + str(status)):
        fetcher.fetch(URL)
    assert len(calls) == 1
