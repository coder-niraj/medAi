from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from fastapi import Depends, HTTPException, Request, status
from services.kms import KMSService
from helpers.audit_context import set_audit_state
from helpers.msg import msg

security_scheme = HTTPBearer()


def decode_token(token: str) -> dict:
    SECRET_KEY = KMSService.get_secret("JWT_SECRET")
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


def check_guest(request: Request, token: str):

    if token.startswith("guest:"):
        token = token[len("guest:") :]
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
