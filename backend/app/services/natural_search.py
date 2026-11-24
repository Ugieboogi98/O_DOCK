import re
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import select
from app.models.entities import Manufacturer
from app.rag.llm import call
from app.rag.prompts import NATURAL_PROMPT
from app.core.config import get_settings
from app.repositories.figures import list_figures


class Filters(BaseModel):
    model_config = ConfigDict(extra="ignore")
    q: str | None = None
    manufacturer_id: int | None = None
    product_line_id: int | None = None
    scale: str | None = None
    year: int | None = Field(default=None, ge=1950, le=2100)
    height_max: int | None = Field(default=None, ge=1, le=10000)
    height_min: int | None = Field(default=None, ge=0, le=10000)
    franchise: str | None = None
    character: str | None = None
    unsupported: list[str] = []


def natural_search(db, query):
    makers = list(db.scalars(select(Manufacturer)))
    if get_settings().llm_api_key:
        filters = Filters.model_validate(
            call(
                NATURAL_PROMPT,
                {
                    "query": query,
                    "manufacturers": [
                        {"id": m.id, "name": m.name, "name_ko": m.name_ko}
                        for m in makers
                    ],
                },
                True,
            )
        )
    else:
        text = query
        data = {}
        for m in makers:
            for name in [m.name, m.name_ko]:
                if name.lower() in text.lower():
                    data["manufacturer_id"] = m.id
                    text = re.sub(re.escape(name), "", text, flags=re.I)
        match = re.search(
            r"(\d+(?:\.\d+)?)\s*(cm|mm|센티|밀리)\s*(이하|미만|이상|초과)", text, re.I
        )
        if match:
            amount = float(match[1]) * (10 if match[2].lower() in ["cm", "센티"] else 1)
            op = match[3]
            data["height_max" if op in ["이하", "미만"] else "height_min"] = int(
                amount
            ) + (-1 if op == "미만" else 1 if op == "초과" else 0)
            text = text.replace(match[0], "")
        match = re.search(r"(20\d{2})년(?:에)?", text)
        if match:
            data["year"] = int(match[1])
            text = text.replace(match[0], "")
        match = re.search(r"1\s*/\s*\d+", text)
        if match:
            data["scale"] = match[0].replace(" ", "")
            text = text.replace(match[0], "")
        unsupported = bool(re.search(r"원|엔|저렴|비싼|색상|빨간|파란|미개봉", text))
        text = re.sub(
            r"스케일|피규어|제품|찾아줘|보여줘|알려줘|추천해줘|나온|출시된|이며|이고|높이|키가",
            " ",
            text,
        )
        data["q"] = text.strip(" ,.") or None
        data["unsupported"] = (
            ["가격·색상·상태 조건은 키 없는 자동 파서에서 지원하지 않습니다."]
            if unsupported
            else []
        )
        filters = Filters(**data)
    if filters.manufacturer_id and filters.manufacturer_id not in [
        m.id for m in makers
    ]:
        filters.unsupported.append("제조사 식별 실패")
    args = filters.model_dump(exclude={"unsupported"}, exclude_none=True)
    if filters.unsupported:
        return {
            "items": [],
            "total": 0,
            "filters": args,
            "warnings": filters.unsupported,
        }
    result = list_figures(db, **args)
    return {
        **result,
        "filters": args,
        "warnings": (
            [
                "API 키 없는 규칙 기반 조건 검색입니다. 한국어 별칭이 없는 제품은 원문명으로 검색하세요."
            ]
            if not get_settings().llm_api_key
            else []
        ),
    }
