from typing import Optional

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date, datetime


class GuestBase(BaseModel):
    id: Optional[str] = None
    guest_token: Optional[str] = None
    tos_accepted: bool
    research_consent: bool
    age_range: str
    gender: str
    nationality: str
    claimed_user_id: Optional[str] = None
    tos_accepted_At: Optional[str] = None
    created_at: Optional[str] = None
    expires_at: Optional[datetime] = None
    triage_left: Optional[int] = 1


class GuestResponse(BaseModel):
    guest_token: Optional[str] = None
    expires_at: Optional[datetime] = None
