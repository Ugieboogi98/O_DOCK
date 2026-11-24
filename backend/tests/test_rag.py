import pytest
from sqlalchemy import select
from app.models.entities import Figure, SourceDocument
from app.rag.store import index_variant, collection, retrieve
from app.core.config import get_settings
from app.rag.graph import answer_question
from app.schemas.requests import ChatRequest


def test_index_idempotent_and_product_filter(db):
    figures = db.scalars(select(Figure).limit(2)).all()
    for f in figures:
        index_variant(db, f, f.variants[0])
    before = collection("figure_documents").count()
    for f in figures:
        index_variant(db, f, f.variants[0])
    assert collection("figure_documents").count() == before
    f = figures[0]
    e, w = retrieve(db, f, f.variants[0], "재질", 3, "mmr")
    assert e[0]["source_type"] == "metadata"
    assert all(x["id"].startswith(f"{f.id}:{f.variants[0].id}:") for x in e[1:])


def test_old_chunks_removed_after_document_shortens(db):
    f = db.scalar(select(Figure))
    v = f.variants[0]
    d = db.scalar(select(SourceDocument).where(SourceDocument.variant_id == v.id))
    d.body = "제품 정보 " * 1500
    db.flush()
    index_variant(db, f, v)
    first = len(collection("figure_documents").get(where={"variant_id": v.id})["ids"])
    d.body = "짧은 사양"
    db.flush()
    index_variant(db, f, v)
    assert (
        first > 1
        and len(collection("figure_documents").get(where={"variant_id": v.id})["ids"])
        == 1
    )


def test_llm_node_with_mock_provider(db, monkeypatch):
    s = get_settings()
    monkeypatch.setattr(s, "llm_api_key", "test-not-a-real-key")

    def fake(prompt, payload):
        assert (
            "제공된 근거만" in prompt
            and payload["evidence"][0]["source_type"] == "metadata"
        )
        return "공식 메타데이터에 제품명이 있습니다. [근거 1]"

    monkeypatch.setattr("app.rag.graph.call", fake)
    f = db.scalar(select(Figure))
    r = answer_question(
        db, f, f.variants[0], ChatRequest(figure_id=f.id, question="제품명")
    )
    assert r["mode"] == "llm_rag" and len(r["sources"]) == 1


def test_llm_invalid_citation_is_rejected(db, monkeypatch):
    monkeypatch.setattr(get_settings(), "llm_api_key", "test-not-a-real-key")
    monkeypatch.setattr("app.rag.graph.call", lambda *a: "잘못된 주장 [근거 999]")
    f = db.scalar(select(Figure))
    r = answer_question(
        db, f, f.variants[0], ChatRequest(figure_id=f.id, question="사양")
    )
    assert not r["sources"] and "확인되지 않음" in r["answer"]
