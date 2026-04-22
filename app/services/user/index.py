from fastapi import HTTPException, status

from repository.users.index import UserRepo
from schemas.userSchema import (
    ResearchConsent,
    UserCreate,
    UserDemoGraphics,
    map_model_to_dto_login,
    map_model_to_dto_register,
)
from utils.firebase import verify_token


class UserService:

    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def _get_firebase_user(self, id_token: str):
        """Helper to centralize token validation."""
        decoded_token = verify_token(id_token)
        if not decoded_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired Firebase Token",
            )
        return decoded_token["uid"], decoded_token["email"]

    def register(self, data: UserCreate):
        fb_uid, fb_email = self._get_firebase_user(data.firebase_id_token)
        exists = self.user_repo.get_user_by_firebase_uid(fb_uid)
        if exists:
            raise HTTPException(status_code=409, detail="already registered")
        else:
            user_obj = self.user_repo.create_user(
                firebase_uid=fb_uid, firbase_email=fb_email, user_dto=data
            )
            return map_model_to_dto_register(user_obj)

    def login(self, data: UserCreate):
        fb_uid, fb_email = self._get_firebase_user(data.firebase_id_token)
        is_user_registered = self.user_repo.get_user_by_firebase_uid(fb_uid)
        if is_user_registered:
            return map_model_to_dto_login(is_user_registered, fb_uid, fb_email)
        else:
            raise HTTPException(
                status_code=409, detail="Could not complete registration"
            )

    def change_user_demographics(self, petient_data: UserDemoGraphics, user_id):
        return self.user_repo.create_user_demographics(petient_data, user_id)

    def change_consent(self, consent_dto: ResearchConsent, user_id, token_data):
        if not consent_dto.tos_accepted:
            raise HTTPException(
                status_code=400,
                detail="Terms of Service must be accepted to update consent.",
            )
        else:
            consent_result = self.user_repo.update_consent_ToS(
                research_consent=consent_dto.research_consent,
                user_id=user_id,
                phone=consent_dto.phone_enc,
            )
            if consent_result.get("result"):
                payload = {
                    "id": token_data.get("id"),
                    "email_enc": token_data.get("id"),
                    "preferred_language": token_data.get("id"),
                    "consent_given_at": token_data.get("id"),
                    "firebase_uid": token_data.get("id"),
                    "triage_count": token_data.get("id"),
                }
                return {
                    "consent_given_at": consent_result["consent_given_at"],
                    "payload": payload,
                }
            else:
                raise HTTPException(
                    status_code=404,
                    detail=consent_result.get("Message", "Update failed"),
                )
