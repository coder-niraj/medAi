from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Depends, FastAPI, HTTPException, Request
from dataclasses import dataclass

from helpers.msg import msg
from middlewares import idempotency

# * For POST /reports/upload
# * POST/triage/complete

# * accept optional XIdempotency-Key header. Store key +
# * response in a short-lived cache (Redis or in memory dict at MVP). Return cached
# * response on duplicate key. Prevents
# * duplicate report uploads from flaky mobile
# * connections.

# * FastAPI: 60 req/min per user_id. 10 chat messages/min per user_id. 5 uploads/day per
# * user_id. 1 guest triage per device/IP per 24hr.

security_scheme = HTTPBearer()


@dataclass
class Idempotency:
    id: str
    expires_at: datetime
    status_code: int
    response: Any


@dataclass
class Guest_Protection:
    id: str
    expires_at: datetime
    device: str


idempotency_storage: dict[str, Idempotency] = {}
guest_storage: dict[str, Guest_Protection] = {}


def check_header_idempotency(
    request: Request,
    res: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    idempotency_key = request.headers.get("Idempotency-Key")
    if idempotency_key:
        return Idempotency_check(idempotency_key)
    else:
        raise HTTPException(
            400,
            {
                "message_ar": msg("errors", "Idempotency_key_required", "ar"),
                "message_en": msg("errors", "Idempotency_key_required", "en"),
            },
        )


def Idempotency_check(header_id):
    already_exist = idempotency_storage.get(header_id)
    if already_exist:
        if already_exist.expires_at > datetime.now(timezone.utc):
            return already_exist.response
    return None


def Idempotency_add(header_id: str, response: Any, code: int):
    idempotency_storage[header_id] = Idempotency(
        id=header_id,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        response=response,
        status_code=code,
    )


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host


def guest_protection_check(
    request: Request,
):
    client_ip = get_client_ip(request)
    device = request.headers.get("X-Device-ID")
    if not device:
        raise HTTPException(
            400,
            {
                "message_ar": msg("errors", "Device_Model_Id_required", "ar"),
                "message_en": msg("errors", "Device_Model_Id_required", "en"),
            },
        )
    already_exist = guest_storage.get(client_ip)
    if already_exist:
        if already_exist.expires_at < datetime.now(timezone.utc):
            del guest_storage[client_ip]
            return True

        if already_exist.device == device:
            return False
        else:
            return True
    else:
        return True


def guest_protection_add(ip, device):

    guest_storage[ip] = Guest_Protection(
        id=ip,
        device=device,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )
