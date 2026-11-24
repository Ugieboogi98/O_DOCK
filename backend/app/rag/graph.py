import time, re
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from app.core.config import get_settings
from app.rag.store import retrieve
from app.rag.llm import call
from app.rag.prompts import ANSWER_PROMPT
from app.rag.citations import cited_sources
from app.services.prices import price_summary, used_summary


class RagState(TypedDict, total=False):
    question: str
    history: list
    evidence: list
    warnings: list
    answer: str
    sources: list
    mode: str
    top_k: int


def factual_answer(f, v, q):
    requested = []
    for tokens, label, value in [
        (
            ["높이", "크기", "height"],
            "높이",
            f"{f.height_mm} mm" if f.height_mm else None,
        ),
        (["재질", "material"], "재질", f.material),
        (["제조사", "manufacturer"], "제조사", f.manufacturer.name),
        (["스케일", "scale"], "스케일", f.scale),
        (["발매일", "출시일", "release date"], "발매일", v.release_date),
    ]:
        if any(t in q.lower() for t in tokens):
            requested.append(
                f"{label}: {value} [근거 1]"
                if value
                else f"{label}: 문서에서 확인되지 않음"
            )
    return (
        "\n".join(requested)
        if requested
        else "문서에서 확인되지 않음. API 키 없는 모드에서는 높이·재질·제조사·스케일·발매일만 조회할 수 있습니다."
    )


def build_graph(db, f, v):
    def retrieve_node(state):
        evidence, warnings = retrieve(
            db, f, v, state["question"], state["top_k"], state["mode"]
        )
        # Price facts enter context only as verified observations with their actual source URLs.
        if re.search(r"가격|시세|price|중고", state["question"], re.I):
            p = price_summary(db, v.id)
            for r in p["release_prices"]:
                evidence.append(
                    {
                        "id": f"release:{r['id']}",
                        "title": f.name_original + " 공식 표시 가격",
                        "url": r["source_url"],
                        "source_type": "price_observation",
                        "text": f"종류 {r['price_kind']}; 금액 {r['price_amount']} {r['currency']}; 확인 {r['checked_at']}; 최초 발매가인지 종류 필드 확인",
                    }
                )
            for r in p["retail_prices"]:
                if r["match_status"] == "MATCHED" and not r["stale"]:
                    evidence.append(
                        {
                            "id": f"retail:{r['id']}",
                            "title": r["retailer"],
                            "url": r["product_url"],
                            "source_type": "price_observation",
                            "text": f"{r['amount']} {r['currency']}; {r['availability']}; 배송비 제외; 확인 {r['observed_at']}",
                        }
                    )
            u = used_summary(db, v.id)
            for r in u["listings"]:
                if (
                    r["match_status"] == "MATCHED"
                    and not r["is_set"]
                    and not r["stale"]
                ):
                    evidence.append(
                        {
                            "id": f"used:{r['id']}",
                            "title": r["platform"] + " 중고 매물",
                            "url": r["listing_url"],
                            "source_type": "used_asking_price",
                            "text": f"판매 희망가 {r['asking_price']} {r['currency']}; 상태 {r['condition']}; 판매 상태 {r['listing_status']}; 확인 {r['observed_at']}; 검증된 실거래가 아님",
                        }
                    )
        return {"evidence": evidence, "warnings": warnings}

    def generate_node(state):
        if get_settings().llm_api_key:
            evidence = [{"number": i + 1, **x} for i, x in enumerate(state["evidence"])]
            answer = call(
                ANSWER_PROMPT,
                {
                    "question": state["question"],
                    "history": state.get("history", [])[:12],
                    "evidence": evidence,
                },
            )
        else:
            answer = factual_answer(f, v, state["question"])
            state["warnings"].append(
                "LLM API 키가 없어 정형 데이터 조회 모드로 응답했습니다."
            )
        answer, sources = cited_sources(answer, state["evidence"])
        return {"answer": answer, "sources": sources, "warnings": state["warnings"]}

    graph = StateGraph(RagState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()


def answer_question(db, f, v, request):
    start = time.perf_counter()
    result = build_graph(db, f, v).invoke(
        {
            "question": request.question,
            "history": request.history,
            "top_k": request.top_k or get_settings().top_k,
            "mode": request.mode,
        }
    )
    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "warnings": result["warnings"],
        "elapsed_ms": round((time.perf_counter() - start) * 1000),
        "mode": "llm_rag" if get_settings().llm_api_key else "structured_lookup",
        "embedding_provider": get_settings().embedding_provider,
        "retrieved_count": len(result["evidence"]),
    }
