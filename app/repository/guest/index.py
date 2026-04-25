from datetime import datetime
from os import name
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from helpers.error_management import msg
from models.guest import GuestSession
from schemas.guestSchema import GuestBase
from helpers.AES import AES256Service
from datetime import datetime, timedelta, timezone


class GuestRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_guest_Session(self, guest_data: GuestBase):
        guest_id = uuid.uuid4()
        guest_token = uuid.uuid4()
        now_utc = datetime.now(timezone.utc)
        expires_at = now_utc + timedelta(hours=24)
        try:
            guest_obj = GuestSession(
                id=guest_id,
                guest_token=guest_token,
                tos_accepted=guest_data.tos_accepted,
                tos_accepted_at=datetime.now(),
                research_consent=guest_data.research_consent,
                age_range=guest_data.age_range,
                gender=guest_data.gender,
                nationality=guest_data.nationality,
                expires_at=expires_at,
                created_at=now_utc,
                triage_count=0,
                claimed_user_id=None,
            )
            self.db.add(guest_obj)
            self.db.commit()
            self.db.refresh(guest_obj)
            return guest_obj
        except Exception as e:
            self.db.rollback()
            print(e)
            raise HTTPException(
                status_code=500,
                detail={
                    "message_ar": msg("errors", "db_failed", "ar"),
                    "message_en": msg("errors", "db_failed", "en"),
                },
            )

    def is_Guest_Eligible(self, guest_uid):
        try:
            guest_obj = (
                self.db.query(GuestSession).filter(GuestSession.id == guest_uid).first()
            )
            if guest_obj:
                is_not_expired = datetime.now(timezone.utc) < guest_obj.expires_at
                has_no_triage = guest_obj.triage_count == 0
                return is_not_expired and has_no_triage
            else:
                return False
        except Exception as e:
            self.db.rollback()
            print(e)
            raise HTTPException(
                status_code=500,
                detail={
                    "message_ar": msg("errors", "db_failed", "ar"),
                    "message_en": msg("errors", "db_failed", "en"),
                },
            )

    def is_Guest_Exists(self, guest_uid):
        guest_obj = (
            self.db.query(GuestSession).filter(GuestSession.id == guest_uid).first()
        )
        return guest_obj is not None

    def get_Guest_from_guest_id(self, guest_uid):
        try:
            return (
                self.db.query(GuestSession).filter(GuestSession.id == guest_uid).first()
            )
        except Exception as e:
            self.db.rollback()
            print(e)
            raise HTTPException(
                status_code=500,
                detail={
                    "message_ar": msg("errors", "db_failed", "ar"),
                    "message_en": msg("errors", "db_failed", "en"),
                },
            )
