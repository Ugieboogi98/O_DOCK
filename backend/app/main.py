"""Application composition. Business rules belong to services and collectors."""

import logging
import mimetypes
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import get_settings
from app.api.catalog import router as catalog_api
from app.api.admin import router as admin_api
from app.api.accounts import router as accounts_api
from app.api.personal import router as personal_api
from app.api.korea_prices import router as korea_api
from app.api.catalog_refresh import router as refresh_api
from app.api.korean import router as korean_api
from app.api.pricing import router as pricing_api
from app.api.product_text import router as product_text_api
from app.api.events import router as events_api
from app.api.retail_offers import router as retail_offers_api

app = FastAPI(title="O_DOCK", version="1.1.0")
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "X-Admin-Token"],
)
routers = (
    catalog_api,
    accounts_api,
    admin_api,
    personal_api,
    pricing_api,
    korea_api,
    product_text_api,
    refresh_api,
    korean_api,
    events_api,
    retail_offers_api,
)
for router in routers:
    app.include_router(router)
settings.media_dir.mkdir(parents=True, exist_ok=True)
mimetypes.add_type('image/webp', '.webp')
app.mount("/api/media", StaticFiles(directory=settings.media_dir), name="media")


@app.middleware('http')
async def private_api_cache_policy(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith('/api/') and not request.url.path.startswith('/api/media/'):
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.exception_handler(Exception)
def unexpected_error(request, exc):
    logging.getLogger("odock").error(
        "request_failed type=%s path=%s", type(exc).__name__, request.url.path
    )
    return JSONResponse(
        status_code=503, content={"detail": "서비스 처리 실패. 서버 로그를 확인하세요."}
    )
