import json
from datetime import timedelta
from decimal import Decimal
from sqlalchemy import select, func
from app.models.entities import *
from app.core.config import get_settings
from app.repositories.figures import list_figures
from app.services.prices import price_summary, used_summary
from scripts.seed import seed


def test_seed_idempotent(db):
    rows = json.loads((get_settings().data_dir / "figures.json").read_text())
    before = db.scalar(select(func.count(Figure.id)))
    assert seed(db, rows) == 0
    assert db.scalar(select(func.count(Figure.id))) == before


def test_api_listing_detail_sources_and_missing(client):
    assert client.get("/api/health").status_code == 200
    data = client.get("/api/figures?page_size=5").json()
    assert data["total"] >= 100
    assert len(data["items"]) == 5
    f = data["items"][0]
    assert (
        client.get(f"/api/figures/{f['id']}").json()["name_original"]
        == f["name_original"]
    )
    sources = client.get(f"/api/figures/{f['id']}/sources").json()
    assert sources and "body" not in sources[0]
    assert client.get("/api/figures/99999999").status_code == 404
    assert client.get("/api/figures?page_size=10000").status_code == 422


def test_numeric_filters_use_database(client):
    r = client.get("/api/figures?height_max=150").json()
    assert r["items"]
    assert all(x["height_mm"] is not None and x["height_mm"] <= 150 for x in r["items"])
    assert client.get("/api/figures?height_max=1").json()["total"] == 0


def test_natural_search_and_unsupported(client):
    r = client.post(
        "/api/search/natural-language",
        json={"query": "굿스마일 컴퍼니 150mm 이하 피규어"},
    ).json()
    assert r["items"] and all(
        x["height_mm"] <= 150 and x["manufacturer"] == "Good Smile Company"
        for x in r["items"]
    )
    r = client.post(
        "/api/search/natural-language", json={"query": "10000원 이하 빨간 피규어"}
    ).json()
    assert r["items"] == [] and r["warnings"]


def test_prices_do_not_invent(client):
    fid = client.get("/api/figures").json()["items"][0]["id"]
    r = client.get(f"/api/figures/{fid}/prices").json()
    assert r["lowest_verified_krw"] is None
    r = client.get(f"/api/figures/{fid}/used-market").json()
    assert r["statistics"] == [] and len(r["search_links"]) == 4


def test_compare_and_admin_auth(client):
    fs = client.get("/api/figures?page_size=2").json()["items"]
    r = client.post("/api/compare", json={"figure_ids": [f["id"] for f in fs]})
    assert len(r.json()["items"]) == 2
    assert client.get("/api/admin/collection-jobs").status_code in (403, 503)
    assert client.post("/api/admin/reindex").status_code in (403, 503)


def test_chat_lookup_and_unknown(client, db):
    f = db.scalar(select(Figure).where(Figure.height_mm.is_not(None)))
    r = client.post(
        "/api/rag/chat", json={"figure_id": f.id, "question": "높이를 알려줘"}
    )
    assert r.status_code == 200, r.text
    r = r.json()
    assert str(f.height_mm) in r["answer"]
    assert r["sources"][0]["number"] == 1
    r = client.post(
        "/api/rag/chat",
        json={"figure_id": f.id, "question": "내일 가격은 정확히 얼마야?"},
    ).json()
    assert "확인되지 않음" in r["answer"] and not r["sources"]


def test_foreign_variant_not_allowed(client, db):
    fs = db.scalars(select(Figure).limit(2)).all()
    r = client.post(
        "/api/rag/chat",
        json={
            "figure_id": fs[0].id,
            "variant_id": fs[1].variants[0].id,
            "question": "높이",
        },
    )
    assert r.status_code == 404


def test_retail_latest_stock_and_stale(db):
    f = db.scalar(select(Figure))
    v = f.variants[0]
    r = db.scalar(select(Retailer))
    stamp = now()

    def add(url, amount, status, age=0, match="MATCHED"):
        db.add(
            RetailPriceRecord(
                variant_id=v.id,
                retailer_id=r.id,
                price_type="displayed",
                amount=amount,
                currency="KRW",
                availability=status,
                match_status=match,
                product_url=url,
                observed_at=stamp - timedelta(hours=age),
            )
        )

    add("https://example.com/a", 10000, "in_stock", 1)
    add("https://example.com/a", 10000, "sold_out")
    add("https://example.com/b", 20000, "in_stock")
    add("https://example.com/c", 500, "in_stock", 200)
    add("https://example.com/d", 1, "in_stock", 0, "MATCH_REVIEW_REQUIRED")
    db.flush()
    result = price_summary(db, v.id)
    assert result["lowest_verified_krw"] == Decimal("20000")


def test_used_currency_condition_status_separated(db):
    f = db.scalar(select(Figure))
    v = f.variants[0]
    m = db.scalar(select(UsedMarketplace))
    stamp = now()

    def add(
        url, price, currency="JPY", condition="unopened", status="active", is_set=False
    ):
        db.add(
            UsedListing(
                variant_id=v.id,
                marketplace_id=m.id,
                listing_url=url,
                asking_price=price,
                currency=currency,
                condition=condition,
                listing_status=status,
                is_set=is_set,
                match_status="MATCHED",
                observed_at=stamp,
            )
        )

    for i, p in enumerate([100, 200, 300]):
        add(f"https://example.com/{i}", p)
    add("https://example.com/krw", 999999, "KRW")
    add("https://example.com/sold", 999, "JPY", status="sold")
    add("https://example.com/set", 1, is_set=True)
    db.flush()
    stats = used_summary(db, v.id)["statistics"]
    active = next(
        s for s in stats if s["currency"] == "JPY" and s["status"] == "active"
    )
    assert active["count"] == 3 and active["median"] == 200
    assert next(s for s in stats if s["currency"] == "KRW")["median"] is None


def test_explicit_refresh_updates_facts_without_duplicate(db):
    rows = json.loads((get_settings().data_dir / "figures.json").read_text())
    r = dict(rows[0])
    f = db.scalar(select(Figure).where(Figure.official_url == r["official_url"]))
    before = db.scalar(select(func.count(Figure.id)))
    r["height_mm"] = 123
    r["source_text"] += "\nheight_mm: 123"
    seed(db, [r], refresh=True)
    assert f.height_mm == 123 and db.scalar(select(func.count(Figure.id))) == before
