# apps/api/app/schemas/pagination.py
from pydantic import BaseModel

class PageMeta(BaseModel):
    limit: int
    offset: int
    total: int
    next_offset: int | None = None  # null when we on the last page

class Page(BaseModel):
    data: list  # we’ll specialize this in routers
    pagination: PageMeta
