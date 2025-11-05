# apps/api/app/repositories/memberships.py
from typing import Any, Optional
from psycopg import AsyncConnection
from ..db import dict_cursor

class MembershipRepository:
    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def upsert_invite(self, *, studio_id: str, user_id: str, role: str, invited_by: str) -> dict[str, Any]:
        async with dict_cursor(self.conn) as cur:
            await cur.execute(
                """
                insert into public.studio_membership (studio_id, user_id, role, status, invited_by)
                values (%s, %s, %s, 'invited', %s)
                on conflict (studio_id, user_id)
                do update set role = excluded.role, status = 'invited', invited_by = excluded.invited_by
                returning studio_id, user_id, role, status, invited_by, created_at
                """,
                (studio_id, user_id, role, invited_by),
            )
            return await cur.fetchone()

    async def activate(self, *, studio_id: str, user_id: str) -> Optional[dict[str, Any]]:
        async with dict_cursor(self.conn) as cur:
            await cur.execute(
                """
                update public.studio_membership
                   set status = 'active'
                 where studio_id = %s and user_id = %s and status in ('invited','pending')
                returning studio_id, user_id, role, status, invited_by, created_at
                """,
                (studio_id, user_id),
            )
            return await cur.fetchone()
