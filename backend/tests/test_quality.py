import json, re
from app.core.config import get_settings, Settings
from app.search_agents.matching import match_product
from app.rag.citations import cited_sources
from app.rag.store import chunks, mmr_indices
from app.collectors.retailers.jsonld import parse_offers
from app.collectors.safe_http import SafeFetcher, CollectionDenied
from app.rag.embeddings import HashEmbeddings
import pytest


def test_dataset_is_real_unique_complete():
    rows = json.loads((get_settings().data_dir / "figures.json").read_text())
    assert len(rows) >= 100
    assert len({r["official_url"] for r in rows}) == len(rows)
    assert len({r["manufacturer"] for r in rows}) == 8
    assert all(
        r["source_url"].startswith("https://") and r["source_text"] and r["checked_at"]
        for r in rows
    )
    assert all(r["name_original"] not in ["TALL", "petit", "Details"] for r in rows)
    assert all(not r.get("image_url") for r in rows)


def test_duplicate_identity_conflicts_win():
    target = {"sku": "A123", "manufacturer": "Good Smile Company", "scale": "1/7"}
    assert match_product(target, {**target, "scale": "1/8"}) == "REJECTED"
    assert match_product(target, {**target, "manufacturer": "FuRyu"}) == "REJECTED"
    assert match_product(target, {**target, "is_set": True}) == "REJECTED"
    assert match_product(target, target) == "MATCHED"


def test_name_only_never_verified():
    assert match_product({"name": "Miku"}, {"name": "Miku"}) == "MATCH_REVIEW_REQUIRED"


def test_reissue_missing_needs_review():
    target = {"sku": "123", "manufacturer": "GSC", "edition": "2025 reissue"}
    assert (
        match_product(target, {"sku": "123", "manufacturer": "GSC"})
        == "MATCH_REVIEW_REQUIRED"
    )


def test_citations_only_used():
    evidence = [
        {"id": "a", "title": "A", "url": "https://a.example", "text": "A"},
        {"id": "b", "title": "B", "url": "https://b.example", "text": "B"},
    ]
    answer, sources = cited_sources("사양 [근거 2] [근거 2]", evidence)
    assert [s["number"] for s in sources] == [2] and "text" not in sources[0]
    assert cited_sources("추측한 정보", evidence)[1] == []
    assert "확인되지 않음" in cited_sources("주장 [근거 9]", evidence)[0]


def test_chunk_settings_and_mmr():
    assert len(chunks("x " * 3000)) > 1
    assert mmr_indices(
        [1.0, 0.0], [[1.0, 0.0], [0.99, 0.01], [0.0, 1.0]], 2, lambda_=0.3
    ) == [0, 2]
    with pytest.raises(ValueError):
        Settings(chunk_size=10, chunk_overlap=10)


def test_hash_deterministic():
    e = HashEmbeddings()
    assert e.embed_query("프리렌") == e.embed_query("프리렌")
    assert len(e.embed_query("")) == 384


def test_jsonld_price_not_aggregate():
    html = (
        '<script type="application/ld+json">'
        + json.dumps(
            {
                "@type": "Product",
                "name": "A",
                "sku": "X",
                "brand": {"name": "GSC"},
                "offers": [
                    {"@type": "AggregateOffer", "lowPrice": 5},
                    {
                        "@type": "Offer",
                        "price": "100,000",
                        "priceCurrency": "KRW",
                        "availability": "https://schema.org/InStock",
                    },
                ],
            }
        )
        + "</script>"
    )
    rows = parse_offers(html, "https://shop.example/product/1")
    assert len(rows) == 1
    assert rows[0]["amount"] == "100000" and rows[0]["availability"] == "in_stock"


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost/a",
        "https://127.0.0.1/a",
        "https://169.254.169.254/a",
        "https://example.com/a",
        "https://user:pass@www.goodsmile.com/en/product/1",
    ],
)
def test_collector_default_denies(url):
    with pytest.raises(CollectionDenied):
        SafeFetcher().validate(url)
