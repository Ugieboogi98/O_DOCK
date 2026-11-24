"""Idempotent seed import. Does not reset user observations or reissue identities."""

import json, hashlib
from datetime import datetime
from sqlalchemy import select
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import *

MAKERS = [
    ("FuRyu", "후류", "https://furyu-hm.com/"),
    ("Bandai Spirits", "반다이 스피리츠", "https://www.bandaispirits.co.jp/"),
    ("MegaHouse", "메가하우스", "https://megahobby.jp/"),
    ("Good Smile Company", "굿스마일 컴퍼니", "https://www.goodsmile.com/"),
    ("SEGA", "세가", "https://segaplaza.jp/"),
    ("Kotobukiya", "코토부키야", "https://www.kotobukiya.co.jp/"),
    ("TAITO", "타이토", "https://www.taito.co.jp/"),
    ("Hot Toys", "핫토이", "https://www.hottoys.jp/"),
]


def seed(db, rows, refresh=False, *, commit=True):
    makers = {}
    for name, ko, url in MAKERS:
        m = db.scalar(select(Manufacturer).where(Manufacturer.name == name))
        if not m:
            m = Manufacturer(name=name, name_ko=ko, official_url=url)
            db.add(m)
            db.flush()
        makers[name] = m
    count = 0
    for row in rows:
        maker = makers[row["manufacturer"]]
        line = None
        if row.get("product_line"):
            line = db.scalar(
                select(ProductLine).where(
                    ProductLine.manufacturer_id == maker.id,
                    ProductLine.name == row["product_line"],
                )
            )
            if not line:
                line = ProductLine(manufacturer_id=maker.id, name=row["product_line"])
                db.add(line)
                db.flush()
        f = db.scalar(select(Figure).where(Figure.official_url == row["official_url"]))
        if not f:
            fields = {
                k: row[k]
                for k in [
                    "name_original",
                    "name_ko",
                    "franchise",
                    "character",
                    "type",
                    "scale",
                    "height_mm",
                    "material",
                    "official_url",
                    "quality",
                ]
                if row.get(k) is not None
            }
            f = Figure(
                manufacturer_id=maker.id,
                product_line_id=line.id if line else None,
                collected_at=datetime.fromisoformat(row["checked_at"]),
                **fields
            )
            db.add(f)
            db.flush()
            count += 1
        if refresh:
            for k in [
                "name_original",
                "name_ko",
                "franchise",
                "character",
                "type",
                "scale",
                "height_mm",
                "material",
                "quality",
            ]:
                if row.get(k) is not None:
                    setattr(f, k, row[k])
            if line:
                f.product_line_id = line.id
            f.collected_at = datetime.fromisoformat(row["checked_at"])
        key = row.get("variant_key", "source-page")
        v = db.scalar(
            select(FigureVariant).where(
                FigureVariant.figure_id == f.id, FigureVariant.variant_key == key
            )
        )
        if not v:
            v = FigureVariant(
                figure_id=f.id,
                variant_key=key,
                **{
                    k: row[k]
                    for k in [
                        "sku",
                        "jan_code",
                        "edition",
                        "reissue_no",
                        "release_date",
                        "release_precision",
                    ]
                    if row.get(k) is not None
                }
            )
            db.add(v)
            db.flush()
        if refresh:
            for k in [
                "sku",
                "jan_code",
                "edition",
                "reissue_no",
                "release_date",
                "release_precision",
            ]:
                if row.get(k) is not None:
                    setattr(v, k, row[k])
        if row.get("price_amount"):
            kind = row.get("price_kind", "official_list")
            url = row["source_url"]
            p = db.scalar(
                select(ReleasePrice).where(
                    ReleasePrice.variant_id == v.id,
                    ReleasePrice.source_url == url,
                    ReleasePrice.price_kind == kind,
                )
            )
            if not p:
                db.add(
                    ReleasePrice(
                        variant_id=v.id,
                        price_amount=row["price_amount"],
                        currency=row["currency"],
                        price_kind=kind,
                        tax_included=row.get("tax_included"),
                        source_url=url,
                        checked_at=datetime.fromisoformat(row["checked_at"]),
                    )
                )
            elif refresh:
                p.price_amount = row["price_amount"]
                p.currency = row["currency"]
                p.checked_at = datetime.fromisoformat(row["checked_at"])
        if refresh:
            document = db.scalar(
                select(SourceDocument).where(
                    SourceDocument.variant_id == v.id,
                    SourceDocument.url == row["source_url"],
                )
            )
            if document:
                document.body = row["source_text"]
                document.content_hash = hashlib.sha256(
                    document.body.encode()
                ).hexdigest()
                document.collected_at = datetime.fromisoformat(row["checked_at"])
        # Stable URL document is not overwritten when re-seeding a starter snapshot.
        if not db.scalar(
            select(SourceDocument).where(
                SourceDocument.variant_id == v.id,
                SourceDocument.url == row["source_url"],
            )
        ):
            body = row["source_text"]
            db.add(
                SourceDocument(
                    variant_id=v.id,
                    title=row["name_original"] + " — 공식 메타데이터 발췌",
                    url=row["source_url"],
                    source_type="official_metadata_extract",
                    language="und",
                    body=body,
                    content_hash=hashlib.sha256(body.encode()).hexdigest(),
                    collected_at=datetime.fromisoformat(row["checked_at"]),
                )
            )
    for name, url, currency in [
        ("메루카리", "https://jp.mercari.com/", "JPY"),
        ("중고나라", "https://web.joongna.com/", "KRW"),
        ("번개장터", "https://m.bunjang.co.kr/", "KRW"),
        ("당근", "https://www.daangn.com/", "KRW"),
    ]:
        if not db.scalar(select(UsedMarketplace).where(UsedMarketplace.name == name)):
            db.add(UsedMarketplace(name=name, url=url, currency=currency))
    for name, url in [
        ("매니아하우스", "https://www.maniahouse.co.kr"),
        ("히어로타임", "https://www.herotime.co.kr"),
        ("피규어팜", "https://www.figurefarm.net"),
        ("코믹스아트", "https://www.comics-art.co.kr"),
    ]:
        if not db.scalar(select(Retailer).where(Retailer.name == name)):
            db.add(Retailer(name=name, site_url=url, seller_type="unverified"))
    db.add(
        CollectionJob(
            collector="bundled_official_metadata",
            status="completed",
            ended_at=now(),
            count=count,
        )
    )
    if commit:
        db.commit()
    return count
