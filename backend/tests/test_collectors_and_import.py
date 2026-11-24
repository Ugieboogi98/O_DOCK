import json
from datetime import timedelta
import pytest
from sqlalchemy import select, func
from app.models.entities import *
from app.collectors.manufacturers.bandai import Adapter
from app.collectors.manufacturers.hottoys import Adapter as HotToys
from scripts.import_observations import import_rows


def test_nested_product_specs_parse():
    html = "<h1>S.H.Figuarts Frieren</h1><dl><div><dt>商品サイズ</dt><dd>全高：約120mm</dd></div><div><dt>商品素材</dt><dd>PVC、ABS製</dd></div></dl>"
    r = Adapter().parse(html, "https://tamashiiweb.com/item/14690/")
    assert r["height_mm"] == 120 and r["material"] == "PVC、ABS製"


def test_hottoys_distributor_not_manufacturer():
    html = (
        "<h1>Figure</h1><table><tr><th>メーカー</th><td>サイドショウ</td></tr></table>"
    )
    with pytest.raises(ValueError):
        HotToys().parse(html, "https://www.hottoys.jp/item/view/1")


def test_authorized_import_deduplicates_and_does_not_trust_status(db):
    f = db.scalar(select(Figure))
    v = f.variants[0]
    raw = [
        {
            "variant_id": v.id,
            "kind": "retail",
            "source_url": "https://shop.example/product/1",
            "amount": "10000",
            "currency": "KRW",
            "observed_at": (now() - timedelta(minutes=1)).isoformat(),
            "candidate": {"name": f.name_original},
            "rights_note": "test fixture, not real data",
            "retailer_name": "Test seller",
            "match_status": "MATCHED",
        }
    ]
    assert import_rows(db, raw) == 1
    assert import_rows(db, raw) == 0
    record = db.scalar(
        select(RetailPriceRecord).where(
            RetailPriceRecord.product_url == "https://shop.example/product/1"
        )
    )
    assert record.match_status == "MATCH_REVIEW_REQUIRED"


def test_import_invalid_batch_is_not_partially_applied(db):
    before = db.scalar(select(func.count(RetailPriceRecord.id)))
    with pytest.raises(ValueError):
        import_rows(
            db,
            [
                {
                    "variant_id": 1,
                    "kind": "retail",
                    "source_url": "https://example.com",
                    "amount": "-1",
                    "currency": "KRW",
                    "observed_at": now().isoformat(),
                    "candidate": {},
                    "rights_note": "test only",
                    "retailer_name": "X",
                }
            ],
        )
    assert db.scalar(select(func.count(RetailPriceRecord.id))) == before
