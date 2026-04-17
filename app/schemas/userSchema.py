from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date, datetime

class UserDTO(BaseModel):
    id:str
    name: str
    email_enc: str
    phone_enc: str
    dob_enc: str
    prefered_language:str
    age_range:str
    gender:str
    nationality:str
    research_consent:bool
    consent_given_at: datetime # backend will generate
    triage_count:int # backend will generate
    role:str
    created_at:str # backend will generate

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    dob: str
    prefered_language:str
    age_range:str
    gender:str
    nationality:str
    research_consent:bool
    role:str
    tos_accepted: bool
