"""Offline regression and isolated real SQL/Chroma integration; no user DB access."""

import json
from pathlib import Path
from datetime import timedelta
import pytest
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.models.entities import (
    Base,
    Figure,
    FigureVariant,
    CollectionJob,
    SourceDocument,
    now,
)
from app.collectors.manufacturers import ADAPTERS
from app.collectors.manufacturers.megahouse import Adapter as MegaHouse
from app.collectors.manufacturers.furyu import Adapter as FuRyu
from app.collectors.safe_http import (
    SafeFetcher,
    CollectionDenied,
    robots_rules,
    robots_allowed,
)
from app.services import catalog_ingest as ingest
from scripts import collect_other_makers as runner

CATALOG = "https://furyu-hm.com/collections/scale-figures"
P1, P2 = "https://furyu-hm.com/products/alpha", "https://furyu-hm.com/products/beta"


def product(title="Alpha", sku="F-1"):
    fields = {
        "商品名": title,
        "SKU": sku,
        "発売元": "フリュー株式会社",
        "作品名": "作品",
        "ブランド": "F:NEX",
        "商品サイズ": "全高：約26cm",
        "仕様": "PVC、ABS製",
        "お届け時期": "2027年2月 発送予定",
    }
    return "<h1>Alpha</h1>" + "".join(
        f'<div class="tw-table-row"><div class="tw-table-cell">【{k}】</div><div class="tw-table-cell">{v}</div></div>'
        for k, v in fields.items()
    )


class Fetcher:
    def __init__(self, pages):
        self.pages, self.calls = pages, []

    def validate(self, url):
        if "blocked" in url:
            raise CollectionDenied("PATH_NOT_ALLOWED")
        return "furyu-hm.com", {}

    def fetch(self, url):
        self.validate(url)
        self.calls.append(url)
        value = self.pages[url]
        if isinstance(value, BaseException):
            raise value
        return value


