from fastapi import HTTPException, Request, status
from helpers.audit import set_audit_state
from repository.guest.index import GuestRepo

from schemas.guestSchema import GuestBase, GuestResponse
from utils.firebase import verify_token


class GuestService:
    def __init__(self, guest_repo: GuestRepo):
        self.guest_repo = guest_repo

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
            resource_type="guest_session",
            outcome="SUCCESS",
            resource_id=guest_model.id,
        )
        return self.map_model_to_guest(guest_model)
