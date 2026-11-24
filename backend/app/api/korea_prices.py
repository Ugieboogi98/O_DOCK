"""Bandai Korea official-site prices, with explicit variant confirmation."""

import re
from decimal import Decimal
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_admin, require_same_origin
from app.models.entities import FigureVariant, ReleasePrice, now
from app.repositories.figures import serialize
from app.collectors.safe_http import SafeFetcher

router = APIRouter(prefix="/api", tags=["korea-prices"])

class KoreaPriceInput(BaseModel):
    variant_id: int = Field(gt=0)
    source_url: str = Field(max_length=1000)
    amount: Decimal = Field(gt=0, le=999999999, decimal_places=0)
    price_kind: Literal["korea_official_sale", "korea_official_list"] = (
        "korea_official_sale"
    )
    confirmed_same_product: bool = False


class KoreaPreview(BaseModel):
    source_url: str = Field(max_length=1000)


def validate_korea(url):
    p = urlparse(url)
    if (
        p.scheme != "https"
        or p.hostname not in ("www.bnkrmall.co.kr", "bnkrmall.co.kr")
        or p.username
        or p.password
        or p.port not in (None, 443)
        or p.path != "/goods/detail.do"
        or not re.fullmatch(r"\d+", parse_qs(p.query).get("gno", [""])[0])
    ):
        raise HTTPException(
            422,
            "반다이남코코리아몰 상품 상세 URL을 입력하세요: https://www.bnkrmall.co.kr/goods/detail.do?gno=상품번호",
        )
    return url


def parse_korea(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select_one('meta[property="og:title"]')
    name = title.get("content", "") if title else ""
    from app.collectors.bnkr_prices import parse_prices

    price = parse_prices(html)
    return {"name": name, "amount": str(price["sale_krw"]), "jan_code": None}


@router.post("/korea-prices/preview", dependencies=[Depends(require_admin), Depends(require_same_origin)])
def preview(data: KoreaPreview):
    validate_korea(data.source_url)
    try:
        return parse_korea(SafeFetcher().fetch(data.source_url))
    except Exception as exc:
        raise HTTPException(
            422,
            "자동 조회 실패: "
            + type(exc).__name__
            + ". 공식 페이지에서 가격과 동일 상품 여부를 확인한 후 직접 입력하세요.",
        )


@router.post("/korea-prices", dependencies=[Depends(require_admin), Depends(require_same_origin)])
def save_price(data: KoreaPriceInput, db: Session = Depends(get_db)):
    validate_korea(data.source_url)
    variant = db.get(FigureVariant, data.variant_id)
    if not variant:
        raise HTTPException(404, "제품 버전 없음")
    if variant.figure.manufacturer.name != "Bandai Spirits":
        raise HTTPException(422, "반다이 상품만 등록할 수 있습니다.")
    if not data.confirmed_same_product:
        raise HTTPException(422, "상품명·버전·제품번호를 확인하세요.")
    row = db.scalar(
        select(ReleasePrice).where(
            ReleasePrice.variant_id == data.variant_id,
            ReleasePrice.source_url == data.source_url,
            ReleasePrice.price_kind == data.price_kind,
        )
    )
    if not row:
        row = ReleasePrice(
            variant_id=data.variant_id,
            source_url=data.source_url,
            price_kind=data.price_kind,
            currency="KRW",
        )
        db.add(row)
    row.price_amount = data.amount
    row.checked_at = now()
    db.commit()
    db.refresh(row)
    return serialize(row)


@router.delete("/korea-prices/{pid}", dependencies=[Depends(require_admin), Depends(require_same_origin)])
def delete_price(pid: int, db: Session = Depends(get_db)):
    row = db.get(ReleasePrice, pid)
    if not row or not row.price_kind.startswith("korea_official_"):
        raise HTTPException(404, "한국 공식 가격 없음")
    db.delete(row)
    db.commit()
    return {"deleted": True}
