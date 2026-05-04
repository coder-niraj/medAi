import os
import time
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from helpers.msg import msg
from services.kms import KMSService
from core.config.lang import MESSAGES
from core.config.lang import MESSAGES, VAL_ERR_MAP
from repository.users.index import UserRepo
from db.session import get_DB
from models.guest import GuestSession

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "app", "core", "security", ".env")
load_dotenv(dotenv_path=ENV_PATH)
security_scheme = HTTPBearer()



def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode_refresh = data.copy()
    # 1. Calculate expiration
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    expire_refresh = datetime.now(timezone.utc) + timedelta(hours=1)
    # 2. Convert datetime to integer timestamp
    # This is the "Safe" way that works in every environment
    to_encode.update({"exp": int(expire.timestamp())})
    to_encode_refresh.update({"exp": expire_refresh})
    # 3. Sign the token
    for key, value in to_encode.items():
        if isinstance(value, datetime):
            to_encode[key] = int(value.timestamp())
    encoded_secret_jwt = jwt.encode(
        to_encode, KMSService.get_secret("JWT_SECRET"), algorithm="HS256"
    )

    return encoded_secret_jwt


async def logger(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    print(f"{request.method} {request.url} completed in {process_time:.3f}s")
    return response


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = []
    for err in exc.errors():
        field_name = str(err["loc"][-1])
        error_type = err["type"]
        original_msg = err["msg"]
        msg_ar = VAL_ERR_MAP.get(error_type, original_msg)
        if error_type == "missing":
            msg_ar = f"الحقل {field_name} مطلوب"
        errors.append(
            {
                "field": field_name,
                "message_en": original_msg,
                "message_ar": msg_ar,
                "type": error_type,
            }
        )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_FAILED",
                "message_en": msg("errors", "input_validation_failed", "en"),
                "message_ar": msg("errors", "input_validation_failed", "ar"),
                "details": {"fields": errors},
            },
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail
    if isinstance(detail, str):
        detail = {
            "message_en": detail,
            "message_ar": "خطأ في النظام",  # Generic fallback for string-only raises
            "code": "HTTP_ERROR",
        }

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": detail.get("code", "ERROR"),
                "message_en": detail.get("message_en", "An unexpected error occurred"),
                "message_ar": detail.get("message_ar", "حدث خطأ غير متوقع"),
                "details": detail.get("details", {}),
            },
        },
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    
    print(f"System Error: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message_en": msg("errors", "unexpected_error_occured", "en"),
                "message_ar": msg("errors", "unexpected_error_occured", "ar"),
                "trace_id": "req_audit_log_id",  
            },
        },
    )




# raise HTTPException(status_code=403, detail={
#     "code": "GUEST_LIMIT_EXCEEDED",
#     "message": "Guest limit reached. Please login.",
#     "message_ar": "تم الوصول إلى الحد الأقصى للضيوف. يرجى تسجيل الدخول."
# })

# raise HTTPException(status_code=403, detail={
#     "code": "CONSENT_REQUIRED",
#     "message": "You must accept the terms to use AI features.",
#     "message_ar": "يجب الموافقة على الشروط لاستخدام ميزات الذكاء الاصطناعي."
# })
