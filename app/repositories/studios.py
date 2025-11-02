# apps/api/app/repositories/studios.py
from typing import Any, Optional
from psycopg import AsyncConnection
from ..db import dict_cursor

class StudioRepository:
    def __init__(self, conn: AsyncConnection, statement_timeout_ms: int = 3000):
        self.conn = conn
        self.stmt_timeout = statement_timeout_ms

    async def get_by_subdomain(self, subdomain: str):
        async with dict_cursor(self.conn) as cur:
            # was: await cur.execute("SET LOCAL statement_timeout = %s", (self.stmt_timeout,))
            await cur.execute(f"SET statement_timeout = {int(self.stmt_timeout)}")
            await cur.execute(
                """
                select id, name, subdomain, timezone,
                    payment_provider, payment_account_ref, payment_settings,
                    created_at
                from public.studio
                where subdomain = %s
                limit 1
                """,
                (subdomain.lower(),),
            )
            return await cur.fetchone()

    async def list(self, limit: int = 50, offset: int = 0) -> list[dict]:
        async with dict_cursor(self.conn) as cur:
            await cur.execute(f"SET statement_timeout = {int(self.stmt_timeout)}")
            await cur.execute(
                """
                select id, name, subdomain, timezone,
                       payment_provider, payment_account_ref, payment_settings,
                       created_at
                from public.studio
                order by created_at desc
                limit %s offset %s
                """,
                (limit, offset),
            )
            return await cur.fetchall()
