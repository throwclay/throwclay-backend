# apps/api/app/services/studios.py
from fastapi import HTTPException
from psycopg import AsyncConnection
from ..repositories.studios import StudioRepository
from ..schemas.studio import StudioIn

class StudioService:
    def __init__(self, conn: AsyncConnection, statement_timeout_ms: int = 3000):
        self.repo = StudioRepository(conn)
        self.conn = conn
        self.stmt_timeout = statement_timeout_ms

    async def get_by_subdomain(self, subdomain: str):
        return await self.repo.get_by_subdomain(subdomain)

    async def create(self, payload: StudioIn) -> dict:
        # Example business rule: unique subdomain (409 if taken)
        if await self.repo.exists_subdomain(payload.subdomain):
            raise HTTPException(status_code=409, detail="Subdomain already in use")

        # If we add multi-table work later, wrap in a transaction:
        # async with self.conn.transaction():
        created = await self.repo.insert(
            name=payload.name,
            subdomain=payload.subdomain,
            timezone=payload.timezone,
        )
        return created

    async def list(self, *, limit: int, offset: int) -> tuple[list[dict], int, int | None]:
        data = await self.repo.list(limit=limit, offset=offset)
        total = await self.repo.count_all()
        next_offset = offset + limit if (offset + limit) < total else None
        return data, total, next_offset