from collections import defaultdict
from datetime import timedelta
from statistics import median
from sqlalchemy import select
from app.core.config import get_settings
from app.models.entities import ReleasePrice, RetailPriceRecord, UsedListing, now
from app.repositories.figures import serialize
from app.services.domestic_prices import domestic_comparison


def latest(rows, key):
    result = {}
    for r in sorted(rows, key=lambda r: r.observed_at):
        result[key(r)] = r
    return list(result.values())


def price_summary(db, variant_id):
    release = list(
        db.scalars(select(ReleasePrice).where(ReleasePrice.variant_id == variant_id))
    )
    rows = latest(
        db.scalars(
            select(RetailPriceRecord).where(RetailPriceRecord.variant_id == variant_id)
        ).all(),
        lambda x: (x.product_url, x.price_type),
    )
    cutoff = now() - timedelta(hours=get_settings().price_max_age_hours)
    valid = [
        r
        for r in rows
        if r.match_status == "MATCHED"
        and r.currency == "KRW"
        and r.availability == "in_stock"
        and r.observed_at >= cutoff
    ]
    return {
        "domestic_comparison": domestic_comparison(db, variant_id, rows),
        "release_prices": [serialize(x) for x in release],
        "japan_release_price": next(
            (
                serialize(x)
                for x in release
                if x.currency == "JPY" and x.price_kind == "official_release"
            ),
            None,
        ),
        "retail_prices": [
            {
                **serialize(x),
                "retailer": x.retailer.name,
                "stale": x.observed_at < cutoff,
            }
            for x in rows
        ],
        "lowest_verified_krw": min((x.amount for x in valid), default=None),
        "shipping_included": False,
        "note": "배송비 제외 · 동일 버전 일치 및 판매 중인 최근 관측만 집계. 전체 시장 최저가 보장 아님.",
    }


def used_summary(db, variant_id):
    rows = latest(
        db.scalars(
            select(UsedListing).where(UsedListing.variant_id == variant_id)
        ).all(),
        lambda x: x.listing_url,
    )
    cutoff = now() - timedelta(hours=get_settings().price_max_age_hours)
    groups = defaultdict(list)
    for r in rows:
        if r.match_status == "MATCHED" and not r.is_set and r.observed_at >= cutoff:
            groups[
                (r.marketplace.name, r.currency, r.condition, r.listing_status)
            ].append(r.asking_price)
    stats = []
    for (platform, currency, condition, status), values in groups.items():
        stats.append(
            {
                "platform": platform,
                "currency": currency,
                "condition": condition,
                "status": status,
                "count": len(values),
                "median": median(values) if len(values) >= 3 else None,
                "min": min(values),
                "max": max(values),
                "note": (
                    "표본 부족"
                    if len(values) < 3
                    else "판매 희망가 통계; 검증된 실거래가 아님"
                ),
            }
        )
    return {
        "listings": [
            {
                **serialize(r),
                "platform": r.marketplace.name,
                "stale": r.observed_at < cutoff,
            }
            for r in rows
        ],
        "statistics": stats,
        "note": "통화·상태·플랫폼·판매 상태별 분리. 국제배송·대행료·세금 제외.",
    }
