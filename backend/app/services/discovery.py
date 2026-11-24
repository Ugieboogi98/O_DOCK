import hashlib
from urllib.parse import urlparse
from sqlalchemy import select
from bs4 import BeautifulSoup
from app.models.entities import SearchRun, SourceDocument, now
from app.rag.llm import call
from app.rag.prompts import QUERY_PROMPT, SELECT_PROMPT
from app.search_agents.web_search import search
from app.collectors.safe_http import SafeFetcher, CollectionDenied
from app.core.config import get_settings


def discover_documents(db, f, v, question):
    if not get_settings().llm_api_key or not get_settings().search_api_key:
        return {"status": "keys_missing", "added": 0}
    queries = call(
        QUERY_PROMPT,
        {
            "product": f.name_original,
            "manufacturer": f.manufacturer.name,
            "sku": v.sku,
            "question": question,
        },
        True,
    ).get("queries", [])
    if not isinstance(queries, list):
        raise ValueError("BAD_QUERY_RESPONSE")
    added = 0
    fetcher = SafeFetcher()
    for query in [f.name_original] + [str(q)[:300] for q in queries[:3]]:
        cached = db.scalar(
            select(SearchRun).where(
                SearchRun.variant_id == v.id,
                SearchRun.query == query,
                SearchRun.provider == "documents",
            )
        )
        if cached and cached.status == "completed":
            continue
        found = search(query)
        found.insert(
            0,
            {
                "title": f.name_original,
                "url": f.official_url,
                "summary": "Selected product official page",
            },
        )
        unique = {x["url"]: x for x in found if x["url"].startswith("https://")}
        candidates = [{"id": str(i), **x} for i, x in enumerate(unique.values())]
        selected = call(
            SELECT_PROMPT, {"product": f.name_original, "candidates": candidates}, True
        ).get("ids", [])
        selected = set(str(i) for i in selected)
        selected.add("0")
        urls = []
        blocked = []
        for item in candidates:
            if item["id"] not in selected:
                continue
            if db.scalar(
                select(SourceDocument).where(
                    SourceDocument.variant_id == v.id, SourceDocument.url == item["url"]
                )
            ):
                urls.append(item["url"])
                continue
            try:
                html = fetcher.fetch(item["url"])
                soup = BeautifulSoup(html, "html.parser")
                for node in soup(["script", "style", "nav", "footer", "header"]):
                    node.decompose()
                body = (soup.find("main") or soup).get_text(" ", strip=True)[:20000]
                if not body:
                    continue
                d = SourceDocument(
                    variant_id=v.id,
                    title=item["title"],
                    url=item["url"],
                    body=body,
                    source_type="external_html",
                    language="und",
                    content_hash=hashlib.sha256(body.encode()).hexdigest(),
                    usage_status="operator_authorized",
                )
                db.add(d)
                urls.append(item["url"])
                added += 1
            except (CollectionDenied, httpx.HTTPError, ValueError, KeyError):
                blocked.append(item["url"])
        run = cached or SearchRun(variant_id=v.id, query=query, provider="documents")
        run.status = "partial" if blocked else "completed"
        run.payload = {"selected_urls": urls, "blocked_urls": blocked}
        run.executed_at = now()
        db.add(run)
        db.commit()
    return {"status": "completed", "added": added}


import httpx
