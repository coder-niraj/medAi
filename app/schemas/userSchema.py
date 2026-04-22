from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date, datetime

from sqlalchemy import Null, null

from helpers.AES import AES256Service


class UserRole(str, Enum):
    patient = "patient"
    doctor = "doctor"
    admin = "admin"


class UserDemoGraphics(BaseModel):
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

    dob: str
    firebase_id_token: str
    firebae_id: Optional[str] = None


class ResearchConsent(BaseModel):
    tos_accepted: bool
    research_consent: bool
    phone_enc: str


class AuthRequest(BaseModel):
    # These are NOT required for Login, but required for Register
    firebase_id_token: str
    name: Optional[str] = None
    dob: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tos_accepted: Optional[bool] = None


def map_model_to_dto_register(user_model) -> UserRegisterDTO:
    """
    Converts the Encrypted Database Model back to a Plain-Text DTO
    for the Flutter Frontend.
    """
    # Decrypt the AES-256 strings only when sending data back to the OWNER
    decrypted_email = AES256Service.decrypt(user_model.email_enc)
    decrypted_phone = AES256Service.decrypt(user_model.phone_enc)

    # If DOB was encrypted as a string, decrypt and convert back to date object
    decrypted_dob_str = AES256Service.decrypt(user_model.dob_enc)
    print(user_model)
    print("___________error ________")
    return UserRegisterDTO(
        user_id=str(user_model.id),
        name=user_model.name,
        email_enc=decrypted_email,  # Now plain text for the UI
        dob_enc=decrypted_dob_str,
        preferred_language=user_model.preferred_language,
        research_consent=False,
        # age_range=user_model.age_range,
        role=user_model.role,
        jwt="",
        consent_given_at=user_model.consent_given_at,
        triage_count=user_model.triage_count,
        created_at=user_model.created_at.isoformat(),  # Convert datetime to ISO string
    )


def map_model_to_dto_login(user_model, fb_uid, fb_email) -> UserLoginDTO:
    print("___________error ________")

    return UserLoginDTO(
        firebase_id=fb_uid,
        access_token="",  # check if consent accepted other wise goto ToS screen
        user_id=str(user_model.id),
        email_enc=user_model.email_enc,
        # email=fb_email,
        preferred_language=user_model.preferred_language,
        consent_given_at=(
            user_model.consent_given_at.isoformat()
            if user_model.consent_given_at
            else None
        ),
        triage_count=user_model.triage_count,
    )
