from decimal import Decimal
from datetime import date
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.models.entities import (
    Base,
    Manufacturer,
    Figure,
    FigureVariant,
    ReleasePrice,
    ExchangeRate,
    now,
    User,
)
from app.core.database import get_db
from app.api.personal import router
from app.api import korea_prices as korea
from app.services.enrichment import extract_media, translate_name, enrich_html


@pytest.fixture
def context(monkeypatch):
    from app.core.config import get_settings
    monkeypatch.setattr(get_settings(), 'admin_token', 'fixture-admin-token-0123456789')
    engine = create_engine(
        "sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    db.add(User(id=1, username='admin'))
    m = Manufacturer(
        name="Bandai Spirits", name_ko="반다이", official_url="https://tamashiiweb.com"
    )
    db.add(m)
    db.flush()
    f = Figure(
        manufacturer_id=m.id,
        name_original="テスト",
        official_url="https://tamashiiweb.com/item/1/",
    )
    db.add(f)
    db.flush()
    v = FigureVariant(figure_id=f.id)
    db.add(v)
    db.commit()
    app = FastAPI()
    app.include_router(router)
    from app.api.pricing import router as pricing_router
    from app.api.product_text import router as text_router
    app.include_router(pricing_router)
    app.include_router(text_router)
    app.include_router(korea.router)
    from app.api.accounts import router as accounts_router
    app.include_router(accounts_router)
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app, headers={'X-Admin-Token': 'fixture-admin-token-0123456789'}) as client:
        yield client, db, f, v
    db.close()
    engine.dispose()


def test_purchase_crud_and_delivery(context):
    c, db, f, v = context
    c.headers.pop('X-Admin-Token', None)  # Personal writes remain available in local single-user mode.
    assert c.post('/api/auth/register', json={'username':'test-user','password':'test-password-long'}).status_code == 200
    body = {
        "variant_id": v.id,
        "amount": "120000",
        "purchased_on": date.today().isoformat(),
        "delivery_status": "pending",
    }
    r = c.post("/api/purchases", json=body)
    assert r.status_code == 200, r.text
    pid = r.json()["id"]
    body.update(delivery_status="delivered", amount="110000", memo="완료")
    assert c.put(f"/api/purchases/{pid}", json=body).status_code == 200
    assert c.get("/api/purchases").json()[0]["delivery_status"] == "delivered"
    assert c.post("/api/purchases", json={**body, "amount": "-1"}).status_code == 422
    assert c.post("/api/purchases", json={**body, "variant_id": 999}).status_code == 404
    assert c.delete(f"/api/purchases/{pid}").status_code == 200
    assert c.get("/api/purchases").json() == []


def test_favorite_idempotent_persistent(context):
    c, db, f, v = context
    c.headers.pop('X-Admin-Token', None)  # personal data needs a user session, not the operator token
    assert c.post('/api/auth/register', json={'username': 'fav-user', 'password': 'test-password-long'}).status_code == 200
    for _ in range(2):
        assert c.put(f"/api/favorites/{f.id}").status_code == 200
    assert len(c.get("/api/favorites").json()) == 1
    db.expire_all()
    assert c.get("/api/figures/999").status_code == 404
    assert c.delete(f"/api/favorites/{f.id}").status_code == 200
    assert c.get("/api/favorites").json() == []
    assert (
        c.put(
            f"/api/favorites/{f.id}", headers={"Origin": "https://evil.example"}
        ).status_code
        == 403
    )


