import os

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request, status
from repository.audit.index import AuditRepo
from schemas.AuditSchema import AuditDTO
from services.Audit.index import AuditService
from helpers.audit import set_audit_state
from helpers.error_management import msg
from repository.users.index import UserRepo
from db.session import get_DB, sessionLocal
from datetime import timezone, datetime
import uuid

security_scheme = HTTPBearer()


async def audit_logger_middleware(request: Request, call_next):
    # 1. Let the request pass through to the controller IMMEDIATELY
    response = await call_next(request)

    # 2. EVERYTHING BELOW THIS LINE runs only AFTER the controller is finished
    print("__________ audit (POST-CONTROLLER) __________")

    path = request.url.path
    # Safely get state
    action = getattr(request.state, "action", None)
    # We only log if an action was set by the controller
    if action:
        resource_id = getattr(request.state, "resource_id", None)

        resource_type = getattr(request.state, "resource_type", None)
        outcome = getattr(request.state, "outcome", None)
        user = getattr(request.state, "user_id", None)
        user = str(user) if user is not None else None
        resource_id = str(resource_id) if resource_id is not None else None
        db = sessionLocal()
        try:
            audit_object = AuditDTO(
                id=uuid.uuid4(),
                action=action,
                outcome=outcome,
                resource_id=resource_id,
                resource_type=resource_type,
                user_id=user,
                timestamp=datetime.utcnow(),
                ip_address_enc=request.client.host if request.client else None,
            )
            service_repo = AuditRepo(db)
            service_object = AuditService(audit_repo=service_repo)
            service_object.create_log(audit_data=audit_object)
            print(
                f"Action: {action} | Path: {path} | ID: {resource_id} | Outcome: {outcome} | User_Id : {user}"
            )
        except Exception as e:
            print("Audit logger failed:", e)
        finally:
            db.close()

    return response


def decode_token(token: str) -> dict:
    SECRET_KEY = os.getenv("JWT_SECRET")
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


def check_guest(request: Request, token: str):

    if token.startswith("guest:"):
        set_audit_state(
            request,
            action="LOGIN",
            resource_type="user_profile",
            outcome="FAILURE",
            resource_id=None,
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


async def get_current_user_gateway(
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
