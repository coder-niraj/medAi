from fastapi import Depends, Header
from sqlalchemy.orm import Session
from repository.guest.index import GuestRepo
from services.guest.index import GuestService
from repository.users.index import UserRepo
from db.session import get_DB
from helpers.index import create_access_token
from services.user.index import UserService
from schemas.userSchema import ResearchConsent, UserCreate, UserDemoGraphics
from schemas.guestSchema import GuestBase


class AuthController:
    def __init__(self, db: Session = Depends(get_DB)):
        self.user_repo = UserRepo(db)
        self.guest_repo = GuestRepo(db)
        self.user_service = UserService(self.user_repo)
        self.guest_service = GuestService(self.guest_repo)

    async def register(self, user_dto: UserCreate):
        user_obj = self.user_service.register(user_dto)
        return user_obj

    async def patient_demographics(self, patient_data: UserDemoGraphics, user_id):
        return self.user_service.change_user_demographics(patient_data, user_id)

    async def login(self, user_dto):
        user_obj = self.user_service.login(user_dto)
        payload = {
            "id": str(user_obj.user_id),
            "email_enc": user_obj.email_enc,
            "preferred_language": user_obj.preferred_language,
            "consent_given_at": user_obj.consent_given_at,
            "firebase_uid": user_obj.firebase_id,
            "triage_count": user_obj.triage_count,
        }
        jwt = create_access_token(payload)
        user_obj.access_token = jwt
        user_obj.email_enc = None
        return user_obj

    async def consent(self, consent_data: ResearchConsent, token_data: dict):
        user_id = token_data.get("id")
        conset_result = self.user_service.change_consent(
            consent_data, user_id, token_data
        )
        jwt = create_access_token(conset_result.get("payload"))
        given_at = conset_result.get("consent_given_at")
        return {"jwt": jwt, "given_at": given_at}

    async def guest_consent(self, guest_data: GuestBase):
        return self.guest_service.getGuestSession(guest_data)
