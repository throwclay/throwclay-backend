# apps/api/app/routers/studios.py
from fastapi import APIRouter, Depends, HTTPException
from psycopg import AsyncConnection
from ..db import get_conn
from ..schemas.studio import StudioOut, StudioIn
from ..schemas.pagination import Page, PageMeta
from ..services.studios import StudioService
from ..settings import settings
from ..auth.roles import require_roles_any

router = APIRouter(prefix="/api/studios", tags=["studios"])

def get_service(conn: AsyncConnection = Depends(get_conn)) -> StudioService:
    return StudioService(conn, statement_timeout_ms=settings.db_statement_timeout_ms)

@router.get("/{subdomain}", response_model=StudioOut)
async def get_studio(subdomain: str, svc: StudioService = Depends(get_service)):
    studio = await svc.get_by_subdomain(subdomain)
    if not studio:
        raise HTTPException(status_code=404, detail="Studio not found")
    return studio

@router.get("", response_model=Page)  # returns { data: [...], pagination: {...} }
async def list_studios(limit: int = 20, offset: int = 0, svc: StudioService = Depends(get_service)):
    data, total, next_offset = await svc.list(limit=limit, offset=offset)
    return Page(
        data=[StudioOut(**s) for s in data],
        pagination=PageMeta(limit=limit, offset=offset, total=total, next_offset=next_offset),
    )

@router.post("", response_model=StudioOut, status_code=201)  # admin/owner only
async def create_studio(
    payload: StudioIn,
    svc: StudioService = Depends(get_service),
    user = Depends(require_roles_any("admin", "owner")),
):
    return await svc.create(payload)
