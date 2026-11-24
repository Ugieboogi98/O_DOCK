"""Administrator product-name edits and source description reads."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_admin, require_same_origin
from app.repositories.figures import get_figure

router = APIRouter(prefix="/api", tags=['product-text'])


class NameInput(BaseModel):
    name_ko: str = Field(min_length=1, max_length=500)


@router.put("/figures/{fid}/korean-name", dependencies=[Depends(require_admin), Depends(require_same_origin)])
def korean_name(fid: int, data: NameInput, db: Session = Depends(get_db)):
    f = get_figure(db, fid)
    if not data.name_ko.strip():
        raise HTTPException(422, "한국어 이름을 입력하세요.")
    f.name_ko = data.name_ko.strip()
    db.commit()
    return {"name_ko": f.name_ko}


@router.post("/figures/{fid}/translate", dependencies=[Depends(require_admin), Depends(require_same_origin)])
def translate(fid: int, db: Session = Depends(get_db)):
    from app.services.enrichment import translate_name

    f = get_figure(db, fid)
    try:
        status = translate_name(db, f)
    except Exception as exc:
        reason = getattr(exc, "reason", "")
        messages = {
            "QUOTA_EXHAUSTED": "번역 API의 잔액 또는 할당량이 부족합니다. 공급자 대시보드를 확인하세요.",
            "RATE_LIMIT_EXHAUSTED": "번역 API 요청 제한이 계속되어 중단했습니다. 잠시 후 다시 시도하세요.",
            "LLM_API_KEY_REQUIRED": "번역 API 키가 설정되어 있지 않습니다.",
            "AUTH_OR_PERMISSION_ERROR": "번역 API 키 또는 사용 권한을 확인하세요.",
            "MODEL_OR_ENDPOINT_NOT_FOUND": "번역 모델 이름 또는 API 주소를 확인하세요.",
            "RETRY_AFTER_REQUIRES_LATER_RUN": "공급자가 대기를 요청했습니다. 나중에 다시 시도하세요.",
        }
        raise HTTPException(
            422,
            messages.get(
                reason, "번역에 실패했습니다. API 설정과 응답 형식을 확인하세요."
            ),
        ) from None
    return {"name_ko": f.name_ko, "status": status}


@router.get("/figures/{fid}/description")
def description(fid: int, variant_id: int, db: Session = Depends(get_db)):
    from app.models.entities import SourceDocument

    f = get_figure(db, fid)
    if variant_id not in [v.id for v in f.variants]:
        raise HTTPException(404, "제품 버전 없음")
    doc = db.scalar(
        select(SourceDocument)
        .where(
            SourceDocument.variant_id == variant_id,
            SourceDocument.source_type == "official_detail",
        )
        .order_by(SourceDocument.collected_at.desc())
    )
    return {"body": doc.body if doc else "", "source_url": doc.url if doc else None}
