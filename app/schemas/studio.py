# apps/api/app/schemas/studio.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class StudioOut(BaseModel):
    id: UUID
    name: str
    subdomain: str
    timezone: str
    payment_provider: str | None = None
    payment_account_ref: str | None = None
    payment_settings: dict | None = None
    created_at: datetime
