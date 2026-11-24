import pytest

from app.collectors.manufacturers.goodsmile import GoodSmileAdapter


def test_japanese_specs_and_schema_keep_official_identity_and_price():
    html = '''<h1>ねんどろいど キャラクター</h1><section id="specification">
    <dl><dt>メーカー</dt><dd>グッドスマイルカンパニー</dd></dl>
    <dl><dt>作品名</dt><dd>作品A</dd></dl>
    <dl><dt>仕様</dt><dd>ABS＆PVC製・1/7スケール・全幅：約300mm・全高：約240mm</dd></dl></section>
    <script type="application/ld+json">{"@type":"Product","productID":"123","name":"【再販】ねんどろいど キャラクター",
    "gtin":"4571697188808","offers":{"price":"9800","priceCurrency":"JPY"}}</script>'''
    row = GoodSmileAdapter().parse(html, 'https://www.goodsmile.com/ja/product/123/title')
    assert row['manufacturer'] == 'Good Smile Company'
    assert row['official_url'] == 'https://www.goodsmile.com/ja/product/123'
    assert row['franchise'] == '作品A' and row['height_mm'] == 240 and row['scale'] == '1/7'
    assert row['jan_code'] == '4571697188808' and row['price_amount'] == '9800'


def test_partner_manufacturer_is_not_labeled_good_smile_company():
    html = '<h1>ねんどろいど</h1><section id="specification"><dl><dt>メーカー</dt><dd>グッドスマイルアーツ上海</dd></dl></section>'
    with pytest.raises(ValueError, match='OTHER_MANUFACTURER'):
        GoodSmileAdapter().parse(html, 'https://www.goodsmile.com/ja/product/123')


def test_english_specs_still_parse():
    html = '<h1>Nendoroid Example</h1><section id="specification"><dl><dt>Manufacturer</dt><dd>Good Smile Company</dd></dl><dl><dt>Specifications</dt><dd>100mm in height</dd></dl></section>'
    row = GoodSmileAdapter().parse(html, 'https://www.goodsmile.com/en/product/123/title')
    assert row['height_mm'] == 100 and row['product_line'] == 'Nendoroid'


@pytest.mark.parametrize('status', [404, 403])
def test_title_slug_fallback_only_recovers_missing_page(status):
    import httpx
    from scripts.collect_goodsmile import fetch_detail
    class Fetcher:
        calls = []
        def fetch_page(self, url):
            self.calls.append(url)
            if len(self.calls) == 1:
                response = httpx.Response(status, request=httpx.Request('GET', url))
                response.raise_for_status()
            return 'html', url
    fetcher = Fetcher()
    if status == 404:
        assert fetch_detail(fetcher, 'https://www.goodsmile.com/ja/product/123', 'BOX/再販')[0] == 'html'
        assert fetcher.calls[-1] == 'https://www.goodsmile.com/ja/product/123'
    else:
        with pytest.raises(httpx.HTTPStatusError):
            fetch_detail(fetcher, 'https://www.goodsmile.com/ja/product/123', 'BOX/再販')
        assert len(fetcher.calls) == 1