def test_currency_and_korea(context):
    c, db, f, v = context
    db.add(
        ExchangeRate(
            pair="JPY/KRW",
            rate=Decimal("9.5"),
            rate_date=date.today().isoformat(),
            source_url="https://api.frankfurter.dev",
            checked_at=now(),
        )
    )
    db.add(
        ReleasePrice(
            variant_id=v.id,
            price_amount=4800,
            currency="JPY",
            price_kind="official_list",
            source_url=f.official_url,
        )
    )
    db.commit()
    body = {
        "variant_id": v.id,
        "source_url": "https://www.bnkrmall.co.kr/goods/detail.do?gno=123",
        "amount": 65000,
        "confirmed_same_product": True,
    }
    assert c.post("/api/korea-prices", json=body).status_code == 200
    r = c.get(f"/api/figures/{f.id}/local-prices?variant_id={v.id}").json()
    assert Decimal(str(r["estimate_krw"])) == 45600
    assert r["korea"]["currency"] == "KRW"
    assert (
        c.post(
            "/api/korea-prices",
            json={**body, "source_url": "https://fake.example/goods/detail.do?gno=123"},
        ).status_code
        == 422
    )
    assert (
        c.post(
            "/api/korea-prices", json={**body, "confirmed_same_product": False}
        ).status_code
        == 422
    )


def test_media_extraction():
    html = """<script type="application/ld+json">{"@type":"Product","image":["/a.jpg","/a.jpg"]}</script><meta property="og:image" content="https://cdn.example/b.png"><div class="c-panzoom"><img src="/c.jpg"></div>"""
    assert extract_media(html, "https://official.example/item") == [
        "https://official.example/a.jpg",
        "https://cdn.example/b.png",
        "https://official.example/c.jpg",
    ]


def test_media_storage_and_idempotence(context, monkeypatch):
    c, db, f, v = context
    monkeypatch.setattr(
        "app.services.enrichment.download_image",
        lambda *args: "/api/media/" + "a" * 64 + ".jpg",
    )
    monkeypatch.setattr("app.services.enrichment.time.sleep", lambda _: None)
    html = '<meta property="og:image" content="https://cdn.example/a.jpg"><div id="description">Product description</div>'
    assert enrich_html(db, f, v, html, f.official_url)["images_added"] == 1
    assert enrich_html(db, f, v, html, f.official_url)["images_added"] == 0
    assert c.put(f"/api/favorites/{f.id}").status_code == 200
    assert c.get("/api/favorites").json()[0]["thumbnail"].startswith("/api/media/")


def test_existing_translation_not_called(context):
    c, db, f, v = context
    f.name_ko = "테스트"
    db.commit()
    assert translate_name(db, f) == "already_translated"


def test_shopify_template_and_share_links():
    html = """<main><div class="product"><img data-src="//cdn.example/a_{width}x.jpg?v=1"></div><a href="https://pinterest.com/pin/create/button/?media=https://cdn.example/a.jpg">Share</a><a href="/b.png?v=1">Image</a></main>"""
    assert extract_media(html, "https://official.example/item") == [
        "https://cdn.example/a_1200x.jpg?v=1",
        "https://official.example/b.png?v=1",
    ]


def test_repeated_offers_upsert(context):
    c, db, f, v = context
    html = """<script type="application/ld+json">{"@type":"Product","offers":[{"priceCurrency":"JPY","price":1000},{"priceCurrency":"JPY","price":1200}]}</script>"""
    enrich_html(db, f, v, html, f.official_url, False)
    enrich_html(db, f, v, html, f.official_url, False)
    rows = list(db.scalars(select(ReleasePrice).where(ReleasePrice.variant_id == v.id)))
    assert len(rows) == 1 and rows[0].price_amount == 1200


def test_parallel_image_downloads(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    import httpx
    import app.services.enrichment as module

    barrier = Barrier(2)
    original = httpx.Client

    def respond(request):
        barrier.wait(timeout=5)
        return httpx.Response(200, content=b"\xff\xd8\xfftest-image")

    monkeypatch.setattr(module, "public_url", lambda _: None)
    monkeypatch.setattr(
        module.httpx,
        "Client",
        lambda **kwargs: original(
            transport=httpx.MockTransport(respond), trust_env=False
        ),
    )
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(
            pool.map(
                lambda _: module.download_image("https://cdn.example/a.jpg", tmp_path),
                range(2),
            )
        )
    assert results[0] == results[1]
    assert len(list(tmp_path.glob("*.jpg"))) == 1
    assert not list(tmp_path.glob("*.part"))
