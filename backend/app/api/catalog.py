import logging, time
from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func, text
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import require_admin
from app.services.accounts import optional_user
from app.models.entities import *
from app.schemas.requests import ChatRequest, NaturalRequest, CompareRequest
from app.repositories.figures import (
    card,
    get_figure,
    choose_variant,
    list_figures,
    serialize,
)
from app.services.prices import price_summary, used_summary

from app.services.price_refresh import refresh_prices
from app.collectors.used_market.links import search_links


from fastapi import APIRouter

router = APIRouter()


@router.get("/api/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


@router.get("/api/status")
def status(db: Session = Depends(get_db)):
    s = get_settings()
    index = {"metadata": 0, "documents": 0}
    index_error = None
    try:
        from app.rag.store import collection

        index = {
            key: collection(name).count()
            for key, name in [
                ("metadata", "figure_metadata"),
                ("documents", "figure_documents"),
            ]
        }
    except Exception:
        index_error = "색인 연결 또는 임베딩 설정 확인 필요"
    return {
        "figure_count": db.scalar(select(func.count(Figure.id))),
        "document_count": db.scalar(select(func.count(SourceDocument.id))),
        "llm_ready": bool(s.llm_api_key),
        "search_ready": bool(s.search_api_key),
        "embedding_provider": s.embedding_provider,
        "index": index,
        "index_error": index_error,
        "notice": "가격은 확인 시점의 관측값입니다. 실시간 최저가·실거래가를 보장하지 않습니다.",
    }


@router.get("/api/manufacturers")
def manufacturers(db: Session = Depends(get_db)):
    return [
        {
            **serialize(m),
            "display_group": "기타" if m.name == "Hot Toys" else m.name_ko,
            "count": db.scalar(
                select(func.count(Figure.id)).where(Figure.manufacturer_id == m.id)
            ),
        }
        for m in db.scalars(select(Manufacturer).order_by(Manufacturer.id))
    ]


@router.get("/api/product-lines")
def lines(db: Session = Depends(get_db)):
    return [
        serialize(x) for x in db.scalars(select(ProductLine).order_by(ProductLine.name))
    ]


@router.get("/api/figures")
def figures(
    q: str | None = None,
    manufacturer_id: int | None = None,
    product_line_id: int | None = None,
    scale: str | None = None,
    year: int | None = None,
    height_max: int | None = None,
    height_min: int | None = None,
    franchise: str | None = None,
    character: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(24, ge=1, le=100),
    figure_form: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(optional_user),
):
    return list_figures(
        db,
        q,
        manufacturer_id,
        scale,
        year,
        height_max,
        height_min,
        franchise,
        character,
        product_line_id,
        page,
        page_size,
        figure_form,
        user_id=user.id if user else None,
    )


@router.get("/api/figures/{fid}")
def detail(fid: int, db: Session = Depends(get_db), user=Depends(optional_user)):
    f = get_figure(db, fid)
    from app.services.image_order import ordered_images

    from app.models.entities import Favorite
    favorite = bool(user and db.get(Favorite, (fid, user.id)))
    return {**card(f, favorite=favorite), "images": [serialize(x) for x in ordered_images(db, f)]}


@router.get("/api/figures/{fid}/prices")
def prices(fid: int, variant_id: int | None = None, db: Session = Depends(get_db)):
    f = get_figure(db, fid)
    v = choose_variant(f, variant_id)
    return price_summary(db, v.id)


@router.get("/api/figures/{fid}/used-market")
def used(fid: int, variant_id: int | None = None, db: Session = Depends(get_db)):
    f = get_figure(db, fid)
    v = choose_variant(f, variant_id)
    return {
        **used_summary(db, v.id),
        "search_links": search_links(f.name_original, f.name_ko),
    }


@router.get("/api/figures/{fid}/sources")
def sources(fid: int, variant_id: int | None = None, db: Session = Depends(get_db)):
    f = get_figure(db, fid)
    v = choose_variant(f, variant_id)
    return [
        {k: val for k, val in serialize(d).items() if k != "body"}
        for d in db.scalars(
            select(SourceDocument).where(SourceDocument.variant_id == v.id)
        )
    ]


@router.post("/api/figures/{fid}/prices/refresh", dependencies=[Depends(require_admin)])
def refresh(fid: int, variant_id: int | None = None, db: Session = Depends(get_db)):
    f = get_figure(db, fid)
    v = choose_variant(f, variant_id)
    # Row lock also serializes independent backend workers for the same variant.
    db.execute(select(FigureVariant).where(FigureVariant.id == v.id).with_for_update())
    return refresh_prices(db, f, v)


@router.post(
    "/api/figures/{fid}/documents/refresh", dependencies=[Depends(require_admin)]
)
def documents_refresh(
    fid: int,
    request: NaturalRequest,
    variant_id: int | None = None,
    db: Session = Depends(get_db),
):
    from app.services.discovery import discover_documents
    from app.rag.store import index_variant

    f = get_figure(db, fid)
    v = choose_variant(f, variant_id)
    result = discover_documents(db, f, v, request.query)
    if result["added"]:
        index_variant(db, f, v)
    return result


@router.post("/api/search/natural-language")
def natural(request: NaturalRequest, db: Session = Depends(get_db)):
    from app.services.natural_search import natural_search

    return natural_search(db, request.query)


@router.post("/api/compare")
def compare(request: CompareRequest, db: Session = Depends(get_db)):
    result = []
    for fid in dict.fromkeys(request.figure_ids):
        f = get_figure(db, fid)
        v = choose_variant(f)
        result.append(
            {
                **card(f),
                "prices": price_summary(db, v.id),
                "sources": sources(fid, v.id, db),
            }
        )
    return {
        "items": result,
        "note": "기본 버전 기준 비교. 다른 버전은 상세 화면에서 선택하세요.",
    }


@router.post("/api/rag/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    f = get_figure(db, request.figure_id)
    v = choose_variant(f, request.variant_id)
    from app.rag.graph import answer_question

    return answer_question(db, f, v, request)


@router.get("/api/admin/collection-jobs", dependencies=[Depends(require_admin)])
def jobs(db: Session = Depends(get_db)):
    return [
        serialize(j)
        for j in db.scalars(
            select(CollectionJob).order_by(CollectionJob.id.desc()).limit(100)
        )
    ]


@router.post("/api/admin/reindex", dependencies=[Depends(require_admin)])
def reindex(db: Session = Depends(get_db)):
    from app.rag.store import index_all

    return index_all(db)


@router.get("/api/franchises")
def franchises(db: Session = Depends(get_db)):
    from sqlalchemy import and_
    from app.models.semantics import ProductSemantics
    from app.services.product_semantics import valid_sql

    display = func.coalesce(ProductSemantics.fields["franchise_ko"].as_string(), Figure.franchise)
    rows = db.execute(
        select(display, func.count(Figure.id)).select_from(Figure)
        .outerjoin(ProductSemantics, and_(*valid_sql())).group_by(display)
    ).all()
    groups = {}
    unknown = 0
    for name, count in rows:
        name = (name or "").strip()
        if name:
            groups[name] = groups.get(name, 0) + count
        else:
            unknown += count
    return {
        "items": [
            {"name": name, "count": count} for name, count in sorted(groups.items())
        ],
        "unknown": unknown,
        "total": sum(groups.values()) + unknown,
    }


@router.get("/api/figures/{fid}/semantics")
def product_semantics(fid: int, db: Session = Depends(get_db)):
    from app.services.product_semantics import current, source_of

    f = get_figure(db, fid)
    profile = current(db, f)
    return {"figure_id": fid, "source": source_of(f),
            "status": profile.status if profile else "pending",
            "fields": profile.fields if profile else None,
            "notice": "AI 번역·분류 결과입니다. 원문 근거를 함께 확인하세요."}
