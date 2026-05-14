from fastapi import HTTPException

from helpers.exception import guestNotFound, userNotFound
from helpers.msg import msg
from models.triage import TriageResult
from models.user import User
from models.guest import GuestSession
from models.chatSession import ChatSession
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError


class TriageRepo:
    def __init__(self, db: Session):
        self.db = db

    def is_Triage_Claimed():
        print("save triage to account if guest is registered")

    def claim_guest_triage(self, guest_id, user_id):
        guest_obj = (
            self.db.query(GuestSession)
            .filter(
                GuestSession.guest_token == guest_id,
                GuestSession.claimed_user_id.is_(None),
                GuestSession.expires_at > datetime.now(timezone.utc),
            )
            .first()
        )
        user_obj = self.db.query(User).filter(User.id.is_(user_id)).first()
        if not user_obj:
            raise userNotFound()
        if not guest_obj.claimed_user_id:
            raise guestNotFound()
        try:
            chat_session = (
                self.db.query(ChatSession)
                .filter(ChatSession.guest_token == guest_id)
                .first()
            )
            self.db.query(GuestSession).filter(
                GuestSession.guest_token == guest_id
            ).update({"claimed_user_id": user_obj.id})
            self.db.query(ChatSession).filter(
                ChatSession.guest_token == guest_id
            ).update({"user_id": user_obj.id})
            self.db.commit()
            triage_result = (
                self.db.query(TriageResult)
                .filter(TriageResult.session_id == chat_session.id)
                .first()
            )

        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=403,
                detail={
                    "message_ar": msg("errors", "db_failed", "ar"),
                    "message_en": msg("errors", "db_failed", "en"),
                },
            )
        return {
            "claimed": True,
            "session_id": str(chat_session.id),
            "triage_result_id": str(triage_result.id),
        }

    def save_triage():
        print("save triage")

    def get_triage_result():
        print("get triage result")

    def get_all_triage():
        print("list of all triages")

    def generate_triage_result():
        print("trigger triage result generation")
