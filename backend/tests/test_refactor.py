import json
from urllib.parse import unquote
import pytest
from app.collectors.bnkr_prices import parse_prices, PriceError
from app.collectors.used_market.links import search_links
from app.collectors.manufacturers.base import ManufacturerAdapter
from app.main import app

SALE = '<input name="price" value="26000"><p class="price_result"><span class="num">23,000</span>원</p><p class="price_origin">26,000</p><p class="total_price">0</p>'


def test_sale_not_list_or_cart():
    assert parse_prices(SALE)["sale_krw"] == 23000
    assert parse_prices(SALE)["origin_krw"] == 26000


@pytest.mark.parametrize(
    "html",
    [
        '<input name="price" value="26000">',
        SALE + '<p class="price_result"><span class="num">22000</span></p>',
        SALE.replace("23,000", "27,000"),
        SALE.replace("26,000", "25,000"),
        "<p>Request rejected</p>" + SALE,
    ],
)
def test_price_uncertainty_not_saved(html):
    with pytest.raises(PriceError):
        parse_prices(html)


def test_all_bnkr_entrypoints_share_parser():
    from app.services.bnkr_catalog import parse_product
    from app.api.korea_prices import parse_korea
    from scripts.repair_bnkr_prices import parse_prices as repair

    html = SALE + '<meta property="og:description" content="Grandista テスト">'
    assert parse_korea(html)["amount"] == "23000"
    assert (
        parse_product(html, "https://www.bnkrmall.co.kr/goods/detail.do?gno=1")[
            "price_krw"
        ]
        == "23000"
    )
    assert repair is parse_prices


def test_marketplace_languages():
    links = search_links("初音ミク & 1/7", "하츠네 미쿠 & 1/7")
    assert "初音ミク & 1/7" in unquote(links[0]["url"])
    assert all("하츠네 미쿠 & 1/7" in unquote(x["url"]) for x in links[1:])
    assert all(x["url"] is None for x in search_links("初音ミク")[1:])
    assert search_links("하츠네 미쿠", "하츠네 미쿠")[0]["url"] is None


def test_no_duplicate_api_routes_and_korea_registered():
    from fastapi.testclient import TestClient

    # OpenAPI paths verifies actual router composition across FastAPI versions.
    schema = app.openapi()
    assert "post" in schema["paths"]["/api/korea-prices"]
    assert "get" in schema["paths"]["/api/franchises"]
    operation_ids = [
        op["operationId"]
        for methods in schema["paths"].values()
        for op in methods.values()
    ]
    assert len(operation_ids) == len(set(operation_ids))


@pytest.mark.parametrize("currency", ["JPY", "KRW", "USD"])
def test_common_adapter_preserves_price_currency(currency):
    adapter = ManufacturerAdapter()
    adapter.manufacturer = "Maker"
    product = {
        "@type": "Product",
        "name": "Test",
        "brand": "Maker",
        "offers": {"price": "23,000", "priceCurrency": currency},
    }
    result = adapter.parse(
        '<script type="application/ld+json">' + json.dumps(product) + "</script>",
        "https://example.com/item/1",
    )
    assert (result["price_amount"], result["currency"]) == ("23000", currency)


def test_uncertain_price_not_chosen():
    a = ManufacturerAdapter()
    a.manufacturer = "Maker"
    product = {
        "@type": "Product",
        "name": "Test",
        "offers": [
            {"price": 100, "priceCurrency": "JPY"},
            {"price": 200, "priceCurrency": "JPY"},
        ],
    }
    assert "price_amount" not in a.parse(
        '<script type="application/ld+json">' + json.dumps(product) + "</script>",
        "https://example.com/1",
    )


def test_translated_franchise_character_and_literal_percent(tmp_path):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    from app.models.entities import Base, Manufacturer, Figure
    from app.models.korean import KoreanProfile
    from app.repositories.figures import list_figures

    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        maker = Manufacturer(
            name="Maker", name_ko="제조사", official_url="https://example.com"
        )
        db.add(maker)
        db.flush()
        figure = Figure(
            manufacturer_id=maker.id,
            name_original="原文",
            official_url="https://example.com/1",
            franchise="作品",
        )
        db.add(figure)
        db.flush()
        db.add(
            KoreanProfile(
                figure_id=figure.id,
                source_hash="test",
                fields={"franchise_ko": "작품", "character_ko": "미쿠"},
                model="test",
            )
        )
        db.commit()
        assert list_figures(db, franchise="작품")["total"] == 1
        assert list_figures(db, character="미쿠")["total"] == 1
        assert list_figures(db, q="미쿠")["total"] == 1
        assert list_figures(db, franchise="%")["total"] == 0
    engine.dispose()


def test_auto_sources_fairness_and_failure_isolation(monkeypatch):
    from sqlalchemy import create_engine, event
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool
    from app.models.entities import Base, CollectionJob
    from app.services import catalog_refresh as refresh, catalog_ingest as ingest

    engine = create_engine(
        "sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
    )

    @event.listens_for(engine, "connect")
    def functions(conn, _):
        conn.create_function("pg_try_advisory_lock", 1, lambda key: 1)
        conn.create_function("pg_advisory_unlock", 1, lambda key: 1)

    Base.metadata.create_all(engine)
    factory = sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(refresh, "SessionLocal", factory)
    monkeypatch.setattr(
        ingest, "retry_pending_indexes", lambda: dict(indexed=0, failed=0)
    )
    monkeypatch.setattr(
        ingest, "retry_pending_enrichment", lambda f: dict(completed=0, failed=0)
    )
    config = {
        "max_pages_per_source": 1,
        "max_new_products_per_run": 4,
        "max_products_per_source": 20,
        "sources": [
            {
                "manufacturer": "FuRyu",
                "start_url": "https://furyu-hm.com/collections/scale-figures",
                "auto_enabled": True,
            },
            {
                "manufacturer": "MegaHouse",
                "start_url": "https://megahobby.jp/products/",
                "auto_enabled": True,
            },
        ],
    }
    monkeypatch.setattr(refresh, "_config", lambda: config)

    class Fetcher:
        def validate(self, url):
            pass

        def fetch(self, url):
            prefix = (
                "https://furyu-hm.com/products/"
                if "furyu" in url
                else "https://megahobby.jp/products/item/"
            )
            return "".join(f'<a href="{prefix}{i}/">item</a>' for i in range(10))

    monkeypatch.setattr(refresh, "SafeFetcher", Fetcher)
    calls = []
    monkeypatch.setattr(
        refresh, "_collect_one", lambda f, u, **kw: calls.append(u) or "created"
    )
    with factory() as db:
        job = CollectionJob(collector=refresh.COLLECTOR, status="running")
        db.add(job)
        db.commit()
        jid = job.id
    refresh._execute(jid)
    assert len(calls) == 4
    assert sum("furyu" in url for url in calls) == 2
    with factory() as db:
        result = refresh._result(db.get(CollectionJob, jid))
        assert result["state"] == "completed"
        assert len(result["sources"]) == 2
    # A broken source cannot stop the following maker.
    calls.clear()

    def fail_first(f, u, **kw):
        if "furyu" in u:
            raise ValueError("offline")
        calls.append(u)
        return "created"

    monkeypatch.setattr(refresh, "_collect_one", fail_first)
    refresh._execute(jid)
    assert len(calls) == 2
    with factory() as db:
        assert db.get(CollectionJob, jid).status == "partial"
    engine.dispose()
