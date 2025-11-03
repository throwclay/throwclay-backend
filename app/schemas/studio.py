# apps/api/app/schemas/studio.py
from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime
import re

SUBDOMAIN_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$")

class StudioIn(BaseModel):
    name: str
    subdomain: str
    timezone: str = "America/Los_Angeles"

    @field_validator("subdomain")
    @classmethod
    def validate_subdomain(cls, v: str) -> str:
        vv = v.strip().lower()
        if not SUBDOMAIN_RE.match(vv):
            raise ValueError("Invalid subdomain (use a–z, 0–9, hyphen; must start/end alphanumeric; max 63)")
        return vv

class StudioOut(BaseModel):
    id: UUID
    name: str
    subdomain: str
    timezone: str
    created_at: datetime
