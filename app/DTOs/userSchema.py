from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date, datetime

from sqlalchemy import Null, null

from services.encryption_service import AES256Service


class UserRole(str, Enum):
    patient = "patient"
    doctor = "doctor"
    admin = "admin"


class UserDemographics(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    age_range: str
    gender: str
    nationality: str
    region: str
    health_literacy: str
    chronic_conditions: list
    consent_for_research: Optional[str] = None
    consent_given_at: Optional[str] = None
    created_at: Optional[str] = None


class UserBase(BaseModel):
    name: Optional[str] = None
    preferred_language: str = "en"
    # age_range: str
    role: UserRole = UserRole.patient


class UserRegisterDTO(BaseModel):
    user_id: str
    name: str
    preferred_language: str = "en"
    email_enc: Optional[str] = None
    dob_enc: Optional[str] = None

    class Config:
        from_attributes = True


class UserLoginDTO(BaseModel):
    user_id: str
    preferred_language: str = "en"
    firebase_id: Optional[str] = None
    email_enc: Optional[str] = None
    email_enc: Optional[str] = None
    access_token: Optional[str] = None
    triage_count: Optional[int] = None  # backend will generate
    consent_given_at: Optional[str] = None

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    name: Optional[str] = None
    dob: Optional[str]
    firebase_id_token: str
    firebae_id: Optional[str] = None


class UserRegisterValidation(BaseModel):
    name: str
    dob: str
    preferred_language: str = "en"
    role: UserRole = UserRole.patient
    firebase_id_token: str
    firebae_id: Optional[str] = None


class ResearchConsent(BaseModel):
    tos_accepted: bool
    research_consent: bool
    phone_enc: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    preferred_language: str
    consent_given_at: Optional[str] = None
    triage_count: int
    firebase_id: str
    email_enc: str = None


class AuthRequest(BaseModel):
    # These are NOT required for Login, but required for Register
    firebase_id_token: str
    name: Optional[str] = None
    dob: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tos_accepted: Optional[bool] = None
