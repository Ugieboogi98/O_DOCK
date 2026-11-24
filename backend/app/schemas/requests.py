from typing import Literal
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    figure_id: int = Field(gt=0)
    variant_id: int | None = Field(default=None, gt=0)
    question: str = Field(min_length=1, max_length=2000)
    top_k: int | None = Field(default=None, ge=1, le=15)
    mode: Literal["similarity", "mmr"] = "similarity"
    history: list[dict[str, str]] = Field(default_factory=list, max_length=12)


class NaturalRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)


class CompareRequest(BaseModel):
    figure_ids: list[int] = Field(min_length=2, max_length=4)
