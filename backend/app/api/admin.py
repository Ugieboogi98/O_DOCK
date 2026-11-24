"""Verify an existing server token without starting any catalog jobs."""
from fastapi import APIRouter, Depends
from app.core.security import require_admin

router = APIRouter(prefix='/api/admin', tags=['admin'])


@router.get('/session', dependencies=[Depends(require_admin)])
def session():
    return {'admin': True}
