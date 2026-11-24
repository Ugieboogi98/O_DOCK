import httpx
from app.core.config import get_settings


def search(query):
    s = get_settings()
    if not s.search_api_key:
        raise ValueError("SEARCH_KEY_MISSING")
    # Brave's public documented search endpoint; snippets are discovery, never price evidence.
    with httpx.Client(timeout=s.request_timeout) as c:
        r = c.get(
            "https://api.search.brave.com/res/v1/web/search",
            params={"q": query, "count": 8},
            headers={
                "X-Subscription-Token": s.search_api_key,
                "Accept": "application/json",
            },
        )
        r.raise_for_status()
    return [
        {
            "title": x.get("title", ""),
            "url": x["url"],
            "summary": x.get("description", ""),
        }
        for x in r.json().get("web", {}).get("results", [])
    ]
