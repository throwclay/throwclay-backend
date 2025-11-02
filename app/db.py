# apps/api/app/db.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from .settings import settings

POOL: AsyncConnectionPool | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global POOL
    POOL = AsyncConnectionPool(
        conninfo=settings.database_url,
        min_size=settings.db_pool_min,
        max_size=settings.db_pool_max,
        open=False
    )
    await POOL.open()
    try:
        yield
    finally:
        await POOL.close()

async def get_conn(request: Request):
    # yields a connection tied to the request lifecycle
    async with POOL.connection() as conn:  # type: ignore[arg-type]
        yield conn

def dict_cursor(conn):
    # small helper so repos can do: async with dict_cursor(conn) as cur:
    return conn.cursor(row_factory=dict_row)
