"""Exchange-rate and local-price read/refresh endpoints."""
from decimal import Decimal, ROUND_HALF_UP
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_admin, require_same_origin
from app.repositories.figures import serialize, get_figure
from app.models.entities import ReleasePrice
from app.services.exchange_rates import fx

router = APIRouter(prefix="/api", tags=['prices'])


@router.get("/exchange-rate")
def exchange(db: Session = Depends(get_db)):
    return fx(db)


@router.post("/exchange-rate/refresh", dependencies=[Depends(require_admin), Depends(require_same_origin)])
def refresh_exchange(db: Session = Depends(get_db)):
    return fx(db, True)


@router.get("/figures/{fid}/local-prices")
def local_prices(fid: int, variant_id: int, db: Session = Depends(get_db)):
    f = get_figure(db, fid)
    if variant_id not in [v.id for v in f.variants]:
        raise HTTPException(404, "제품 버전 없음")
    prices = list(
        db.scalars(
            select(ReleasePrice)
            .where(ReleasePrice.variant_id == variant_id)
            .order_by(ReleasePrice.checked_at.desc())
        )
    )
    jp = next((x for x in prices if x.currency == "JPY"), None)
    kr = next(
        (
            x
            for x in prices
            if x.currency == "KRW"
            and x.price_kind in ("korea_official_sale", "korea_official_list")
        ),
        None,
    )
    exchange = fx(db)
    rate = exchange["rate"]
    return {
        "korea": serialize(kr) if kr else None,
        "japan": serialize(jp) if jp else None,
        **exchange,
        "estimate_krw": (
            (jp.price_amount * rate["rate"]).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            )
            if jp and rate
            else None
        ),
    }
