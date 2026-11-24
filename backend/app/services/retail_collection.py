"""Atomic listing/offer upserts, with stale observations excluded from updates."""
from datetime import datetime, timezone
import hashlib
import json
from urllib.parse import urlsplit

from sqlalchemy import case, select
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from app.collectors.retailers.preview_sources import SOURCES
from app.models.entities import Retailer
from app.models.retail import RetailListing, RetailOffer, RetailOfferHistory
from app.services.collection_preferences import excluded_retail_product

def link_verified_identifier(db, listing, row):
    """Link only a unique valid JAN with agreeing maker and no variant conflicts."""
    import re
    from app.models.entities import FigureVariant
    from app.collectors.retailers.maniahouse import valid_jan
    from app.search_agents.matching import match_product, norm
    jan = row.get('jan_ean')
    if not valid_jan(jan) or row.get('has_shop_bonus') or row.get('conditional_price'):
        return False
    if re.search(r'세트|\bset\b|\d+\s*종',row.get('title_raw',''),re.I):
        return False
    variants = list(db.scalars(select(FigureVariant).where(FigureVariant.jan_code.in_([jan,jan.zfill(14),jan.lstrip('0')]))))
    if len(variants) != 1:
        return False
    variant = variants[0]
    figure = variant.figure
    maker = figure.manufacturer
    if norm(row.get('manufacturer_raw')) not in {norm(maker.name),norm(maker.name_ko)} or not row.get('manufacturer_raw'):
        return False
    target = {'jan_code':variant.jan_code,'manufacturer':maker.name,'scale':figure.scale,
              'edition':variant.edition,'reissue_no':variant.reissue_no}
    scale = re.search(r'(?<!\d)1\s*/\s*\d+',row.get('title_raw',''))
    candidate = {'jan_code':variant.jan_code,'manufacturer':maker.name,
                 'scale':re.sub(r'\s+','',scale[0]) if scale else None}
    if match_product(target,candidate) != 'MATCHED':
        return False
    listing.catalog_variant_id = variant.id
    listing.match_status = 'MATCHED'
    listing.match_evidence = {'status':'MATCHED','reason':'UNIQUE_VALID_JAN_AND_MANUFACTURER','jan_ean':jan}
    return True


def save_offer(db, source_code, row):
    if excluded_retail_product(row):
        raise ValueError('MANUFACTURER_EXCLUDED')
    source = SOURCES[source_code]
    if row.get('currency') != 'KRW':
        raise ValueError('KRW_REQUIRED')
    for field in ('sale_price', 'list_price'):
        value = row.get(field)
        if value is not None and (type(value) is not int or value < 0):
            raise ValueError('INVALID_PRICE')
    observed = datetime.fromisoformat(row['observed_at'])
    if observed.tzinfo is None or observed > datetime.now(timezone.utc):
        raise ValueError('INVALID_OBSERVATION_TIME')
    observed = observed.astimezone(timezone.utc)
    if urlsplit(row['product_url']).hostname != source['host']:
        raise ValueError('SOURCE_URL_MISMATCH')
    insert = postgres_insert if db.get_bind().dialect.name == 'postgresql' else sqlite_insert
    seller = db.scalar(select(Retailer).where(Retailer.name == source['name']))
    if seller is None:
        stmt = insert(Retailer).values(name=source['name'], site_url='https://' + source['host'], seller_type='unverified')
        db.execute(stmt.on_conflict_do_nothing(index_elements=['name']))
        seller = db.scalar(select(Retailer).where(Retailer.name == source['name']))
    existing = db.scalar(select(RetailListing.id).where(
        RetailListing.source_code == source_code,
        RetailListing.external_product_id == row['external_product_id'], RetailListing.option_key == ''))
    values = dict(retailer_id=seller.id, source_code=source_code,
                  external_product_id=row['external_product_id'], option_key='', canonical_url=row['product_url'],
                  title_raw=row['title_raw'], manufacturer_raw=row.get('manufacturer_raw'),
                  jan_ean=row.get('jan_ean'), model_code=row.get('model_code'),
                  catalog_variant_id=None, match_status=row['match']['status'], match_evidence=row['match'],
                  facts={key: value for key, value in row.items() if key not in ('match', 'observed_at')},
                  first_seen_at=observed, last_seen_at=observed)
    stmt = insert(RetailListing).values(**values)
    updates = {key: stmt.excluded[key] for key in values
               if key not in ('first_seen_at', 'source_code', 'external_product_id', 'option_key', 'catalog_variant_id')}
    confirmed_identity = (
        RetailListing.catalog_variant_id.is_not(None)
        & (RetailListing.match_status == 'MATCHED')
        & (RetailListing.title_raw == stmt.excluded.title_raw)
        & RetailListing.manufacturer_raw.is_not_distinct_from(stmt.excluded.manufacturer_raw)
        & RetailListing.jan_ean.is_not_distinct_from(stmt.excluded.jan_ean)
        & RetailListing.model_code.is_not_distinct_from(stmt.excluded.model_code)
    )
    updates['catalog_variant_id'] = case((confirmed_identity, RetailListing.catalog_variant_id), else_=None)
    updates['match_status'] = case((confirmed_identity, RetailListing.match_status), else_=stmt.excluded.match_status)
    updates['match_evidence'] = case((confirmed_identity, RetailListing.match_evidence), else_=stmt.excluded.match_evidence)
    listing_id = db.execute(stmt.on_conflict_do_update(
        index_elements=['source_code', 'external_product_id', 'option_key'], set_=updates,
        where=RetailListing.last_seen_at <= observed).returning(RetailListing.id)).scalar_one_or_none()
    if listing_id is None:
        return 'stale'
    listing = db.get(RetailListing,listing_id,populate_existing=True)
    if listing.catalog_variant_id is None:
        link_verified_identifier(db,listing,row)
    digest = hashlib.sha256(json.dumps(row, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    offer_values = dict(listing_id=listing_id, currency='KRW', list_price=row.get('list_price'),
                        sale_price=row.get('sale_price'), availability=row['availability'],
                        conditions={'has_shop_bonus': row['has_shop_bonus'],
                                    'conditional_price': row['conditional_price'],
                                    'payment_options': row['payment_options'], 'warnings': row['warnings']},
                        observed_at=observed, source_url=row['product_url'], observation_hash=digest)
    offer_stmt = insert(RetailOffer).values(**offer_values)
    db.execute(offer_stmt.on_conflict_do_update(index_elements=['listing_id'],
        set_={key: offer_stmt.excluded[key] for key in offer_values if key != 'listing_id'},
        where=RetailOffer.observed_at <= observed))
    history = insert(RetailOfferHistory).values(listing_id=listing_id, observed_at=observed, list_price=row.get('list_price'),
                                                sale_price=row.get('sale_price'), availability=row['availability'])
    db.execute(history.on_conflict_do_nothing(index_elements=['listing_id', 'observed_at']))
    return 'updated' if existing else 'inserted'
