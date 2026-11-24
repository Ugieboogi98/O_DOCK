"""Read collected domestic prices, including listings awaiting catalog matches."""
from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.models.entities import Retailer
from app.models.retail import RetailListing, RetailOffer


router = APIRouter(prefix='/api', tags=['retail-offers'])


@router.get('/retail-offers')
def list_offers(source: Literal['', 'maniahouse', 'herotime', 'comics_art', 'figurefarm'] = '',
                q: str = Query('', max_length=120), jan: str = Query('', max_length=30),
                availability: Literal['', 'IN_STOCK', 'PREORDER', 'SOLD_OUT', 'COMING_SOON', 'UNKNOWN'] = '',
                page: int = Query(1, ge=1), size: int = Query(30, ge=1, le=100),
                db: Session = Depends(get_db)):
    query = (select(RetailListing, RetailOffer, Retailer.name)
             .join(RetailOffer, RetailOffer.listing_id == RetailListing.id)
             .join(Retailer, Retailer.id == RetailListing.retailer_id))
    if source:
        query = query.where(RetailListing.source_code == source)
    if q.strip():
        query = query.where(RetailListing.title_raw.icontains(q.strip(), autoescape=True))
    if jan:
        query = query.where(RetailListing.jan_ean == jan)
    if availability:
        query = query.where(RetailOffer.availability == availability)
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    rows = db.execute(query.order_by(RetailOffer.observed_at.desc(), RetailListing.id.desc())
                      .offset((page - 1) * size).limit(size))
    cutoff = datetime.now(timezone.utc) - timedelta(hours=get_settings().price_max_age_hours)
    items = []
    for listing, offer, name in rows:
        observed = offer.observed_at
        if observed.tzinfo is None:
            observed = observed.replace(tzinfo=timezone.utc)
        items.append({'id': listing.id, 'retailer': name, 'source': listing.source_code,
                      'external_product_id': listing.external_product_id, 'title': listing.title_raw,
                      'manufacturer': listing.manufacturer_raw, 'jan_ean': listing.jan_ean,
                      'catalog_variant_id': listing.catalog_variant_id, 'match_status': listing.match_status,
                      'currency': offer.currency, 'sale_price': offer.sale_price, 'list_price': offer.list_price,
                      'availability': offer.availability, 'conditions': offer.conditions,
                      'product_url': offer.source_url, 'observed_at': observed.isoformat(),
                      'stale': observed < cutoff})
    return {'items': items, 'total': total, 'page': page, 'size': size}
