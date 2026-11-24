"""Korean catalogue RAG, isolated from existing collections and embedding settings."""

import os
import hashlib
from functools import lru_cache
from sqlalchemy import select, or_
from app.core.config import get_settings
from app.models.entities import Figure, SourceDocument
from app.models.korean import KoreanProfile
from app.services.ko_translation import (
    current_profile,
    current_chunks,
    digest,
    profile_source,
)
from app.rag.store import client, metadata_text
from app.rag.embeddings import HashEmbeddings


def config():
    s = get_settings()
    return {
        "provider": os.getenv("KOREAN_RAG_EMBEDDING_PROVIDER", "openai"),
        "model": os.getenv("KOREAN_RAG_EMBEDDING_MODEL", s.embedding_model),
        "url": s.embedding_base_url,
    }


def index_name():
    cfg = config()
    signature = digest(cfg)[:16]
    return "odock_ko_" + signature


def collection():
    return client().get_or_create_collection(
        index_name(), embedding_function=None, metadata={"hnsw:space": "cosine"}
    )


@lru_cache(maxsize=4)
def _embedder(provider, model, url, key):
    if provider == "hash":
        return HashEmbeddings()
    if provider != "openai":
        raise ValueError("KOREAN_EMBEDDING_PROVIDER_INVALID")
    if not key:
        raise ValueError("EMBEDDING_API_KEY_REQUIRED")
    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(
        model=model, base_url=url, api_key=key, max_retries=2, request_timeout=60
    )


def embedder():
    s = get_settings()
    cfg = config()
    # No implicit LLM-key reuse: providers/endpoints can be different.
    return _embedder(cfg["provider"], cfg["model"], cfg["url"], s.embedding_api_key)


def records(db, f, v):
    p = current_profile(db, f)
    if p is None:
        return []
    title = f.name_ko or p.fields["name_ko"]
    fields = p.fields
    text = (
        metadata_text(f, v)
        + "\n"
        + "\n".join(
            f'{k}: {fields.get(k) or "미확인"}'
            for k in ["franchise_ko", "character_ko", "material_ko"]
        )
    )
    text += (
        "\n한국어 상품명: "
        + title
        + "\n제조사 한국어명: "
        + (f.manufacturer.name_ko or f.manufacturer.name)
    )
    base = {
        "figure_id": f.id,
        "variant_id": v.id,
        "title": title,
        "source_url": f.official_url,
        "kind": "metadata",
        "translated": True,
    }
    rows = [
        {
            "id": f"m:{v.id}",
            "text": text,
            "metadata": {**base, "fingerprint": digest(text)},
        }
    ]
    for d in db.scalars(
        select(SourceDocument)
        .where(SourceDocument.variant_id == v.id)
        .order_by(SourceDocument.id)
    ):
        for chunk in current_chunks(db, d):
            # Every translation retains the actual original document URL, never an invented URL.
            text = f"제품: {title}\n한국어 번역 (AI 번역):\n{chunk.body_ko}"
            rows.append(
                {
                    "id": f"d:{d.id}:{chunk.part}",
                    "text": text,
                    "metadata": {
                        **base,
                        "kind": "document",
                        "source_url": d.url,
                        "document_id": d.id,
                        "part": chunk.part,
                        "source_hash": chunk.source_hash,
                        "fingerprint": digest(text),
                    },
                }
            )
    return rows


def index_figure(db, f):
    if current_profile(db, f) is None:
        return {"state": "translation_missing", "updated": 0, "skipped": 0}
    c = collection()
    updated = skipped = 0
    for v in f.variants:
        rows = records(db, f, v)
        old = c.get(where={"variant_id": v.id}, include=["metadatas"])
        fingerprints = {
            id_: m.get("fingerprint") for id_, m in zip(old["ids"], old["metadatas"])
        }
        todo = [
            r for r in rows if fingerprints.get(r["id"]) != r["metadata"]["fingerprint"]
        ]
        skipped += len(rows) - len(todo)
        for start in range(0, len(todo), 24):
            batch = todo[start : start + 24]
            vectors = embedder().embed_documents([r["text"] for r in batch])
            db.expire_all()
            f = db.get(Figure, f.id)
            fresh = {
                r["id"]: r["metadata"]["fingerprint"]
                for r in records(db, f, next(x for x in f.variants if x.id == v.id))
            }
            if any(fresh.get(r["id"]) != r["metadata"]["fingerprint"] for r in batch):
                raise ValueError("SOURCE_CHANGED_REINDEX")
            c.upsert(
                ids=[r["id"] for r in batch],
                documents=[r["text"] for r in batch],
                metadatas=[r["metadata"] for r in batch],
                embeddings=vectors,
            )
            updated += len(batch)
        stale = set(old["ids"]) - {r["id"] for r in rows}
        if stale:
            c.delete(ids=sorted(stale))
    return {"state": "indexed", "updated": updated, "skipped": skipped}


def evidence_from_rows(rows):
    return [
        {
            "id": r["id"],
            "text": r["text"],
            "title": r["metadata"]["title"],
            "url": r["metadata"]["source_url"],
            "source_type": (
                "ai_translation" if r["metadata"]["kind"] == "document" else "metadata"
            ),
            "figure_id": r["metadata"]["figure_id"],
            "variant_id": r["metadata"]["variant_id"],
        }
        for r in rows
    ]


