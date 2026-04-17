from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date, datetime

class GuestCreate(BaseModel):
    id: str
    guest_token: str
    tos_accepted: bool
    research_consent: bool
    age_range: str
    gender: str
    nationality: str
    claimed_user_id: str

class GuestDTO(BaseModel):
    id: str
    guest_token: str
    tos_accepted: bool
    research_consent: bool
    age_range: str
    tos_accepted_At: str
    gender: str
    nationality: str
    claimed_user_id: str
    created_at: str
    expires_at: datetime
    triage_left: int = 1