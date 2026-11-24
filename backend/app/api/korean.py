from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.repositories.figures import get_figure
from app.models.entities import SourceDocument
from app.services.ko_translation import current_profile, current_chunks, parts

router = APIRouter(prefix="/api")


class KoreanSearch(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=6, ge=1, le=12)


@router.post("/search/korean")
def search(request: KoreanSearch, db: Session = Depends(get_db)):
    from app.rag.ko_rag import answer_search

    if not request.query.strip():
        raise HTTPException(422, "검색어를 입력하세요.")
    try:
        return answer_search(db, request.query.strip(), request.top_k)
    except Exception:
        raise HTTPException(
            503,
            "한국어 색인 또는 임베딩 API를 사용할 수 없습니다. korean_pipeline --stage index 실행 결과와 API 설정을 확인하세요.",
        ) from None


@router.get("/figures/{fid}/korean")
def translated(fid: int, db: Session = Depends(get_db)):
    f = get_figure(db, fid)
    p = current_profile(db, f)
    documents = []
    for v in f.variants:
        for d in db.scalars(
            select(SourceDocument)
            .where(SourceDocument.variant_id == v.id)
            .order_by(SourceDocument.id)
        ):
            chunks = current_chunks(db, d)
            documents.append(
                {
                    "id": d.id,
                    "variant_id": v.id,
                    "title": d.title,
                    "url": d.url,
                    "body_ko": "\n".join(c.body_ko for c in chunks),
                    "parts_ready": len(chunks),
                    "parts_total": len(parts(d.body)),
                    "complete": len(chunks) == len(parts(d.body)),
                }
            )
    return {
        "figure_id": fid,
        "profile": p.fields if p else None,
        "documents": documents,
        "notice": "AI 번역입니다. 고유명사와 수치는 원문을 함께 확인하세요.",
    }
