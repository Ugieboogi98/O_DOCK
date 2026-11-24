from sqlalchemy import select
from app.models.entities import Figure, SourceDocument
from app.core.config import get_settings
from app.services.discovery import discover_documents


def test_query_and_selection_and_cache_keep_official_document(db, monkeypatch):
    cfg = get_settings()
    monkeypatch.setattr(cfg, "llm_api_key", "fake")
    monkeypatch.setattr(cfg, "search_api_key", "fake")
    f = db.scalar(select(Figure))
    v = f.variants[0]
    calls = []

    def model(prompt, payload, json_output=False):
        calls.append(payload)
        return (
            {"queries": ["specific product details"]}
            if "question" in payload
            else {"ids": []}
        )  # AI rejects everything

    searches = []
    monkeypatch.setattr("app.services.discovery.call", model)
    monkeypatch.setattr(
        "app.services.discovery.search",
        lambda q: searches.append(q)
        or [
            {
                "title": "Other",
                "url": "https://example.com/unrelated",
                "summary": "different product",
            }
        ],
    )

    class Fetcher:
        def fetch(self, url):
            assert (
                url == f.official_url
            )  # selected product always included despite rejection
            return "<main>Official factual specifications.</main>"

    monkeypatch.setattr("app.services.discovery.SafeFetcher", Fetcher)
    discover_documents(db, f, v, "사양")
    before = len(searches)
    discover_documents(db, f, v, "사양")
    assert len(searches) == before
    assert db.scalar(
        select(SourceDocument).where(
            SourceDocument.variant_id == v.id, SourceDocument.url == f.official_url
        )
    )
    assert any("candidates" in p for p in calls)