def search_evidence(db, query, k=5, variant_id=None, mode="similarity"):
    c = collection()
    count = c.count()
    warnings = []
    if config()["provider"] == "hash":
        warnings.append(
            "단어 기반 시험 모드입니다. 한국어 의미 검색 품질을 평가하려면 openai 임베딩으로 색인하세요."
        )
    if not count:
        return [], warnings + [
            "한국어 색인이 비어 있습니다. 번역 후 korean_pipeline --stage index를 실행하세요."
        ]
    kwargs = {"where": {"variant_id": variant_id}} if variant_id is not None else {}
    q = embedder().embed_query(query)
    include = ["metadatas", "distances"] + (["embeddings"] if mode == "mmr" else [])
    result = c.query(
        query_embeddings=[q],
        n_results=min(count, max(k * 5, 30)),
        include=include,
        **kwargs,
    )
    if mode == "mmr" and result["ids"][0]:
        from app.rag.store import mmr_indices

        order = mmr_indices(q, result["embeddings"][0], len(result["ids"][0]))
        for field in ("ids", "metadatas"):
            result[field][0] = [result[field][0][i] for i in order]
    candidates = {}
    cache = {}
    # Use only live DB rows that still match the indexed text; stale translations cannot be cited.
    for rank, (rid, m) in enumerate(zip(result["ids"][0], result["metadatas"][0])):
        fid = m["figure_id"]
        vid = m["variant_id"]
        if (fid, vid) not in cache:
            f = db.get(Figure, fid)
            v = next((x for x in f.variants if x.id == vid), None) if f else None
            cache[(fid, vid)] = {r["id"]: r for r in records(db, f, v)} if v else {}
        row = cache[(fid, vid)].get(rid)
        if not row or row["metadata"]["fingerprint"] != m.get("fingerprint"):
            continue
        candidates[rid] = (1 / (60 + rank), row)
    # Exact Korean/original product names supplement semantic ranking.
    if variant_id is None:
        escaped = (
            query.strip().replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
        )
        fs = db.scalars(
            select(Figure)
            .where(
                or_(
                    Figure.name_ko.ilike("%" + escaped + "%", escape="\\"),
                    Figure.name_original.ilike("%" + escaped + "%", escape="\\"),
                )
            )
            .order_by(Figure.id)
            .limit(30)
        )
        for rank, f in enumerate(fs):
            for v in f.variants[:1]:
                rows = records(db, f, v)
                if not rows:
                    continue
                r = rows[0]
                old = candidates.get(r["id"], (0, r))
                candidates[r["id"]] = (old[0] + 1 / (60 + rank), r)
    ranked = sorted(candidates.values(), key=lambda item: item[0], reverse=True)
    selected = []
    per_figure = {}
    for score, row in ranked:
        fid = row["metadata"]["figure_id"]
        # Global search balances products; scoped Q&A can use several chunks of one product.
        if variant_id is None and per_figure.get(fid, 0) >= 2:
            continue
        selected.append(row)
        per_figure[fid] = per_figure.get(fid, 0) + 1
        if len(selected) >= k:
            break
    if not selected:
        warnings.append(
            "현재 원문과 일치하는 한국어 근거가 없습니다. 번역과 색인을 다시 실행하세요."
        )
    return evidence_from_rows(selected), warnings


def answer_search(db, query, k=6):
    from app.repositories.figures import card
    from app.rag.llm import call
    from app.rag.citations import cited_sources
    from app.rag.prompts import ANSWER_PROMPT

    evidence, warnings = search_evidence(db, query, k)
    if not evidence:
        return {
            "items": [],
            "answer": "검색에 사용할 한국어 근거가 없습니다.",
            "sources": [],
            "warnings": warnings,
            "mode": "no_evidence",
        }
    fallback = "\n\n".join(
        f'{e["title"]}: {e["text"][:400]} [근거 {i+1}]' for i, e in enumerate(evidence)
    )
    mode = "retrieved_excerpts"
    answer = fallback
    if get_settings().llm_api_key:
        try:
            answer = call(
                ANSWER_PROMPT
                + "\n서비스명은 O_DOCK이다. 여러 상품의 근거가 섞여 있으므로 상품과 버전을 구분한다. "
                "번역은 공식 한국어 명칭이 아닌 AI 번역이다. 검색된 후보가 질문 조건을 충족하는지 근거로 확인하고, "
                "확인되지 않은 조건을 충족한다고 말하지 않는다.",
                {
                    "question": query,
                    "evidence": [
                        {"number": i + 1, **e} for i, e in enumerate(evidence)
                    ],
                },
            )
            mode = "korean_rag"
        except Exception:
            warnings.append(
                "답변 생성 API를 사용할 수 없어 검색된 근거 발췌를 표시합니다."
            )
    else:
        warnings.append("LLM 키가 없어 답변 생성 대신 근거 발췌를 표시합니다.")
    answer, sources = cited_sources(answer, evidence)
    if not sources and mode == "korean_rag":
        answer, sources = cited_sources(fallback, evidence)
        mode = "retrieved_excerpts"
        warnings.append(
            "유효한 출처 인용이 없는 생성 답변 대신 근거 발췌를 표시합니다."
        )
    items = []
    seen = set()
    for e in evidence:
        if e["figure_id"] in seen:
            continue
        seen.add(e["figure_id"])
        f = db.get(Figure, e["figure_id"])
        items.append(card(f))
    return {
        "items": items,
        "answer": answer,
        "sources": sources,
        "warnings": warnings,
        "mode": mode,
        "embedding_provider": config()["provider"],
        "retrieved_count": len(evidence),
    }
