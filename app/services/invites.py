# apps/api/app/services/invites.py
from fastapi import HTTPException
from psycopg import AsyncConnection
from ..repositories.memberships import MembershipRepository
from ..repositories.studios import StudioRepository
from ..lib.supabase_admin import admin_create_user, admin_invite_user

class InviteService:
    def __init__(self, conn: AsyncConnection):
        self.conn = conn
        self.memberships = MembershipRepository(conn)
        self.studios = StudioRepository(conn)

    async def invite(self, *, subdomain: str, email: str, role: str, invited_by_user_id: str) -> dict:
        studio = await self.studios.get_by_subdomain(subdomain)
        if not studio:
            raise HTTPException(status_code=404, detail="Studio not found")

        # Create user (or capture "already exists")
        try:
            u = await admin_create_user(email)
            user_id = u["id"]
        except Exception as e:
            # If already exists, you can prompt accept flow or (optionally) fetch by email if your GoTrue version allows.
            raise HTTPException(status_code=400, detail="Unable to create/invite user") from e

        # Optionally send an invite email via GoTrue (magic link)
        try:
            await admin_invite_user(email)
        except Exception:
            # Non-fatal; membership can still be created. You might log this.
            pass

        # Upsert membership as 'invited'
        membership = await self.memberships.upsert_invite(
            studio_id=str(studio["id"]),
            user_id=user_id,
            role=role,
            invited_by=invited_by_user_id,
        )
        return membership

    async def accept(self, *, subdomain: str, current_user_id: str) -> dict:
        studio = await self.studios.get_by_subdomain(subdomain)
        if not studio:
            raise HTTPException(status_code=404, detail="Studio not found")

        row = await self.memberships.activate(studio_id=str(studio["id"]), user_id=current_user_id)
        if not row:
            raise HTTPException(status_code=404, detail="Invite not found")
        return row
