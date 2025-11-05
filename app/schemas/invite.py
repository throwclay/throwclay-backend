# apps/api/app/schemas/invite.py
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class InviteIn(BaseModel):
    email: EmailStr
    role: str  # 'admin' | 'staff' | 'member'

class MembershipOut(BaseModel):
    studio_id: UUID
    user_id: UUID
    role: str
    status: str
    invited_by: UUID | None = None
    created_at: datetime
