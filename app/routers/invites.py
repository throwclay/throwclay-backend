# apps/api/app/routers/invites.py
from fastapi import APIRouter, Depends
from psycopg import AsyncConnection
from ..db import get_conn
from ..auth.roles import require_roles_any
from ..auth.deps import get_current_user
from ..schemas.invite import InviteIn, MembershipOut
from ..services.invites import InviteService

router = APIRouter(prefix="/api/studios/{subdomain}/invites", tags=["invites"])

def get_service(conn: AsyncConnection = Depends(get_conn)) -> InviteService:
    return InviteService(conn)

@router.post("", response_model=MembershipOut, dependencies=[Depends(require_roles_any("owner","admin"))])
async def invite_user(subdomain: str, payload: InviteIn, svc: InviteService = Depends(get_service), user=Depends(get_current_user)):
    return await svc.invite(subdomain=subdomain, email=payload.email, role=payload.role, invited_by_user_id=user.id)

@router.post("/accept", response_model=MembershipOut)
async def accept_invite(subdomain: str, svc: InviteService = Depends(get_service), user=Depends(get_current_user)):
    return await svc.accept(subdomain=subdomain, current_user_id=user.id)
