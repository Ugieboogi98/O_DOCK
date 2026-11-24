"""Purchase validation and persistence, independent of HTTP route registration."""
from datetime import date
from fastapi import HTTPException
from app.models.entities import FigureVariant, Purchase
from app.repositories.figures import serialize


def save_purchase(db, data, user_id, row=None):
    if not db.get(FigureVariant, data.variant_id):
        raise HTTPException(404, "제품 버전 없음")
    if data.purchased_on > date.today():
        raise HTTPException(422, "구매일은 미래일 수 없습니다.")
    values = data.model_dump()
    values["purchased_on"] = data.purchased_on.isoformat()
    if row:
        for k, v in values.items():
            setattr(row, k, v)
    else:
        row = Purchase(**values, user_id=user_id)
        db.add(row)
    db.commit()
    db.refresh(row)
    return serialize(row)
