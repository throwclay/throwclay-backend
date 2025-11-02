# apps/api/app/routers/studios.py
from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection
from ..db import get_conn
from ..schemas.studio import StudioOut
from ..services.studios import StudioService
from ..settings import settings

router = APIRouter(prefix="/api/studios", tags=["studios"])

def get_service(conn: AsyncConnection = Depends(get_conn)) -> StudioService:
    return StudioService(conn, statement_timeout_ms=settings.db_statement_timeout_ms)

@router.get("/{subdomain}", response_model=StudioOut)
async def get_studio(subdomain: str, svc: StudioService = Depends(get_service)):
    studio = await svc.get_by_subdomain(subdomain)
    if not studio:
        raise HTTPException(status_code=404, detail="Studio not found")
    return studio

@router.get("", response_model=list[StudioOut])
async def list_studios(limit: int = 50, offset: int = 0, svc: StudioService = Depends(get_service)):
    return await svc.list(limit, offset)
