from datetime import datetime, timedelta, timezone

from app.services.domestic_prices import summarize_offers


STAMP = datetime(2026, 11, 16, tzinfo=timezone.utc)
CUTOFF = STAMP - timedelta(days=7)


def offer(source, price, availability='IN_STOCK', **extra):
    return {'source': source, 'price': price, 'availability': availability,
            'observed_at': STAMP, 'product_url': 'https://shop.example/' + source, **extra}


def test_three_prices_return_lowest_and_keep_fourth_store_empty():
    result = summarize_offers([offer('maniahouse', 150000), offer('comics_art', 140000),
                               offer('figurefarm', 145000)], CUTOFF)
    assert result['lowest_price'] == 140000 and result['available_count'] == 3
    assert len(result['retailers']) == 4
    assert next(row for row in result['retailers'] if row['code'] == 'herotime')['price'] is None
    assert [row['code'] for row in result['retailers'] if row['is_lowest']] == ['comics_art']


def test_all_missing_and_tied_lowest_prices():
    result = summarize_offers([], CUTOFF)
    assert result['lowest_price'] is None and len(result['retailers']) == 4
    assert all(row['price'] is None for row in result['retailers'])
    result = summarize_offers([offer('maniahouse', 10000), offer('figurefarm', 10000)], CUTOFF)
    assert sum(row['is_lowest'] for row in result['retailers']) == 2


def test_preorder_included_but_soldout_stale_and_conditional_are_excluded_from_lowest():
    result = summarize_offers([
        offer('maniahouse', 15000, 'PREORDER'), offer('figurefarm', 100, 'SOLD_OUT'),
        offer('comics_art', 200, observed_at=STAMP - timedelta(days=8)),
        offer('herotime', 300, conditional_price=True)], CUTOFF)
    assert result['lowest_price'] == 15000 and result['available_count'] == 1
    assert next(row for row in result['retailers'] if row['code'] == 'figurefarm')['price'] == 100
    assert next(row for row in result['retailers'] if row['code'] == 'herotime')['price'] is None


def test_newer_soldout_observation_replaces_older_in_stock_for_same_listing():
    result = summarize_offers([offer('maniahouse', 10000, observed_at=STAMP - timedelta(hours=1)),
                               offer('maniahouse', 10000, 'SOLD_OUT')], CUTOFF)
    assert result['lowest_price'] is None
    assert result['retailers'][0]['availability'] == 'SOLD_OUT'


def test_multiple_listings_choose_lowest_eligible_and_ignore_unknown_or_zero():
    result = summarize_offers([
        offer('maniahouse', 10000), offer('maniahouse', 9000, product_url='https://shop.example/other'),
        offer('figurefarm', None), offer('comics_art', 0)], CUTOFF)
    assert result['lowest_price'] == 9000
    assert result['retailers'][0]['product_url'].endswith('/other')
