"""Authenticated favorites and purchase endpoints."""
from datetime import date
from decimal import Decimal
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_same_origin
from app.repositories.figures import card, serialize, get_figure
from app.models.entities import Favorite, Purchase, Figure, FigureVariant, now
from app.services.accounts import require_user
from app.services.personal_records import save_purchase

router = APIRouter(prefix="/api", tags=['personal'])


class PurchaseInput(BaseModel):
    variant_id: int = Field(gt=0)
    amount: Decimal = Field(ge=0, le=999999999999, decimal_places=2)
    currency: Literal["KRW", "JPY", "USD"] = "KRW"
    purchased_on: date
    delivery_status: Literal["pending", "shipping", "delivered"] = "pending"
    shop: str = Field(default="", max_length=200)
    memo: str = Field(default="", max_length=2000)


@router.get("/favorites")
def favorites(db: Session = Depends(get_db), user=Depends(require_user)):
    return [
        card(f, favorite=True)
        for f in db.scalars(
            select(Figure)
            .join(Favorite, Favorite.figure_id == Figure.id)
            .where(Favorite.user_id == user.id)
            .order_by(Favorite.created_at.desc())
        )
    ]


@router.put("/favorites/{fid}", dependencies=[Depends(require_same_origin)])
def add_favorite(fid: int, db: Session = Depends(get_db), user=Depends(require_user)):
    get_figure(db, fid)
    from sqlalchemy.dialects.postgresql import insert as pg_insert
    from sqlalchemy.dialects.sqlite import insert as sqlite_insert
    insert = pg_insert if db.bind.dialect.name == 'postgresql' else sqlite_insert
    db.execute(insert(Favorite).values(figure_id=fid, user_id=user.id, created_at=now())
               .on_conflict_do_nothing(index_elements=['figure_id', 'user_id']))
    db.commit()
    return {"favorite": True}


@router.delete("/favorites/{fid}", dependencies=[Depends(require_same_origin)])
def remove_favorite(fid: int, db: Session = Depends(get_db), user=Depends(require_user)):
    row = db.get(Favorite, (fid, user.id))
    if row:
        db.delete(row)
        db.commit()
    return {"favorite": False}


@router.get("/purchases")
def purchases(db: Session = Depends(get_db), user=Depends(require_user)):
    return [
        {
            **serialize(p),
            "figure_id": f.id,
            "name": f.name_ko or f.name_original,
            "edition": v.edition or v.variant_key,
        }
        for p, v, f in db.execute(
            select(Purchase, FigureVariant, Figure)
            .join(FigureVariant, Purchase.variant_id == FigureVariant.id)
            .join(Figure, FigureVariant.figure_id == Figure.id)
            .where(Purchase.user_id == user.id)
            .order_by(Purchase.id.desc())
        )
    ]


@router.post("/purchases", dependencies=[Depends(require_same_origin)])
def create_purchase(data: PurchaseInput, db: Session = Depends(get_db), user=Depends(require_user)):
    return save_purchase(db, data, user.id)


@router.put("/purchases/{pid}", dependencies=[Depends(require_same_origin)])
def update_purchase(pid: int, data: PurchaseInput, db: Session = Depends(get_db), user=Depends(require_user)):
    row = db.scalar(select(Purchase).where(Purchase.id == pid, Purchase.user_id == user.id))
    if not row:
        raise HTTPException(404, "구매 기록 없음")
    return save_purchase(db, data, user.id, row)


@router.delete("/purchases/{pid}", dependencies=[Depends(require_same_origin)])
def delete_purchase(pid: int, db: Session = Depends(get_db), user=Depends(require_user)):
    row = db.scalar(select(Purchase).where(Purchase.id == pid, Purchase.user_id == user.id))
    if not row:
        raise HTTPException(404, "구매 기록 없음")
    db.delete(row)
    db.commit()
    return {"deleted": True}
