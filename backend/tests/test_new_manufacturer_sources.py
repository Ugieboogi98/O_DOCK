from app.collectors.manufacturers.furyu import Adapter as FuRyu
from app.collectors.manufacturers.sega import Adapter as Sega
from app.collectors.manufacturers.bandai import Adapter as Bandai
from app.services.enrichment import extract_media


def test_furyu_new_schedule_and_product():
    adapter = FuRyu()
    html = '''<script>const jsonData = {"data":{"2026114":{"items":[
      {"name_item":"BiCute Dark Figure", "url":"https://furyuprize.com/item/22558"},
      {"name_item":"ぬいぐるみ", "url":"https://furyuprize.com/item/22559"}
    ]}}};</script>'''
    assert adapter.discover(html, 'https://furyuprize.com/') == ['https://furyuprize.com/item/22558']
    row = adapter.parse('<div class="infoblk"><h2 class="name">けいおん！</h2><h3 class="about">BiCute Dark Figureー中野梓ー</h3><span class="date">2026年11月4週</span></div>', 'https://furyuprize.com/item/22558')
    assert row['name_original'] == 'けいおん！ BiCute Dark Figureー中野梓ー'
    assert row['release_date'] == '2026-11'
    assert row['release_precision'] == 'month'


def test_sega_gigantix_title_ignores_section_heading():
    row = Sega().parse('<main><h3>プライズ</h3><h3>進撃の巨人 GigantiX ‐エレン・イェーガー‐進撃の巨人Ver.</h3></main>', 'https://segaplaza.jp/prize/D123411/')
    assert row['name_original'].startswith('進撃の巨人 GigantiX')


def test_bandai_menu_images_are_not_product_photos():
    html = '<meta property="og:image" content="/storage/images/products/main/figure.webp"><main><div class="product"><img src="/assets/img/header/item_character/thumb_gundam_series.webp"></div></main>'
    assert extract_media(html, 'https://tamashiiweb.com/item/16273/') == ['https://tamashiiweb.com/storage/images/products/main/figure.webp']


def test_bandai_prize_title_skips_empty_logo_heading():
    row = Bandai().parse('<h1 class="gHeader_logo"><img src="logo.svg"></h1><h1 class="headLine1">葬送のフリーレン フィギュア～とあるカフェのフェルン～</h1>', 'https://bsp-prize.jp/item/2845263/')
    assert row['name_original'].startswith('葬送のフリーレン')


def test_hottoys_main_photos_skip_navigation():
    html = '<img src="/image/navi_g1.jpg"><ul><li class="first"><img src="../../catalog/swfdata/ht5775/image/Corporal_Hicks-01.jpg"></li></ul>'
    assert extract_media(html, 'https://www.hottoys.jp/item/view/4570192002343.php') == ['https://www.hottoys.jp/catalog/swfdata/ht5775/image/Corporal_Hicks-01.jpg']
    assert extract_media('<img src="/catalog/swfdata/ht5774/main.jpg">', 'https://www.hottoys.jp/item/view/4895228625533.php') == ['https://www.hottoys.jp/catalog/swfdata/ht5774/main.jpg']


def test_bandai_prize_prefers_published_original_gallery():
    html = '<meta property="og:image" content="/files_thumbnail/item.jpg/500w_500h.jpg"><a href="/files/item.jpg"><img src="/files_thumbnail/item.jpg/668w_668h.jpg"></a>'
    assert extract_media(html, 'https://bsp-prize.jp/item/2845263/')[0] == 'https://bsp-prize.jp/files/item.jpg'
