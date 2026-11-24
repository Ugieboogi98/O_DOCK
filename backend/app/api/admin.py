"""Administrator session check and the one-click data pipeline."""
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.security import require_admin, require_same_origin
from app.services import master_pipeline

router = APIRouter(prefix='/api/admin', tags=['admin'])


@router.get('/session', dependencies=[Depends(require_admin)])
def session():
    return {'admin': True}


class PipelineRun(BaseModel):
    steps: list[Literal['catalog', 'semantics', 'events', 'verify']] | None = None


@router.get('/pipeline', dependencies=[Depends(require_admin)])
def pipeline_status():
    return master_pipeline.status()


@router.post('/pipeline/run', dependencies=[Depends(require_admin), Depends(require_same_origin)])
def pipeline_run(body: PipelineRun | None = None):
    try:
        return master_pipeline.start((body.steps if body else None) or None)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
