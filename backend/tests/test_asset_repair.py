"""Missing-asset repair and provider failure regression; never calls a paid API."""

import json
from types import SimpleNamespace
import pytest
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from app.models.entities import (
    Base,
    Figure,
    CollectionJob,
    SourceDocument,
    ProductImage,
)
from app.services import enrichment as media
from scripts import repair_assets
from scripts.seed import seed
from app.core.config import get_settings


@pytest.fixture
def isolated_assets(tmp_path, monkeypatch):
    engine = create_engine("sqlite:///" + str(tmp_path / "assets.db"))
    Base.metadata.create_all(engine)
    factory = sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(repair_assets, "SessionLocal", factory)
    cfg = get_settings()
    monkeypatch.setattr(cfg, "media_dir", tmp_path / "media")
    monkeypatch.setattr(cfg, "llm_api_key", "test-key-not-real")
    monkeypatch.setattr(media.time, "sleep", lambda _: None)
    with factory() as db:
        from app.models.entities import now

        seed(
            db,
            [
                {
                    "manufacturer": "MegaHouse",
                    "official_url": f"https://megahobby.jp/products/item/{i}/",
                    "name_original": f"フィギュア{i}",
                    "checked_at": now().isoformat(),
                    "source_url": f"https://megahobby.jp/products/item/{i}/",
                    "source_text": "metadata",
                }
                for i in range(1, 4)
            ],
        )
    yield factory, tmp_path
    engine.dispose()


def fake_client(monkeypatch, results):
    import openai

    calls = []

    def create(**kwargs):
        calls.append(kwargs)
        value = results.pop(0)
        if isinstance(value, Exception):
            raise value
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=value))]
        )

    monkeypatch.setattr(
        openai,
        "OpenAI",
        lambda **kw: SimpleNamespace(
            chat=SimpleNamespace(completions=SimpleNamespace(create=create))
        ),
    )
    return calls


def args(tmp_path, mode):
    return repair_assets.parser().parse_args(
        [
            "--mode",
            mode,
            "--only-missing",
            "--no-index",
            "--state-file",
            str(tmp_path / "state/checkpoint.json"),
        ]
    )


class ProviderError(Exception):
    def __init__(self, status, code="", retry_after=""):
        self.status_code = status
        self.code = code
        self.body = {"error": {"code": code}}
        self.response = SimpleNamespace(headers={"retry-after": retry_after})


def test_megahouse_gallery_selectors_ignore_related_products():
    html = '<meta property="og:image" content="//www.megahobby.jp"><div class="item_main"><img src="/images/item/a.jpg"></div><a class="colorbox" href="/images/item/b.jpg"><img src="/images/item/thumb.jpg"></a><aside><img src="/images/item/related.jpg"></aside>'
    links = media.extract_media(html, "https://megahobby.jp/products/item/1/")
    assert links == [
        "https://megahobby.jp/images/item/a.jpg",
        "https://megahobby.jp/images/item/b.jpg",
    ]


def test_transient_rate_limit_retries_and_queues_index(isolated_assets, monkeypatch):
    factory, _ = isolated_assets
    calls = fake_client(
        monkeypatch,
        [ProviderError(429, "rate_limit_exceeded"), '{"name_ko":"피규어 1"}'],
    )
    with factory() as db:
        f = db.scalar(select(Figure))
        assert media.translate_name(db, f) == "translated"
        assert f.name_ko == "피규어 1"
        assert media.translate_name(db, f) == "already_translated"
        assert (
            db.scalar(
                select(func.count(CollectionJob.id)).where(
                    CollectionJob.collector == "catalog_index"
                )
            )
            == 1
        )
    assert len(calls) == 2


def test_quota_error_does_not_retry_or_scan_all_products(isolated_assets, monkeypatch):
    factory, tmp = isolated_assets
    calls = fake_client(monkeypatch, [ProviderError(429, "insufficient_quota")])
    result, code = repair_assets.run(args(tmp, "translations"))
    assert code == 1 and result["translation_blocked"] == "QUOTA_EXHAUSTED"
    assert result["processed"] == 1 and len(calls) == 1
    with factory() as db:
        assert all(f.name_ko is None for f in db.scalars(select(Figure)))


def test_rate_retry_budget_is_bounded(isolated_assets, monkeypatch):
    factory, _ = isolated_assets
    calls = fake_client(monkeypatch, [ProviderError(429) for _ in range(3)])
    with factory() as db:
        with pytest.raises(media.TranslationUnavailable, match="RATE_LIMIT_EXHAUSTED"):
            media.translate_name(db, db.scalar(select(Figure)), max_retries=2)
    assert len(calls) == 3


def test_large_retry_after_defers_without_shortening_server_delay(
    isolated_assets, monkeypatch
):
    factory, _ = isolated_assets
    calls = fake_client(monkeypatch, [ProviderError(429, retry_after="120")])
    with factory() as db:
        with pytest.raises(
            media.TranslationUnavailable, match="RETRY_AFTER_REQUIRES_LATER_RUN"
        ):
            media.translate_name(db, db.scalar(select(Figure)))
    assert len(calls) == 1


def test_japanese_output_not_stored_as_korean(isolated_assets, monkeypatch):
    factory, _ = isolated_assets
    fake_client(monkeypatch, ['{"name_ko":"フィギュア"}'])
    with factory() as db:
        f = db.scalar(select(Figure))
        with pytest.raises(
            media.TranslationUnavailable, match="TRANSLATION_NOT_KOREAN"
        ):
            media.translate_name(db, f)
        assert f.name_ko is None


