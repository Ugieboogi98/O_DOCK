"""Four-store price comparison for a confirmed catalog variant."""
from datetime import timedelta, timezone
from decimal import Decimal
from urllib.parse import urlsplit

from sqlalchemy import select

from app.core.config import get_settings
from app.models.entities import now
from app.models.retail import RetailListing, RetailOffer


RETAILERS = (
    ('maniahouse', '매니아하우스', 'maniahouse.co.kr'),
    ('herotime', '히어로타임', 'herotime.co.kr'),
    ('figurefarm', '피규어팜', 'figurefarm.net'),
    ('comics_art', '코믹스아트', 'comics-art.co.kr'),
)


def aware(value):
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def summarize_offers(observations, cutoff):
    latest = {}
    for observation in observations:
        key = (observation['source'], observation['product_url'])
        previous = latest.get(key)
        if previous is None or aware(observation['observed_at']) >= aware(previous['observed_at']):
            latest[key] = observation
    rows = []
    for code, name, _ in RETAILERS:
        offers = []
        for item in latest.values():
            if item['source'] != code or item['price'] is None or item.get('conditional_price'):
                continue
            price = Decimal(str(item['price']))
            if not price.is_finite() or price <= 0 or price != price.to_integral_value():
                continue
            observed = aware(item['observed_at'])
            stale = observed < cutoff
            offers.append({**item, 'price': int(price), 'observed_at': observed.isoformat(), 'stale': stale,
                           'eligible': not stale and item['availability'] in ('IN_STOCK', 'PREORDER')})
        eligible = [offer for offer in offers if offer['eligible']]
        chosen = min(eligible, key=lambda offer: offer['price']) if eligible else max(
            offers, key=lambda offer: offer['observed_at'], default=None)
        row = {'code': code, 'name': name, 'price': None, 'product_url': None,
               'availability': None, 'observed_at': None, 'stale': False, 'eligible': False}
        if chosen:
            row.update({key: chosen[key] for key in row if key in chosen})
        rows.append(row)
    lowest = min((row['price'] for row in rows if row['eligible']), default=None)
    for row in rows:
        row['is_lowest'] = row['eligible'] and row['price'] == lowest
    return {'retailers': rows, 'lowest_price': lowest, 'currency': 'KRW',
            'available_count': sum(row['eligible'] for row in rows), 'shipping_included': False}


def domestic_comparison(db, variant_id, legacy_rows):
    observations = []
    for record in legacy_rows:
        if record.match_status != 'MATCHED' or record.currency != 'KRW':
            continue
        if record.price_type not in ('displayed', 'normal', 'discount', 'preorder'):
            continue
        host = (urlsplit(record.product_url).hostname or '').removeprefix('www.')
        code = next((code for code, name, domain in RETAILERS
                     if host == domain or record.retailer.name == name), None)
        if code:
            observations.append({'source': code, 'price': record.amount,
                'product_url': record.product_url, 'observed_at': record.observed_at,
                'availability': {'in_stock': 'IN_STOCK', 'preorder': 'PREORDER',
                                 'out_of_stock': 'SOLD_OUT', 'sold_out': 'SOLD_OUT'}.get(record.availability, 'UNKNOWN')})
    query = (select(RetailListing, RetailOffer)
             .join(RetailOffer, RetailOffer.listing_id == RetailListing.id)
             .where(RetailListing.catalog_variant_id == variant_id, RetailListing.match_status == 'MATCHED'))
    for listing, offer in db.execute(query):
        observations.append({'source': listing.source_code, 'price': offer.sale_price,
            'product_url': offer.source_url, 'observed_at': offer.observed_at,
            'availability': offer.availability, 'conditional_price': offer.conditions.get('conditional_price', False)})
    cutoff = now() - timedelta(hours=get_settings().price_max_age_hours)
    return summarize_offers(observations, cutoff)
