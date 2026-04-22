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

from repository.users.index import UserRepo
from db.session import get_DB
from models.guest import GuestSession

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "app", "core", "security", ".env")
load_dotenv(dotenv_path=ENV_PATH)
security_scheme = HTTPBearer()


async def get_current_user(
    res: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_DB),
):
    token = res.credentials  # This is the raw JWT string
    # --- 1. HANDLE GUEST LOGIC (UUID) ---
    if token.startswith("guest:"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Guests are not authorized to use this feature.",
        )
    try:
        SECRET_KEY = os.getenv("JWT_SECRET")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Check if the token has expired (pyjwt handles this, but good to be explicit)
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
            timezone.utc
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )

        return payload  # Returns {'id': 'user_id', 'email': '...', 'exp': ...}

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_demo_graphic_patent(
    res: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_DB),
):
    token = res.credentials  # This is the raw JWT string
    # --- 1. HANDLE GUEST LOGIC (UUID) ---
    if token.startswith("guest:"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Guests are not authorized to use this feature.",
        )
    try:
        SECRET_KEY = os.getenv("JWT_SECRET")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Check if the token has expired (pyjwt handles this, but good to be explicit)
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
            timezone.utc
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )
        user_repo = UserRepo(db)
        user_obj = user_repo.get_user_by_id(payload.get("id"))
        demo_obj = user_repo.get_user_demo_data(payload.get("id"))
        if not user_obj.research_consent:
            print("payload___________", payload)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="research consent_required",
            )
        print("demo obj : ", demo_obj)
        if demo_obj:
            return payload  # Returns {'id': 'user_id', 'email': '...', 'exp': ...}
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="demographic data already exist",
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_gateway(
    res: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_DB),
):
    token = res.credentials  # This is the raw JWT string
    # --- 1. HANDLE GUEST LOGIC (UUID) ---
    if token.startswith("guest:"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Guests are not authorized to use this feature.",
        )
    try:
        SECRET_KEY = os.getenv("JWT_SECRET")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Check if the token has expired (pyjwt handles this, but good to be explicit)
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
            timezone.utc
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )
        if not payload.get("consent_given_at"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="tos_consent_required"
            )
        return payload  # Returns {'id': 'user_id', 'email': '...', 'exp': ...}

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_access_token(data: dict):

    to_encode = data.copy()

    # Set expiration (e.g., 7 days)
    expire = datetime.now(timezone.utc) + timedelta(days=31)

    # The 'exp' claim is reserved in JWT for expiration
    to_encode.update({"exp": expire})

    # Sign the token with your secret key
    encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET"), algorithm="HS256")
    return encoded_jwt


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
        errors.append(
            {"field": str(err["loc"][-1]), "message": err["msg"], "type": err["type"]}
        )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_FAILED",
                "message": "Input validation failed. Please check the required fields.",
                "message_ar": "فشل التحقق من البيانات. يرجى التحقق من الحقول المطلوبة.",
                "details": {"fields": errors},
            },
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    # This allows you to pass a dict as 'detail' for complex errors
    # or a simple string for quick errors.
    detail = exc.detail
    if isinstance(detail, str):
        detail = {"message": detail, "code": "HTTP_ERROR"}

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": detail.get("code", "ERROR"),
                "message": detail.get("message"),
                "message_ar": detail.get("message_ar", "خطأ في النظام"),
                "details": detail.get("details", {}),
            },
        },
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Log the full error to your backend console/GCP Logs
    print(f"System Error: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
                "message_ar": "حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى لاحقاً.",
                "trace_id": "req_audit_log_id",  # You can generate a UUID here
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
