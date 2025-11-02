# apps/api/app/services/studios.py
from psycopg import AsyncConnection
from ..repositories.studios import StudioRepository

class StudioService:
    def __init__(self, conn: AsyncConnection, statement_timeout_ms: int = 3000):
        self.repo = StudioRepository(conn, statement_timeout_ms)

    async def get_by_subdomain(self, subdomain: str):
        # place for extra logic (e.g., access checks, transforms)
        return await self.repo.get_by_subdomain(subdomain)

    async def list(self, limit: int = 50, offset: int = 0):
        return await self.repo.list(limit=limit, offset=offset)