@pytest.fixture
def isolated(monkeypatch, tmp_path):
    engine = create_engine(
        "sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(ingest, "SessionLocal", factory)
    from app.services import catalog_refresh

    monkeypatch.setattr(catalog_refresh, "SessionLocal", factory)
    from app.core.config import get_settings

    cfg = get_settings()
    monkeypatch.setattr(cfg, "chroma_host", "")
    monkeypatch.setattr(cfg, "chroma_path", str(tmp_path / "chroma"))
    monkeypatch.setattr(cfg, "embedding_provider", "hash")
    from app.rag.store import client

    client.cache_clear()
    yield factory
    client.cache_clear()
    engine.dispose()


def test_megahouse_meta_title_regression():
    row = MegaHouse().parse(
        '<meta property="og:title" content="Recovered figure"><dl><dt>サイズ</dt><dd>全高 約120mm</dd></dl>',
        "https://megahobby.jp/products/item/123/",
    )
    assert row["name_original"] == "Recovered figure"
    assert row["height_mm"] == 120


@pytest.mark.parametrize(
    "host,path,expected",
    [
        ("tamashiiweb.com", "/item/", False),
        ("tamashiiweb.com", "/item/123/", True),
        ("segaplaza.jp", "/prize/123/", True),
        ("segaplaza.jp", "/prize/calendar/", False),
        ("www.taito.co.jp", "/taito-prize/123", True),
        ("www.taito.co.jp", "/taito-prize/brand", False),
        ("www.hottoys.com.hk", "/productDetail.php?productID=123", True),
        ("www.hottoys.com.hk", "/productDetail.php", False),
        ("www.goodsmile.com", "/en/product/123", True),
        ("www.kotobukiya.co.jp", "/product/detail/p4934/", True),
        ("furyu-hm.com", "/products/", False),
    ],
)
def test_product_patterns(host, path, expected):
    a = ingest.adapter_for("https://" + host + path)
    assert a.is_product_url("https://" + host + path) is expected


def test_discovery_filters_external_and_catalogs():
    a = ingest.adapter_for(P1)
    html = '<a href="/products/">list</a><a href="/products/alpha#x">a</a><a href="https://evil.example/products/alpha">external</a>'
    assert a.discover(html, CATALOG) == [P1]


def test_furyu_fields_and_supplier_check():
    row = FuRyu().parse(product("Alpha 1/7"), P1)
    assert (row["height_mm"], row["sku"], row["release_date"], row["scale"]) == (
        260,
        "F-1",
        "2027-02",
        "1/7",
    )
    with pytest.raises(ValueError, match="MANUFACTURER"):
        FuRyu().parse(product().replace("フリュー株式会社", "Other"), P1)


def test_discovery_then_commit_caps_and_resume(tmp_path, monkeypatch):
    fetcher = Fetcher({CATALOG: f'<a href="{P1}">1</a><a href="{P2}">2</a>'})
    calls = []
    monkeypatch.setattr(
        runner, "_collect_one", lambda f, u: calls.append(u) or "created"
    )
    args = ("FuRyu", [CATALOG], fetcher, 1, 1)
    first = runner.source_job(*args, False, False, False, tmp_path)
    assert first["discovered_total"] == 2 and calls == []
    second = runner.source_job(*args, True, False, False, tmp_path)
    assert second["new_db_products"] == 1
    monkeypatch.setattr(
        runner, "_collect_one", lambda f, u: "existing" if u == P1 else "created"
    )
    third = runner.source_job(*args, True, False, False, tmp_path)
    assert third["existing_db_products"] == 1 and third["new_db_products"] == 1


def test_retry_failures_explicit_and_refresh_catalog(tmp_path, monkeypatch):
    f = Fetcher({CATALOG: RuntimeError("unavailable")})
    a = ("FuRyu", [CATALOG], f, 1, 5, False, False)
    assert runner.source_job(*a, False, tmp_path)["failed_page_count"] == 1
    f.pages[CATALOG] = f'<a href="{P1}">1</a>'
    r = runner.source_job(*a, True, tmp_path)
    assert r["failed_page_count"] == 0 and r["discovered_total"] == 1
    f.pages[CATALOG] += f'<a href="{P2}">2</a>'
    r = runner.source_job(*a, False, tmp_path, refresh_catalog=True)
    assert r["discovered_total"] == 2


def test_failed_product_requires_retry_flag(tmp_path, monkeypatch):
    f = Fetcher({CATALOG: f'<a href="{P1}">1</a>'})
    calls = []

    def fail(*args):
        calls.append(1)
        raise ValueError("bad format")

    monkeypatch.setattr(runner, "_collect_one", fail)
    args = ("FuRyu", [CATALOG], f, 1, 5, True, False)
    assert runner.source_job(*args, False, tmp_path)["failed_products"] == 1
    runner.source_job(*args, False, tmp_path)
    assert len(calls) == 1
    runner.source_job(*args, True, tmp_path)
    assert len(calls) == 2


def test_interrupt_preserves_current_page(tmp_path, monkeypatch):
    f = Fetcher({CATALOG: f'<a href="{P1}">1</a>'})
    monkeypatch.setattr(
        runner, "_collect_one", lambda *a: (_ for _ in ()).throw(KeyboardInterrupt())
    )
    with pytest.raises(KeyboardInterrupt):
        runner.source_job("FuRyu", [CATALOG], f, 1, 1, True, False, False, tmp_path)
    state = json.loads((tmp_path / "furyu/checkpoint.json").read_text())
    assert CATALOG in state["queue"]
    assert P1 in (tmp_path / "furyu/product_urls.txt").read_text()


def test_sql_chroma_replay_duplicate_sku_and_pending_repair(isolated, monkeypatch):
    f = Fetcher({P1: product(), P2: product("Alternate URL")})
    from app.rag import store

    original = store.index_variant
    monkeypatch.setattr(
        store,
        "index_variant",
        lambda *a: (_ for _ in ()).throw(RuntimeError("chroma offline")),
    )
    assert ingest.collect_one(f, P1) == "created_index_pending"
    with isolated() as db:
        assert db.scalar(select(func.count(Figure.id))) == 1
        assert db.scalar(select(func.count(SourceDocument.id))) == 1
        assert (
            db.scalar(
                select(CollectionJob).where(CollectionJob.collector == ingest.INDEX_JOB)
            ).status
            == "pending"
        )
    monkeypatch.setattr(store, "index_variant", original)
    assert ingest.retry_pending_indexes() == {"indexed": 1, "failed": 0}
    assert ingest.collect_one(f, P1) == "existing"
    assert ingest.collect_one(f, P2) == "existing"
    assert store.collection("figure_metadata").count() == 1
    assert store.collection("figure_documents").count() >= 1
    assert ingest.retry_pending_indexes() == {"indexed": 0, "failed": 0}
    with isolated() as db:
        assert db.scalar(select(func.count(Figure.id))) == 1
        fig = db.scalar(select(Figure))
        evidence, warnings = store.retrieve(
            db, fig, fig.variants[0], "높이", 3, "similarity"
        )
        assert any("260" in x["text"] for x in evidence)
        assert not warnings


def test_ingestion_queues_semantics_without_legacy_paid_translation(isolated, monkeypatch):
    from app.services import enrichment, product_semantics
    from app.services.semantic_queue import pending_jobs
    from app.core.config import get_settings
    cfg = get_settings()
    monkeypatch.setattr(cfg, 'auto_translate_names', True)
    monkeypatch.setattr(cfg, 'llm_api_key', 'fixture-not-real')

    def forbidden(*args, **kwargs):
        pytest.fail('Ingestion must not call a paid translator')

    monkeypatch.setattr(enrichment, 'translate_name', forbidden)
    monkeypatch.setattr(product_semantics, 'Extractor', forbidden)
    fetcher = Fetcher({P1: product()})
    assert ingest.collect_one(fetcher, P1, enrich=True) == 'created'
    with isolated() as db:
        jobs = pending_jobs(db)
        assert len(jobs) == 1
        initial_job = jobs[0].id
        f = db.scalar(select(Figure))
        payload = json.loads(jobs[0].error_summary)
        assert payload['source_hash'] == product_semantics.source_hash(product_semantics.source_of(f))
        assert f.name_ko is None
    assert ingest.collect_one(fetcher, P1, enrich=True) == 'existing'
    assert fetcher.calls == [P1]
    with isolated() as db:
        assert [job.id for job in pending_jobs(db)] == [initial_job]


def test_product_and_semantic_outbox_commit_atomically(isolated, monkeypatch):
    def broken_queue(*args):
        raise RuntimeError('queue unavailable')

    monkeypatch.setattr(ingest, 'enqueue_semantics', broken_queue)
    with pytest.raises(RuntimeError, match='queue unavailable'):
        ingest.collect_one(Fetcher({P1: product()}), P1)
    with isolated() as db:
        assert db.scalar(select(func.count(Figure.id))) == 0
        assert db.scalar(select(func.count(CollectionJob.id))) == 0


def test_queue_reuses_pending_work_and_finishes_only_matching_source(isolated):
    from app.services import product_semantics as sem
    from app.services.semantic_queue import enqueue, finish, pending_jobs
    assert ingest.collect_one(Fetcher({P1: product()}), P1) == 'created'
    with isolated() as db:
        f = db.scalar(select(Figure))
        job = pending_jobs(db)[0]
        previous = json.loads(job.error_summary)['source_hash']
        doc = db.scalar(select(SourceDocument))
        doc.body += ' updated description'
        db.commit()
        assert enqueue(db, f).id == job.id
        db.commit()
        current_hash = json.loads(job.error_summary)['source_hash']
        assert current_hash != previous
        finish(db, f.id, previous, 'ready')
        db.commit()
        assert job.status == 'pending'
        source = sem.source_of(f)
        response = {'name_ko': '알파', 'franchise': None, 'characters': [], 'figure_form': None}
        assert sem.save_record(db, {'figure_id': f.id, 'source': source,
            'source_hash': sem.source_hash(source), 'model': 'fixture', 'result': response}) == 'partial'
        assert not pending_jobs(db)
        assert job.status == 'completed'
        assert enqueue(db, f) is None
        db.commit()


def test_failed_enrichment_keeps_current_source_queued(isolated, monkeypatch):
    from app.services import enrichment, product_semantics as sem
    from app.services.semantic_queue import pending_jobs

    def partial(db, figure, variant, *args, **kwargs):
        doc = db.scalar(select(SourceDocument))
        doc.body += ' partial but committed detail'
        db.commit()
        return {'image_failures': [{'error': 'mock'}]}

    monkeypatch.setattr(enrichment, 'enrich_html', partial)
    assert ingest.collect_one(Fetcher({P1: product()}), P1, enrich=True) == 'created'
    with isolated() as db:
        f = db.scalar(select(Figure))
        jobs = pending_jobs(db)
        assert len(jobs) == 1
        assert json.loads(jobs[0].error_summary)['source_hash'] == sem.source_hash(sem.source_of(f))
        derivative = db.scalar(select(CollectionJob).where(CollectionJob.collector == 'catalog_enrichment'))
        assert derivative.status == 'pending'


def test_robots_wildcards_longest_rule_and_agent_precedence():
    rules = robots_rules(
        "User-agent: *\nDisallow: /collections/*sort_by*\nAllow: /\nCrawl-delay: 20",
        "FigureArchiveResearch",
    )
    assert not robots_allowed(rules, CATALOG + "?sort_by=x")
    assert robots_allowed(rules, CATALOG + "?page=2")
    rules = robots_rules(
        "User-agent: *\nAllow: /\nUser-agent: FigureArchiveResearch\nDisallow: /",
        "FigureArchiveResearch/1.0",
    )
    assert not robots_allowed(rules, P1)
    rules = robots_rules("User-agent: *\nDisallow: /a\nAllow: /a$", "test")
    assert robots_allowed(rules, "https://example.com/a")
    assert not robots_allowed(rules, "https://example.com/ab")


def test_safe_fetcher_policy_and_private_dns(monkeypatch):
    f = SafeFetcher()
    monkeypatch.setattr(
        "socket.getaddrinfo", lambda *a, **kw: [(0, 0, 0, "", ("8.8.8.8", 443))]
    )
    assert f.validate(CATALOG)[0] == "furyu-hm.com"
    with pytest.raises(CollectionDenied):
        f.validate("https://furyu-hm.com/collections/scale-figures/../admin")
    monkeypatch.setattr(
        "socket.getaddrinfo", lambda *a, **kw: [(0, 0, 0, "", ("127.0.0.1", 443))]
    )
    with pytest.raises(CollectionDenied):
        f.validate(P1)


def test_safe_fetcher_honors_robots_delay(monkeypatch):
    f = SafeFetcher()
    f.robots["example.com"] = [("crawl-delay", "20")]
    f.last["example.com"] = 100
    sleeps = []
    monkeypatch.setattr("time.monotonic", lambda: 105)
    monkeypatch.setattr("time.sleep", sleeps.append)
    f._pace("example.com", {"delay_seconds": 2})
    assert sleeps == [15]


def test_cooldown_survives_new_request(isolated, monkeypatch):
    from app.services import catalog_refresh as refresh

    monkeypatch.setattr(refresh, "_pending", False)
    with isolated() as db:
        db.add(
            CollectionJob(
                collector=refresh.COLLECTOR,
                status="completed",
                started_at=now() - timedelta(hours=23),
            )
        )
        db.commit()
    assert refresh.start_refresh()["reason"] == "cooldown"


def test_pagination_head_link_and_megahouse_regression():
    from scripts.discover_catalogs_all import pagination_links

    assert pagination_links('<link rel="next" href="?page=2">', CATALOG) == [
        CATALOG + "?page=2"
    ]
    assert pagination_links(
        '<a href="/products/2/?sort=new">2</a>', "https://megahobby.jp/products/"
    ) == ["https://megahobby.jp/products/2/?sort=new"]


def test_new_product_visible_in_api_and_status(isolated):
    from fastapi.testclient import TestClient
    from app.main import app
    from app.core.database import get_db

    assert ingest.collect_one(Fetcher({P1: product()}), P1) == "created"

    def session():
        with isolated() as db:
            yield db

    app.dependency_overrides[get_db] = session
    try:
        with TestClient(app) as client:
            listing = client.get("/api/figures").json()
            assert listing["total"] == 1
            assert listing["items"][0]["name_original"] == "Alpha"
            status = client.get("/api/status").json()
            assert status["figure_count"] == 1
            assert status["index"]["metadata"] == 1
            assert status["index_error"] is None
            makers = client.get("/api/manufacturers").json()
            assert next(m for m in makers if m["name"] == "FuRyu")["count"] == 1
    finally:
        app.dependency_overrides.clear()


def test_disk_checkpoint_contains_inflight_page(tmp_path, monkeypatch):
    f = Fetcher({CATALOG: f'<a href="{P1}">1</a><link rel="next" href="?page=2">'})

    def collect(fetcher, url):
        state = json.loads((tmp_path / "furyu/checkpoint.json").read_text())
        assert (
            CATALOG in state["queue"]
        )  # A process kill here must not lose pagination.
        return "created"

    monkeypatch.setattr(runner, "_collect_one", collect)
    runner.source_job("FuRyu", [CATALOG], f, 1, 1, True, False, False, tmp_path)
    state = json.loads((tmp_path / "furyu/checkpoint.json").read_text())
    assert state["queue"] == [CATALOG + "?page=2"]


def test_failed_page_not_retried_without_flag(tmp_path):
    f = Fetcher({CATALOG: RuntimeError()})
    args = ("FuRyu", [CATALOG], f, 1, 1, False, False, False, tmp_path)
    runner.source_job(*args)
    runner.source_job(*args)
    assert f.calls == [CATALOG]


def test_page_attempt_budget_counts_errors(tmp_path):
    f = Fetcher({CATALOG: RuntimeError()})
    folder = tmp_path / "furyu"
    folder.mkdir()
    runner.atomic_json(
        folder / "checkpoint.json", {"queue": [CATALOG, CATALOG + "?page=2"]}
    )
    result = runner.source_job(
        "FuRyu", [CATALOG], f, 1, 1, False, False, False, tmp_path
    )
    assert result["remaining_pages"] == 1 and len(f.calls) == 1


def test_all_bundled_official_urls_remain_recognized():
    from app.core.config import get_settings

    rows = json.loads((get_settings().data_dir / "figures.json").read_text())
    for row in rows:
        adapter = ingest.adapter_for(row["official_url"])
        assert adapter is not None, row["official_url"]
        assert adapter.is_product_url(row["official_url"]), row["official_url"]