def test_missing_image_pass_and_rerun_do_not_save_descriptions(
    isolated_assets, monkeypatch
):
    factory, tmp = isolated_assets

    class Fetcher:
        calls = 0

        def fetch_page(self, url):
            self.calls += 1
            return (
                '<div class="item_main"><img src="/images/item/image.jpg"></div><div id="description">Do not save</div>',
                url,
            )

    fetcher = Fetcher()
    monkeypatch.setattr(repair_assets, "SafeFetcher", lambda: fetcher)

    def download(url, folder):
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "image.jpg").write_bytes(b"\xff\xd8\xfftest")
        return "/api/media/image.jpg"

    monkeypatch.setattr(media, "download_image", download)
    a = args(tmp, "images")
    result, code = repair_assets.run(a)
    assert code == 0 and result["images_ready"] == 3
    assert fetcher.calls == 3
    result, code = repair_assets.run(a)
    assert code == 0 and result["already_complete"] == 3
    assert fetcher.calls == 3
    with factory() as db:
        assert db.scalar(select(func.count(ProductImage.id))) == 3
        assert db.scalar(select(func.count(SourceDocument.id))) == 3


def test_missing_local_file_is_repaired(isolated_assets, monkeypatch):
    factory, tmp = isolated_assets
    with factory() as db:
        f = db.scalar(select(Figure))
        db.add(
            ProductImage(
                variant_id=f.variants[0].id,
                image_url="/api/media/gone.jpg",
                source_url="https://megahobby.jp/images/item/a.jpg",
                usage_status="personal_local",
            )
        )
        db.commit()
        assert media.image_count(db, [f.variants[0].id]) == 0

        def download(url, folder):
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "gone.jpg").write_bytes(b"\xff\xd8\xfftest")
            return "/api/media/gone.jpg"

        monkeypatch.setattr(media, "download_image", download)
        media.enrich_html(
            db,
            f,
            f.variants[0],
            '<meta property="og:image" content="/images/item/a.jpg">',
            f.official_url,
            media_only=True,
            max_images=1,
        )
        assert media.image_count(db, [f.variants[0].id]) == 1
        assert db.scalar(select(func.count(ProductImage.id))) == 1


@pytest.mark.parametrize("file_exists", [True, False])
def test_refresh_preserves_hidden_duplicate(isolated_assets, monkeypatch, file_exists):
    factory, tmp = isolated_assets
    source = "https://megahobby.jp/images/item/a.jpg"
    if file_exists:
        folder = tmp / "media"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "hidden.jpg").write_bytes(b"image")

    def unexpected_download(*args):
        pytest.fail("A hidden duplicate must not be downloaded again")

    monkeypatch.setattr(media, "download_image", unexpected_download)
    with factory() as db:
        f = db.scalar(select(Figure))
        record = ProductImage(
            variant_id=f.variants[0].id,
            image_url="/api/media/hidden.jpg",
            source_url=source,
            usage_status="duplicate_hidden",
        )
        db.add(record)
        db.commit()
        for _ in range(2):
            media._enrich_html(
                db, f, f.variants[0],
                '<meta property="og:image" content="/images/item/a.jpg">',
                f.official_url, media_only=True,
            )
        db.refresh(record)
        assert record.usage_status == "duplicate_hidden"
        assert record.image_url == "/api/media/hidden.jpg"
        assert db.scalar(select(func.count(ProductImage.id))) == 1
        assert media.image_count(db, [f.variants[0].id]) == 0


@pytest.mark.parametrize("file_exists", [True, False])
def test_bnkr_refresh_preserves_hidden_duplicate(isolated_assets, monkeypatch, file_exists):
    from app.core import database
    from app.services import bnkr_catalog

    factory, tmp = isolated_assets
    source = "https://cdn.bnkrmall.co.kr/hidden.jpg"
    monkeypatch.setattr(database, "SessionLocal", factory)
    monkeypatch.setattr(bnkr_catalog.time, "sleep", lambda _: None)
    if file_exists:
        folder = tmp / "media"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "hidden.jpg").write_bytes(b"image")
    with factory() as db:
        f = db.scalar(select(Figure))
        vid = f.variants[0].id
        db.add(ProductImage(variant_id=vid, image_url="/api/media/hidden.jpg",
                            source_url=source, usage_status="duplicate_hidden"))
        db.commit()

    monkeypatch.setattr(bnkr_catalog, "match_variant",
                        lambda db, row: (db.get(Figure, f.id).variants[0], "matched"))

    def unexpected_download(*args):
        pytest.fail("A hidden duplicate must not be downloaded again")

    monkeypatch.setattr(media, "download_image", unexpected_download)
    row = {"name_ko": "피규어", "url": "https://www.bnkrmall.co.kr/goods/detail.do?gno=1",
           "jan_code": None, "specifications": {}, "price_krw": None, "images": [source]}
    for _ in range(2):
        bnkr_catalog.store_product(row, SimpleNamespace(commit=True, max_images=10), SimpleNamespace())
    with factory() as db:
        record = db.scalar(select(ProductImage))
        assert record.usage_status == "duplicate_hidden"
        assert db.scalar(select(func.count(ProductImage.id))) == 1


def test_images_continue_when_translation_provider_is_blocked(
    isolated_assets, monkeypatch
):
    factory, tmp = isolated_assets
    fake_client(monkeypatch, [ProviderError(401)])

    class Fetcher:
        def fetch_page(self, url):
            return '<meta property="og:image" content="/a.jpg">', url

    monkeypatch.setattr(repair_assets, "SafeFetcher", Fetcher)

    def download(url, folder):
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "a.jpg").write_bytes(b"\xff\xd8\xfftest")
        return "/api/media/a.jpg"

    monkeypatch.setattr(media, "download_image", download)
    result, code = repair_assets.run(args(tmp, "both"))
    assert code == 1 and result["images_ready"] == 3
    assert result["translation_blocked"] == "AUTH_OR_PERMISSION_ERROR"
