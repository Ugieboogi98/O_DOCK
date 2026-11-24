import re

PATTERN = re.compile(r"\[근거\s*(\d+)\]")


def cited_sources(answer, evidence):
    numbers = list(dict.fromkeys(int(x) for x in PATTERN.findall(answer)))
    invalid = any(n < 1 or n > len(evidence) for n in numbers)
    if invalid:
        return "문서에서 확인되지 않음. 생성된 인용 번호를 검증하지 못했습니다.", []
    sources = [
        {"number": n, **{k: v for k, v in evidence[n - 1].items() if k != "text"}}
        for n in numbers
    ]
    if not sources and "문서에서 확인되지 않음" not in answer:
        return (
            "문서에서 확인되지 않음. 검증 가능한 인용이 없는 답변을 표시하지 않았습니다.",
            [],
        )
    return answer, sources
