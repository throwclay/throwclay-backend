# apps/api/app/schemas/studio.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class StudioOut(BaseModel):
    id: UUID
    name: str
    subdomain: str
    timezone: str
    created_at: datetime
