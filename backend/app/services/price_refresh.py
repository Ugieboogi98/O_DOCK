from datetime import timedelta
from urllib.parse import urlparse
from sqlalchemy import select
from fastapi import HTTPException
from app.models.entities import SearchRun, Retailer, RetailPriceRecord, now
from app.core.config import get_settings
from app.search_agents.web_search import search
from app.search_agents.matching import match_product
from app.collectors.safe_http import SafeFetcher
from app.collectors.retailers.jsonld import parse_offers
from app.rag.llm import call
from app.rag.prompts import QUERY_PROMPT


def refresh_prices(db, f, v):
    s = get_settings()
    query = f'{f.name_original} {v.sku or ""} 피규어 가격 구매'
    run = db.scalar(
        select(SearchRun).where(
            SearchRun.variant_id == v.id,
            SearchRun.query == query,
            SearchRun.provider == "prices",
        )
    )
    if run and run.executed_at > now() - timedelta(minutes=s.price_cache_minutes):
        return {"cached": True, **run.payload}
    if not s.search_api_key:
        raise HTTPException(503, "가격 검색에는 SEARCH_API_KEY가 필요합니다.")
    if s.llm_api_key:
        out = call(
            QUERY_PROMPT,
            {
                "product": f.name_original,
                "sku": v.sku,
                "question": "한국 신품 판매처 가격 검색",
            },
            True,
        )
        extra = [str(x)[:300] for x in out.get("queries", [])[:2]]
    else:
        extra = []
    candidates = {}
    errors = 0
    count = 0
    for q in [query] + extra:
        for c in search(q):
            candidates[c["url"]] = c
    fetcher = SafeFetcher()
    target = {
        "manufacturer": f.manufacturer.name,
        "sku": v.sku,
        "jan_code": v.jan_code,
        "edition": v.edition,
        "scale": f.scale,
        "reissue_no": v.reissue_no,
    }
    for url, c in candidates.items():
        c["status"] = "link_only"
        try:
            html = fetcher.fetch(url)
            offers = parse_offers(html, url)
            for o in offers:
                if o["currency"] != "KRW":
                    continue
                match = match_product(target, o)
                host = urlparse(url).hostname
                retailer = db.scalar(
                    select(Retailer).where(Retailer.site_url == "https://" + host)
                )
                if not retailer:
                    retailer = Retailer(
                        name=host, site_url="https://" + host, seller_type="unverified"
                    )
                    db.add(retailer)
                    db.flush()
                db.add(
                    RetailPriceRecord(
                        variant_id=v.id,
                        retailer_id=retailer.id,
                        price_type=o["price_type"],
                        amount=o["amount"],
                        currency="KRW",
                        shipping=o["shipping"],
                        availability=o["availability"],
                        match_status=match,
                        product_url=url,
                    )
                )
                count += 1
                c["status"] = match
        except Exception:
            errors += 1
            c["status"] = "unavailable_or_permission_required"
    payload = {
        "candidates": list(candidates.values()),
        "observations_added": count,
        "unavailable": errors,
        "checked_at": now().isoformat(),
    }
    run = run or SearchRun(variant_id=v.id, query=query, provider="prices")
    run.status = "completed"
    run.payload = payload
    run.executed_at = now()
    db.add(run)
    db.commit()
    return {"cached": False, **payload}
