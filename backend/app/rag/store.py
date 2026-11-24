import hashlib
from functools import lru_cache
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy import select
from app.core.config import get_settings
from app.models.entities import Figure, SourceDocument
from app.rag.embeddings import embedding, signature


@lru_cache
def client():
    s = get_settings()
    cfg = ChromaSettings(anonymized_telemetry=False)
    return (
        chromadb.HttpClient(host=s.chroma_host, port=s.chroma_port, settings=cfg)
        if s.chroma_host
        else chromadb.PersistentClient(path=s.chroma_path, settings=cfg)
    )


def collection(name):
    c = client().get_or_create_collection(
        name,
        embedding_function=None,
        metadata={"hnsw:space": "cosine", "embedding_signature": signature()},
    )
    if (c.metadata or {}).get("embedding_signature") != signature():
        raise ValueError("EMBEDDING_CHANGED_REINDEX_REQUIRED")
    return c


def metadata_text(f, v):
    fields = {
        "제품명": f.name_original,
        "한국어명": f.name_ko,
        "제조사": f.manufacturer.name,
        "작품": f.franchise,
        "캐릭터": f.character,
        "라인": f.product_line.name if f.product_line else None,
        "스케일": f.scale,
        "높이(mm)": f.height_mm,
        "재질": f.material,
        "SKU": v.sku,
        "JAN": v.jan_code,
        "버전": v.edition,
        "재판": v.reissue_no,
        "발매일": v.release_date,
        "발매일 정확도": v.release_precision,
    }
    return "\n".join(
        f'{k}: {val if val is not None else "미확인"}' for k, val in fields.items()
    )


def chunks(text):
    s = get_settings()
    return RecursiveCharacterTextSplitter(
        chunk_size=s.chunk_size, chunk_overlap=s.chunk_overlap
    ).split_text(text)


def index_variant(db, f, v):
    embed = embedding()
    meta = collection("figure_metadata")
    docs = collection("figure_documents")
    body = metadata_text(f, v)
    base = {
        "figure_id": f.id,
        "variant_id": v.id,
        "manufacturer": f.manufacturer.name,
        "title": f.name_original,
        "source_type": "metadata",
        "source_url": f.official_url,
        "collected_at": f.collected_at.isoformat(),
    }
    meta.upsert(
        ids=[f"{f.id}:{v.id}"],
        documents=[body],
        metadatas=[base],
        embeddings=embed.embed_documents([body]),
    )
    ids = []
    bodies = []
    metas = []
    for d in db.scalars(
        select(SourceDocument).where(SourceDocument.variant_id == v.id)
    ):
        for i, text in enumerate(chunks(d.body)):
            ids.append(f"{f.id}:{v.id}:{d.id}:{i}")
            bodies.append(text)
            metas.append(
                {
                    **base,
                    "doc_id": d.id,
                    "title": d.title,
                    "source_type": d.source_type,
                    "source_url": d.url,
                    "collected_at": d.collected_at.isoformat(),
                }
            )
    # Upsert first, then delete stale tails; a failed embedding call retains the previous usable index.
    for start in range(0, len(ids), 64):
        sl = slice(start, start + 64)
        docs.upsert(
            ids=ids[sl],
            documents=bodies[sl],
            metadatas=metas[sl],
            embeddings=embed.embed_documents(bodies[sl]),
        )
    existing = docs.get(where={"variant_id": v.id})["ids"]
    stale = list(set(existing) - set(ids))
    if stale:
        docs.delete(ids=stale)
    return len(ids)


def index_all(db, reset=False):
    if reset:
        for name in ("figure_metadata", "figure_documents"):
            try:
                client().delete_collection(name)
            except chromadb.errors.NotFoundError:
                pass
    count = 0
    for f in db.scalars(select(Figure).order_by(Figure.id)):
        for v in f.variants:
            count += index_variant(db, f, v)
    return {
        "metadata": collection("figure_metadata").count(),
        "documents": collection("figure_documents").count(),
    }


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def mmr_indices(query, vectors, k, lambda_=0.65):
    selected = []
    remaining = list(range(len(vectors)))
    while remaining and len(selected) < k:
        best = max(
            remaining,
            key=lambda i: lambda_ * dot(query, vectors[i])
            - (1 - lambda_)
            * max((dot(vectors[i], vectors[j]) for j in selected), default=0),
        )
        selected.append(best)
        remaining.remove(best)
    return selected


def retrieve(db, f, v, question, k, mode):
    # O_DOCK Korean translated evidence
    try:
        from app.services.ko_translation import current_profile

        if current_profile(db, f) is not None:
            from app.rag.ko_rag import search_evidence, records, evidence_from_rows

            metadata = evidence_from_rows(records(db, f, v)[:1])
            found, warnings = search_evidence(
                db, question, k, variant_id=v.id, mode=mode
            )
            found = [e for e in found if not e["id"].startswith("m:")]
            if found:
                return metadata + found, warnings
            return metadata, warnings + [
                "한국어 설명 근거가 없습니다. 문서 번역/색인 상태를 확인하세요."
            ]
    except Exception:
        pass
    # The relational source remains authoritative even before an index has been built.
    evidence = [
        {
            "id": f"meta:{v.id}",
            "text": metadata_text(f, v),
            "title": f.name_original,
            "url": f.official_url,
            "source_type": "metadata",
        }
    ]
    warnings = []
    try:
        meta = collection("figure_metadata").get(
            ids=[f"{f.id}:{v.id}"], include=["documents", "metadatas"]
        )
        if meta["ids"]:
            evidence[0]["text"] = meta["documents"][0]
            evidence[0]["url"] = meta["metadatas"][0]["source_url"]
        else:
            warnings.append("메타데이터 색인이 없어 현재 DB 사양을 직접 사용했습니다.")
        c = collection("figure_documents")
        count = len(c.get(where={"variant_id": v.id})["ids"])
        if count == 0:
            return evidence, ["외부 문서 색인이 없습니다. 관리자 색인을 실행하세요."]
        q = embedding().embed_query(question)
        result = c.query(
            query_embeddings=[q],
            where={"variant_id": v.id},
            n_results=min(count, get_settings().fetch_k),
            include=["documents", "metadatas", "embeddings", "distances"],
        )
        chosen = (
            mmr_indices(q, result["embeddings"][0], k)
            if mode == "mmr"
            else list(range(min(k, len(result["ids"][0]))))
        )
        seen = {hashlib.sha256(evidence[0]["text"].encode()).hexdigest()}
        for i in chosen:
            text = result["documents"][0][i]
            h = hashlib.sha256(text.encode()).hexdigest()
            if h in seen:
                continue
            seen.add(h)
            m = result["metadatas"][0][i]
            evidence.append(
                {
                    "id": result["ids"][0][i],
                    "text": text,
                    "title": m["title"],
                    "url": m["source_url"],
                    "source_type": m["source_type"],
                }
            )
    except Exception:
        warnings.append(
            "문서 색인을 사용할 수 없습니다. 임베딩 설정·서비스 상태를 확인하세요."
        )
    return evidence, warnings
