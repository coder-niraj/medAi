from fastapi import HTTPException, status
from repository.guest.index import GuestRepo

from schemas.guestSchema import GuestBase, map_model_to_guest
from utils.firebase import verify_token


class GuestService:
    def __init__(self, guest_repo: GuestRepo):
        self.guest_repo = guest_repo

    def getGuestSession(self, guest_data: GuestBase):
        guest_model = self.guest_repo.create_guest_Session(guest_data)
        return map_model_to_guest(guest_model)
