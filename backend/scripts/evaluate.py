"""Real paid RAG/no-RAG comparison; requires user-configured LLM key. Never generates fake scores."""

import argparse, json, time
from pathlib import Path
from sqlalchemy import select
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.rag.llm import call
from app.rag.graph import answer_question
from app.schemas.requests import ChatRequest

QUESTIONS = [
    "이 제품의 제조사는?",
    "공식 높이는 몇 mm인가?",
    "재질은 무엇인가?",
    "일본 공식 최초 발매가는?",
    "내년 중고 가격이 얼마인지 확정할 수 있나?",
]
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--figure-id", type=int, required=True)
    p.add_argument("--out", default="../docs/rag-evaluation.json")
    a = p.parse_args()
    if not get_settings().llm_api_key:
        raise SystemExit("LLM_API_KEY를 설정해야 실제 비교를 실행할 수 있습니다.")
    with SessionLocal() as db:
        f = db.get(Figure, a.figure_id)
        if not f:
            raise SystemExit("제품 ID를 확인하세요.")
        results = []
        for q in QUESTIONS:
            start = time.perf_counter()
            baseline = call(
                "피규어 질문에 한국어로 답하세요. 모르면 모른다고 답하세요.",
                {"product": f.name_original, "question": q},
            )
            elapsed = round((time.perf_counter() - start) * 1000)
            rag = answer_question(
                db, f, f.variants[0], ChatRequest(figure_id=f.id, question=q)
            )
            results.append(
                {
                    "question": q,
                    "without_rag": baseline,
                    "without_rag_ms": elapsed,
                    "with_rag": rag,
                    "human_accuracy": None,
                    "human_citation_correctness": None,
                    "human_abstention_correctness": None,
                }
            )
        Path(a.out).write_text(
            json.dumps(
                {"figure_id": f.id, "results": results}, ensure_ascii=False, indent=2
            )
        )
