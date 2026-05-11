from middlewares.idempotency import guest_protection_add
from fastapi import HTTPException, Request, status
from helpers.audit_context import set_audit_state
from repository.guest.index import GuestRepo

from DTOs.guestSchema import GuestBase, GuestResponse
from utils.firebase import verify_token


class GuestService:
    def __init__(self, guest_repo: GuestRepo):
        self.guest_repo = guest_repo

    def get_client_ip(self, request: Request) -> str:
        # X-Forwarded-For can contain multiple IPs if multiple proxies
        # "client_ip, proxy1_ip, proxy2_ip"
        # Always take the first one — that's the real client
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host

    def map_model_to_guest(self, guest_model: GuestBase) -> GuestResponse:
        return GuestResponse(
            expires_at=guest_model.expires_at, guest_token=guest_model.guest_token
        )

    def get_guest_session(
        self, request: Request, guest_data: GuestBase
    ) -> GuestResponse:
        guest_model = self.guest_repo.create_guest_Session(guest_data)

        set_audit_state(
            request,
            action="CONSENT_GIVEN",
            resource_type="user_profile",
            outcome="SUCCESS",
            resource_id=guest_model.id,
        )
        client_ip = self.get_client_ip(request)
        device = request.headers.get("X-Device-ID")
        guest_protection_add(client_ip, device)
        return self.map_model_to_guest(guest_model)
