from typing import Any, Tuple

from fastapi import HTTPException, Request, status

from services.encryption_service import AES256Service
from helpers.audit_context import set_audit_state
from helpers.msg import msg
from repository.users.index import UserRepo
from DTOs.userSchema import (
    ResearchConsent,
    UserCreate,
    UserDemographics,
    UserLoginDTO,
    UserRegisterDTO,
    UserRegisterValidation,
)
from utils.firebase import verify_token


class UserService:

    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def map_model_to_dto_register(self, user_model) -> UserRegisterDTO:
        decrypted_email = AES256Service.decrypt(user_model.email_enc)
        decrypted_dob_str = AES256Service.decrypt(user_model.dob_enc)

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

    def map_model_to_dto_login(self, user_model, fb_uid, fb_email) -> UserLoginDTO:
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
            # research_consent=user_model.research_consent,
            triage_count=user_model.triage_count,
        )

    def _get_firebase_user(self, request, id_token: str) -> Tuple[str, str]:
        decoded_token = verify_token(id_token)
        if not decoded_token:
            set_audit_state(
                request,
                action="LOGIN",
                resource_type="user_profile",
                outcome="FAILURE",
                resource_id=None,
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message_ar": msg("errors", "firebase_invalid", "ar"),
                    "message_en": msg("errors", "firebase_invalid", "en"),
                },
            )
        return decoded_token["uid"], decoded_token["email"]

    def register(
        self, request: Request, data: UserRegisterValidation
    ) -> UserRegisterDTO:
        fb_uid, fb_email = self._get_firebase_user(request, data.firebase_id_token)
        exists = self.user_repo.get_user_by_firebase_uid(fb_uid)
        if exists:
            request.state.user_id = exists.id
            set_audit_state(
                request,
                action="LOGIN",
                resource_type="user_profile",
                outcome="FAILURE",
                resource_id=exists.id,
            )
            raise HTTPException(
                status_code=409,
                detail={
                    "message_ar": msg("errors", "already_registered", "ar"),
                    "message_en": msg("errors", "already_registered", "en"),
                },
            )
        else:

            user_obj = self.user_repo.create_user(
                firebase_uid=fb_uid, firbase_email=fb_email, user_dto=data
            )
            request.state.user_id = user_obj.id
            set_audit_state(
                request,
                action="LOGIN",
                resource_type="user_profile",
                outcome="SUCCESS",
                resource_id=user_obj.id,
            )
            return self.map_model_to_dto_register(user_obj)

    def login(self, request: Request, data: UserCreate) -> UserLoginDTO:
        fb_uid, fb_email = self._get_firebase_user(request, data.firebase_id_token)
        is_user_registered = self.user_repo.get_user_by_firebase_uid(fb_uid)
        if is_user_registered:
            request.state.user_id = is_user_registered.id
            set_audit_state(
                request,
                action="LOGIN",
                resource_type="user_profile",
                outcome="SUCCESS",
                resource_id=is_user_registered.id,
            )
            return self.map_model_to_dto_login(is_user_registered, fb_uid, fb_email)
        else:

            set_audit_state(
                request,
                action="LOGIN",
                resource_type="user_profile",
                outcome="FAILURE",
                resource_id=None,
            )
            raise HTTPException(
                status_code=409,
                detail={
                    "message_ar": msg("errors", "registration_failed", "ar"),
                    "message_en": msg("errors", "registration_failed", "en"),
                },
            )

    def change_user_demographics(
        self, request: Request, petient_data: UserDemographics, user_id
    ) -> dict[str, str]:
        request.state.user_id = user_id
        return self.user_repo.create_user_demographics(request, petient_data, user_id)

    def change_consent(
        self, request: Request, consent_dto: ResearchConsent, user_id, token_data
    ) -> dict[str, Any]:
        request.state.user_id = user_id
        if not consent_dto.tos_accepted:

            set_audit_state(
                request,
                action="CONSENT_GIVEN",
                resource_type="user_profile",
                outcome="FAILURE",
                resource_id=user_id,
            )
            raise HTTPException(
                status_code=400,
                detail={
                    "message_ar": msg("errors", "tos_required", "ar"),
                    "message_en": msg("errors", "tos_required", "en"),
                },
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
                    # "email_enc": token_data.get("id"),
                    "preferred_language": token_data.get("preferred_language"),
                    "consent_given_at": consent_result.get("consent_given_at"),
                    # "research_consent": consent_dto.research_consent,
                    "firebase_uid": token_data.get("firebase_uid"),
                    "triage_count": token_data.get("triage_count"),
                }

                set_audit_state(
                    request,
                    action="CONSENT_GIVEN",
                    resource_type="user_profile",
                    outcome="SUCCESS",
                    resource_id=user_id,
                )
                return {
                    "consent_given_at": consent_result["consent_given_at"],
                    "payload": payload,
                }
            else:
                set_audit_state(
                    request,
                    action="CONSENT_GIVEN",
                    resource_type="user_profile",
                    outcome="FAILURE",
                    resource_id=user_id,
                )
                raise HTTPException(
                    status_code=404,
                    detail=consent_result.get(
                        "message_ar",
                        msg("errors", "update_failed", "ar"),
                        "message_en",
                        msg("errors", "update_failed", "ar"),
                    ),
                )
