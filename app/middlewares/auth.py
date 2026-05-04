import os

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request, status
from services.kms import KMSService
from repository.audit.index import AuditRepo
from DTOs.auditSchema import AuditDTO
from services.Audit.index import AuditService
from helpers.audit_context import set_audit_state
from helpers.msg import msg
from repository.users.index import UserRepo
from db.session import get_DB, sessionLocal
from datetime import timezone, datetime
import uuid

security_scheme = HTTPBearer()





def decode_token(token: str) -> dict:
    SECRET_KEY = KMSService.get_secret("JWT_SECRET")
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


def check_guest(request: Request, token: str):

    if token.startswith("guest:"):
        token = token[len("guest:"):]
        set_audit_state(
            request,
            action="LOGIN",
            resource_type="user_profile",
            outcome="FAILURE",
            resource_id=token,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message_ar": msg("errors", "guest_access_denied", "ar"),
                "message_en": msg("errors", "guest_access_denied", "en"),
            },
        )


async def get_current_user(
    request: Request,
    res: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    token = res.credentials
    print("get_current_user")
    check_guest(request, token)
    try:
        return decode_token(token)
    except jwt.ExpiredSignatureError:
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
                "message_ar": msg("errors", "token_expired", "ar"),
                "message_en": msg("errors", "token_expired", "en"),
            },
        )

    except jwt.PyJWTError:
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
                "message_ar": msg("errors", "invalid_credentials", "ar"),
                "message_en": msg("errors", "invalid_credentials", "en"),
            },
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_demographic_patient(
    request: Request,
    res: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_DB),
):
    token = res.credentials  # This is the raw JWT string
    check_guest(request, token)
    print("get_demographic_patient")
    try:
        payload = decode_token(token)
        user_repo = UserRepo(db)
        user_obj = user_repo.get_user_by_id(payload.get("id"))
        demo_obj = user_repo.get_user_demo_data(payload.get("id"))
        if not user_obj.research_consent:
            set_audit_state(
                request,
                action="READ",
                resource_type="user_profile",
                outcome="FAILURE",
                resource_id=payload.get("id"),
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message_ar": msg("errors", "research_consent_required", "ar"),
                    "message_en": msg("errors", "research_consent_required", "en"),
                },
            )

        return payload
    except jwt.ExpiredSignatureError:
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
                "message_ar": msg("errors", "token_expired", "ar"),
                "message_en": msg("errors", "token_expired", "en"),
            },
        )
    except jwt.PyJWTError:
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
                "message_ar": msg("errors", "invalid_credentials", "ar"),
                "message_en": msg("errors", "invalid_credentials", "en"),
            },
            headers={"WWW-Authenticate": "Bearer"},
        )


async def consent_gate(
    request: Request,
    res: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    token = res.credentials  # This is the raw JWT string
    # --- 1. HANDLE GUEST LOGIC (UUID) ---
    check_guest(request, token)
    print("get_current_user_gateway")
    try:

        payload = decode_token(token)

        if not payload.get("consent_given_at"):

            set_audit_state(
                request,
                action="READ",
                resource_type="user_profile",
                outcome="FAILURE",
                resource_id=payload.get("id"),
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message_ar": msg("errors", "tos_required", "ar"),
                    "message_en": msg("errors", "tos_required", "en"),
                },
            )
        return payload
    except jwt.ExpiredSignatureError:

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
                "message_ar": msg("errors", "token_expired", "ar"),
                "message_en": msg("errors", "token_expired", "en"),
            },
        )
    except jwt.PyJWTError:

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
                "message_ar": msg("errors", "invalid_credentials", "ar"),
                "message_en": msg("errors", "invalid_credentials", "en"),
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
