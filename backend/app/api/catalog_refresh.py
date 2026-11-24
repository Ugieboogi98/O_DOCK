"""Public progress reads and administrator-only bounded refresh."""

from fastapi import APIRouter, Depends
from app.core.security import require_admin
from app.services.catalog_refresh import refresh_status, start_refresh

router = APIRouter(prefix="/api/catalog", tags=["catalog"])


@router.get("/status")
def catalog_status():
    return refresh_status()


@router.post("/refresh", dependencies=[Depends(require_admin)])
def catalog_refresh():
    return start_refresh()
