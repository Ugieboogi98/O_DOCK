"""Fetch, validate and cache JPY/KRW exchange rates."""
from datetime import date, timedelta, timezone
from decimal import Decimal
import httpx
from app.models.entities import ExchangeRate, now
from app.repositories.figures import serialize
FX_URL = "https://api.frankfurter.dev/v2/rate/JPY/KRW"


def fx(db, force=False):
    row = db.get(ExchangeRate, "JPY/KRW")
    error = None
    checked = row.checked_at.replace(tzinfo=timezone.utc) if row else None
    if force or not row or now() - checked > timedelta(hours=12):
        try:
            response = httpx.get(FX_URL, timeout=15)
            response.raise_for_status()
            data = response.json()
            rate = Decimal(str(data["rate"]))
            rate_date = date.fromisoformat(data["date"])
            if (
                data["base"].upper() != "JPY"
                or data["quote"].upper() != "KRW"
                or not rate.is_finite()
                or rate <= 0
                or rate_date > date.today()
            ):
                raise ValueError("invalid rate")
            if not row:
                row = ExchangeRate(pair="JPY/KRW")
                db.add(row)
            row.rate = rate
            row.rate_date = rate_date.isoformat()
            row.source_url = FX_URL
            row.checked_at = now()
            db.commit()
        except Exception:
            error = "환율 갱신 실패. 저장된 환율이 있으면 기준일과 함께 표시합니다."
    return {"rate": serialize(row) if row and row.rate else None, "error": error}
