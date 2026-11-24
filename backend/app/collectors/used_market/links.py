from urllib.parse import quote
import re


def search_links(query, name_ko=None):
    original = (query or "").strip()
    korean = (name_ko or "").strip()
    japanese = (
        original
        if re.search(r"[\u3040-\u30ff\u3400-\u9fff]", original)
        and not re.search(r"[가-힣]", original)
        else ""
    )
    markets = [
        ("메루카리", "JPY", "ja", japanese, "https://jp.mercari.com/search?keyword="),
        ("중고나라", "KRW", "ko", korean, "https://web.joongna.com/search/"),
        ("번개장터", "KRW", "ko", korean, "https://m.bunjang.co.kr/search/products?q="),
        ("당근", "KRW", "ko", korean, "https://www.daangn.com/search/"),
    ]
    return [
        {
            "name": name,
            "currency": currency,
            "language": language,
            "query": term,
            "url": prefix + quote(term, safe="") if term else None,
            "available": bool(term),
            "reason": (
                None
                if term
                else ("일본어 원문 필요" if language == "ja" else "한국어 번역 필요")
            ),
        }
        for name, currency, language, term, prefix in markets
    ]
