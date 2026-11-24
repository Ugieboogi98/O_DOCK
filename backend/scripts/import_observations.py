"""Import an authorized JSON export. All rows are validated before one atomic transaction."""

import argparse, json
from datetime import datetime, timezone
from decimal import Decimal
from typing import Literal
from urllib.parse import urlparse
from pydantic import BaseModel, Field, AnyHttpUrl, model_validator
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.entities import (
    FigureVariant,
    Retailer,
    RetailPriceRecord,
    UsedMarketplace,
    UsedListing,
    CollectionJob,
    now,
)
from app.search_agents.matching import match_product


class Observation(BaseModel):
    variant_id: int = Field(gt=0)
    kind: Literal["retail", "used"]
    source_url: AnyHttpUrl
    amount: Decimal = Field(ge=0, max_digits=14, decimal_places=2, allow_inf_nan=False)
    currency: Literal["JPY", "KRW"]
    observed_at: datetime
    candidate: dict
    rights_note: str = Field(min_length=8)
    retailer_name: str | None = None
    platform: str | None = None
    availability: Literal[
        "in_stock", "preorder", "out_of_stock", "sold_out", "unknown"
    ] = "unknown"
    price_type: Literal["displayed", "normal", "discount", "preorder"] = "displayed"
    shipping: Decimal | None = Field(
        default=None, ge=0, max_digits=14, decimal_places=2
    )
    condition: Literal[
        "unopened", "opened_good", "damaged", "no_box", "missing_parts", "unknown"
    ] = "unknown"
    listing_status: Literal["active", "sold", "unknown"] = "unknown"
    is_set: bool = False
    region: str | None = None

    @model_validator(mode="after")
    def check(self):
        if self.observed_at.tzinfo is None:
            raise ValueError("observed_at requires timezone")
        if self.observed_at > datetime.now(timezone.utc):
            raise ValueError("future observation is invalid")
        if self.kind == "retail" and (not self.retailer_name or self.currency != "KRW"):
            raise ValueError("KRW retail and retailer_name required")
        if self.kind == "used" and not self.platform:
            raise ValueError("platform required")
        return self


def import_rows(db, raw):
    rows = [Observation.model_validate(r) for r in raw]
    added = 0
    for r in rows:
        v = db.get(FigureVariant, r.variant_id)
        if not v:
            raise ValueError(f"Unknown variant {r.variant_id}")
        f = v.figure
        target = {
            "sku": v.sku,
            "jan_code": v.jan_code,
            "manufacturer": f.manufacturer.name,
            "scale": f.scale,
            "edition": v.edition,
            "reissue_no": v.reissue_no,
        }
        status = match_product(target, {**r.candidate, "is_set": r.is_set})
        url = str(r.source_url)
        if r.kind == "retail":
            seller = db.scalar(select(Retailer).where(Retailer.name == r.retailer_name))
            if not seller:
                seller = Retailer(
                    name=r.retailer_name,
                    site_url="https://" + urlparse(url).netloc,
                    seller_type="unverified",
                )
                db.add(seller)
                db.flush()
            if db.scalar(
                select(RetailPriceRecord).where(
                    RetailPriceRecord.variant_id == v.id,
                    RetailPriceRecord.product_url == url,
                    RetailPriceRecord.observed_at == r.observed_at,
                    RetailPriceRecord.price_type == r.price_type,
                )
            ):
                continue
            db.add(
                RetailPriceRecord(
                    variant_id=v.id,
                    retailer_id=seller.id,
                    price_type=r.price_type,
                    amount=r.amount,
                    currency=r.currency,
                    shipping=r.shipping,
                    availability=r.availability,
                    match_status=status,
                    product_url=url,
                    observed_at=r.observed_at,
                )
            )
        else:
            platform = db.scalar(
                select(UsedMarketplace).where(UsedMarketplace.name == r.platform)
            )
            if not platform or platform.currency != r.currency:
                raise ValueError("Unknown platform or currency mismatch")
            if db.scalar(
                select(UsedListing).where(
                    UsedListing.listing_url == url,
                    UsedListing.observed_at == r.observed_at,
                )
            ):
                continue
            db.add(
                UsedListing(
                    variant_id=v.id,
                    marketplace_id=platform.id,
                    listing_url=url,
                    asking_price=r.amount,
                    currency=r.currency,
                    condition=r.condition,
                    listing_status=r.listing_status,
                    is_set=r.is_set,
                    match_status=status,
                    region=r.region,
                    observed_at=r.observed_at,
                )
            )
        added += 1
    db.add(
        CollectionJob(
            collector="authorized_observation_import",
            status="completed",
            ended_at=now(),
            count=added,
            error_summary=json.dumps(
                {"rights_notes": list(dict.fromkeys(r.rights_note for r in rows))},
                ensure_ascii=False,
            ),
        )
    )
    db.commit()
    return added


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True)
    a = p.parse_args()
    with SessionLocal() as db:
        print({"imported": import_rows(db, json.load(open(a.file, encoding="utf-8")))})
