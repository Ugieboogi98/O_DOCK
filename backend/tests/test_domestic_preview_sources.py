import json
from datetime import date

from app.collectors.retailers import figurefarm, maniahouse
from app.collectors.safe_http import CollectionDenied
from scripts import preview_domestic_prices as preview


FARM_URL = 'https://www.figurefarm.net/shop/detail.php?pno=606FEC164FBB88E0D5775CD55852E6A8'


def farm_page(options='', purchase='바로구매'):
    return f'''<div id="detail"><form name="prdFrm"><div class="info">
    <h3 class="name">[27년5월입고] 원피스 나미</h3><div class="price"><span class="sell"><strong>221,000</strong>원</span></div>
    <table class="list"><tr><th>제조사</th><td>메가하우스 4535123716737</td></tr></table>
    {options}<a href="javascript:addCart(document.prdFrm,2)">{purchase}</a>
    <span style="display:none">품절</span></div></form></div>'''


def test_comics_fields_and_full_payment_alias():
    base = 'https://comics-art.co.kr'
    url = base + '/product/detail.html?product_no=269758'
    group = {'@type': 'ProductGroup', 'hasVariant': [
        {'name': '도로시 ' + label, 'offers': {'@type': 'Offer', 'priceCurrency': 'KRW',
         'price': value, 'url': url, 'availability': 'https://schema.org/InStock'}}
        for label, value in [('1차결제', 41000), ('전체결제', 277000)]]}
    html = '''<div class="infoArea"><div class="headingArea"><h2>도로시 세렌디피티</h2></div>
    <li><div class="disnoul_left"><span>판매가</span> :</div><div class="disnoul_right">277,000원</div></li>
    <li><div class="disnoul_left"><span>JAN CODE</span></div><div class="disnoul_right">6927254804571</div></li>
    <li><div class="disnoul_left"><span>발매</span></div><div class="disnoul_right">2099년 12월</div></li>
    </div><script type="application/ld+json">''' + json.dumps(group) + '</script>'
    row = maniahouse.parse_product(html, url, base)
    assert row['sale_price'] == 277000 and row['jan_ean'] == '6927254804571'
    assert row['availability'] == 'PREORDER'
    assert row['payment_options'][0]['price_basis'] == 'DEPOSIT'
    assert maniahouse.product_url('https://maniahouse.co.kr/product/detail.html?product_no=269758', base) is None


def test_future_release_year_month_and_quarter():
    today = date(2026, 11, 16)
    assert maniahouse.future_release('27년 4분기', today)
    assert maniahouse.future_release('2026년 12월', today)
    assert not maniahouse.future_release('26년 4분기', today)
    assert not maniahouse.future_release('2025년 12월', today)
    assert not maniahouse.future_release('확인 중', today)


def test_farm_form_scope_payment_and_jan():
    options = '''<select name="option1"><option value="">선택</option>
    <option value="deposit">예약금(50,000원)</option>
    <option value="balance" disabled>잔금결제(171,000원) (품절)</option>
    <option value="full">전액결제(221,000원)</option></select>'''
    row = figurefarm.parse_product(farm_page(options), FARM_URL)
    assert row['sale_price'] == 221000 and row['availability'] == 'PREORDER'
    assert row['jan_ean'] == '4535123716737' and row['manufacturer_raw'] == '메가하우스'
    assert '수량' not in row['evidence']


def test_farm_soldout_and_ambiguous_options():
    row = figurefarm.parse_product(farm_page(purchase='품절'), FARM_URL)
    assert row['availability'] == 'SOLD_OUT'
    row = figurefarm.parse_product(farm_page('<select name="option1"><option value="a">색상 A</option></select>'), FARM_URL)
    assert row['sale_price'] is None and 'OPTION_PRICE_REQUIRES_REVIEW' in row['warnings']


def test_farm_discovery_excludes_banners_and_deduplicates_tracking():
    html = f'<a href="{FARM_URL}">배너</a><div class="ff-products"><a href="{FARM_URL}&amp;rURL=unused">A</a><a href="{FARM_URL}">B</a></div>'
    assert figurefarm.discover(html) == [FARM_URL]
    assert figurefarm.product_url(FARM_URL.replace('www.figurefarm.net', 'evil.example')) is None


def test_source_failure_is_recorded_and_next_source_can_run(tmp_path, monkeypatch):
    class BlockedFetcher:
        requests = 1
        def __init__(self, name):
            self.name = name
        def fetch(self, url):
            raise CollectionDenied('HTTP_403')
    monkeypatch.setattr(preview, 'PreviewFetcher', BlockedFetcher)
    report = {'sources': {}, 'items': [], 'errors': []}
    output = tmp_path / 'preview.json'
    for name in ('comics_art', 'figurefarm'):
        result = preview.collect_source(name, 5, report, output)
        assert result['state'] == 'stopped' and result['parsed'] == 0
    assert len(report['sources']) == 2 and len(report['errors']) == 2
    assert json.loads(output.read_text())['errors'][1]['source'] == 'figurefarm'
