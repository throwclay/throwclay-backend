# apps/api/app/repositories/studios.py
from typing import Any, Optional
from psycopg import AsyncConnection
from ..db import dict_cursor

class StudioRepository:
    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def get_by_subdomain(self, subdomain: str) -> Optional[dict[str, Any]]:
        async with dict_cursor(self.conn) as cur:
            await cur.execute(
                """
                select id, name, subdomain, timezone, created_at
                from public.studio
                where subdomain = %s
                limit 1
                """,
                (subdomain.lower(),),
            )
            return await cur.fetchone()

    async def exists_subdomain(self, subdomain: str) -> bool:
        async with dict_cursor(self.conn) as cur:
            await cur.execute("select 1 from public.studio where subdomain = %s", (subdomain.lower(),))
            return (await cur.fetchone()) is not None

    async def insert(self, *, name: str, subdomain: str, timezone: str) -> dict[str, Any]:
        async with dict_cursor(self.conn) as cur:
            await cur.execute(
                """
                insert into public.studio (name, subdomain, timezone)
                values (%s, %s, %s)
                returning id, name, subdomain, timezone, created_at
                """,
                (name, subdomain.lower(), timezone),
            )
            return await cur.fetchone()
