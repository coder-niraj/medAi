from typing import Any
from fastapi import Request
from sqlalchemy.orm import Session
from repository.guest.index import GuestRepo
from services.guest.index import GuestService
from repository.users.index import UserRepo
from helpers.index import create_access_token
from services.user.index import UserService
from schemas.userSchema import (
    LoginResponse,
    ResearchConsent,
    UserCreate,
    UserDemographics,
    UserRegisterDTO,
    UserRegisterVlidation,
)
from schemas.guestSchema import GuestBase, GuestResponse


class AuthController:
    def __init__(self, db: Session):
        self.user_repo = UserRepo(db)
        self.guest_repo = GuestRepo(db)
        self.user_service = UserService(self.user_repo)
        self.guest_service = GuestService(self.guest_repo)

    def register(
        self, request: Request, user_dto: UserRegisterVlidation
    ) -> UserRegisterDTO:

        user_obj = self.user_service.register(request, user_dto)
        return user_obj

    def patient_demographics(
        self, request: Request, patient_data: UserDemographics, user_id: str
    ) -> dict[str, str]:
        request.state.user_id = str(user_id)
        return self.user_service.change_user_demographics(
            request, patient_data, user_id
        )

    def login(self, request: Request, user_dto: UserCreate) -> LoginResponse:
        user_obj = self.user_service.login(request, user_dto)
        request.state.user_id = str(user_obj.user_id)
        payload = {
            "id": str(user_obj.user_id),
            # "email_enc": user_obj.email_enc,
            "preferred_language": user_obj.preferred_language,
            "consent_given_at": (
                str(user_obj.consent_given_at) if user_obj.consent_given_at else None
            ),
            "firebase_uid": user_obj.firebase_id,
            "triage_count": user_obj.triage_count,
            # "research_consent": user_obj.research_consent,
        }
        jwt = create_access_token(payload)
        return LoginResponse(
            user_id=user_obj.user_id,
            access_token=jwt,
            consent_given_at=user_obj.consent_given_at,
            firebase_id=user_obj.firebase_id,
            preferred_language=user_obj.preferred_language,
            token_type="bearer",
            triage_count=user_obj.triage_count,
        )

    def consent(
        self, request: Request, consent_data: ResearchConsent, token_data: dict
    ) -> dict[str, Any]:
        user_id = token_data.get("id")
        request.state.user_id = str(user_id)
        consent_result = self.user_service.change_consent(
            request, consent_data, user_id, token_data
        )
        jwt = create_access_token(consent_result.get("payload"))
        given_at = consent_result.get("consent_given_at")
        return {"access_token": jwt, "consent_given_at": given_at}

    def guest_consent(self, request: Request, guest_data: GuestBase) -> GuestResponse:
        return self.guest_service.get_guest_session(request, guest_data)
