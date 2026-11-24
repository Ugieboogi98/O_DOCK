"""Read collected domestic prices, including listings awaiting catalog matches."""
from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import require_admin, require_same_origin
from app.models.entities import Figure, FigureVariant, Retailer
from app.models.retail import RetailListing, RetailOffer, RetailOfferHistory
from app.services.semantic_neighbors import NgramIndex


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


def _iso(value):
    return (value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value).isoformat()


@router.get('/figures/{fid}/price-history')
def price_history(fid: int, days: int = Query(180, ge=1, le=730), variant_id: int | None = None,
                  db: Session = Depends(get_db)):
    """Observed domestic prices per store over time, for linked listings only."""
    variants = select(FigureVariant.id).where(FigureVariant.figure_id == fid)
    if variant_id is not None:
        variants = variants.where(FigureVariant.id == variant_id)
    since = datetime.now(timezone.utc) - timedelta(days=days)
    rows = db.execute(
        select(RetailListing.id, RetailListing.source_code, Retailer.name, RetailOfferHistory)
        .join(RetailOfferHistory, RetailOfferHistory.listing_id == RetailListing.id)
        .join(Retailer, Retailer.id == RetailListing.retailer_id)
        .where(RetailListing.catalog_variant_id.in_(variants), RetailOfferHistory.observed_at >= since)
        .order_by(RetailListing.id, RetailOfferHistory.observed_at))
    series = {}
    for listing_id, source, name, point in rows:
        entry = series.setdefault(listing_id, {'listing_id': listing_id, 'source': source, 'retailer': name, 'points': []})
        entry['points'].append({'observed_at': _iso(point.observed_at), 'sale_price': point.sale_price,
                                'list_price': point.list_price, 'availability': point.availability})
    prices = [p['sale_price'] for s in series.values() for p in s['points'] if p['sale_price']]
    return {'figure_id': fid, 'days': days, 'series': list(series.values()),
            'lowest_observed': min(prices) if prices else None}


# ----- Admin review queue for listings the automatic JAN matcher could not link -----

_candidate_index = {'key': None, 'index': None}


def _figure_index(db):
    key = db.execute(select(func.count(Figure.id), func.max(Figure.id))).one()
    if _candidate_index['key'] != tuple(key):
        examples = [{'figure_id': fid, 'name_original': ' '.join(x for x in (original, ko) if x)}
                    for fid, original, ko in db.execute(select(Figure.id, Figure.name_original, Figure.name_ko))]
        _candidate_index.update(key=tuple(key), index=NgramIndex(examples))
    return _candidate_index['index']


def _variant_options(db, figure_ids):
    rows = db.execute(select(FigureVariant.id, FigureVariant.figure_id, FigureVariant.jan_code, FigureVariant.edition,
                             Figure.name_original, Figure.name_ko)
                      .join(Figure, Figure.id == FigureVariant.figure_id).where(FigureVariant.figure_id.in_(figure_ids)))
    return [{'variant_id': v, 'figure_id': f, 'jan_code': jan, 'edition': edition, 'name_original': original, 'name_ko': ko}
            for v, f, jan, edition, original, ko in rows]


@router.get('/admin/retail-matches', dependencies=[Depends(require_admin)])
def unmatched_listings(source: Literal['', 'maniahouse', 'herotime', 'comics_art', 'figurefarm'] = '',
                       page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=50), db: Session = Depends(get_db)):
    query = select(RetailListing).where(RetailListing.catalog_variant_id.is_(None))
    if source:
        query = query.where(RetailListing.source_code == source)
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    listings = list(db.scalars(query.order_by(RetailListing.last_seen_at.desc(), RetailListing.id.desc())
                               .offset((page - 1) * size).limit(size)))
    index = _figure_index(db) if listings else None
    items = []
    for listing in listings:
        similar = index.similar(listing.title_raw or '', 5, min_score=0.15, exclude_title=False)
        by_jan = []
        if listing.jan_ean:
            by_jan = list(db.scalars(select(FigureVariant.figure_id).where(FigureVariant.jan_code == listing.jan_ean)))
        ids = list(dict.fromkeys([*by_jan, *(s['figure_id'] for s in similar)]))
        scores = {s['figure_id']: s['similarity'] for s in similar}
        options = _variant_options(db, ids) if ids else []
        for option in options:
            option['similarity'] = scores.get(option['figure_id'])
            option['jan_match'] = bool(listing.jan_ean and option['jan_code'] == listing.jan_ean)
        options.sort(key=lambda o: (not o['jan_match'], -(o['similarity'] or 0)))
        items.append({'listing_id': listing.id, 'source': listing.source_code, 'title': listing.title_raw,
                      'manufacturer': listing.manufacturer_raw, 'jan_ean': listing.jan_ean,
                      'match_status': listing.match_status, 'match_evidence': listing.match_evidence,
                      'url': listing.canonical_url, 'candidates': options[:8]})
    return {'items': items, 'total': total, 'page': page, 'size': size}


class ManualMatch(BaseModel):
    model_config = ConfigDict(extra='forbid')
    variant_id: int = Field(ge=1)


@router.post('/admin/retail-matches/{listing_id}', dependencies=[Depends(require_admin), Depends(require_same_origin)])
def confirm_match(listing_id: int, data: ManualMatch, db: Session = Depends(get_db)):
    listing = db.get(RetailListing, listing_id)
    variant = db.get(FigureVariant, data.variant_id)
    if listing is None or variant is None:
        raise HTTPException(404, '판매 기록 또는 상품 판본을 찾을 수 없습니다.')
    # 'MATCHED' is kept by later observations as long as the listing's identity fields stay the same.
    listing.catalog_variant_id = variant.id
    listing.match_status = 'MATCHED'
    listing.match_evidence = {'status': 'MATCHED', 'reason': 'ADMIN_CONFIRMED', 'variant_id': variant.id,
                              'confirmed_at': datetime.now(timezone.utc).isoformat()}
    db.commit()
    return {'listing_id': listing.id, 'catalog_variant_id': variant.id, 'match_status': listing.match_status}


@router.delete('/admin/retail-matches/{listing_id}', dependencies=[Depends(require_admin), Depends(require_same_origin)])
def remove_match(listing_id: int, db: Session = Depends(get_db)):
    listing = db.get(RetailListing, listing_id)
    if listing is None:
        raise HTTPException(404, '판매 기록을 찾을 수 없습니다.')
    listing.catalog_variant_id = None
    listing.match_status = 'UNMATCHED'
    listing.match_evidence = {'status': 'UNMATCHED', 'reason': 'ADMIN_REMOVED',
                              'removed_at': datetime.now(timezone.utc).isoformat()}
    db.commit()
    return {'listing_id': listing.id, 'catalog_variant_id': None, 'match_status': listing.match_status}
