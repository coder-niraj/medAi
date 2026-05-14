from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException, Request, status
import uuid
from sqlalchemy import func, select
from DTOs.chatSchema import (
    ChatCreationValidation,
    ChatMessageValidation,
    GuestChatCreationValidation,
)

from sqlalchemy.orm import Session

from DTOs.chatMessage import ChatMessageObject
from helpers.audit_context import set_audit_state
from helpers.exception import (
    demographicsNotFound,
    reportIdNotFound,
    reportNotAllowed,
    reportNotFound,
)
from db import session
from models.patient import PatientDemographics
from models.user import User
from services.encryption_service import AES256Service
from models.chatMessage import ChatMessage
from models.chatSession import ChatSession
from helpers.msg import msg
from models.reports import Report


class ChatRepo:

    def __init__(self, db: Session):
        self.db = db

    def report_data_list(self, chat_sessions) -> list[dict[str, Any]]:
        result = []

        for chat_session in chat_sessions:

            result.append(
                {
                    "id": chat_session.id,
                    "mode": chat_session.mode,
                    "title": chat_session.title,
                    "report_id": chat_session.report_id,
                    "report_type": chat_session.report_type,
                    "triage_result": chat_session.triage_result,
                    "message_count": chat_session.message_count,
                    "last_message_at": chat_session.last_message_at,
                    "language": chat_session.language,
                }
            )
        return result

    def create_chat_session(self, request, data: ChatCreationValidation, user_id):

        report_id = None
        print("::::::::::::::::::::: ", data.mode == "triage")
        print("::::::::::::::::::::: ", data.mode)
        if data.mode == "triage":
            print("-------")
            is_demo_data_Exist = (
                self.db.query(PatientDemographics)
                .filter(PatientDemographics.user_id == user_id)
                .first()
            )
            if not is_demo_data_Exist:
                print("here -------")
                raise demographicsNotFound()
        elif data.mode == "document":
            if not data.report_id:
                raise reportIdNotFound()
            report_data = (
                self.db.query(Report)
                .filter(
                    Report.id == data.report_id,
                    Report.user_id == user_id,
                    Report.status == "ready",
                )
                .first()
            )
            if not report_data:
                raise reportNotFound()
            report_id = report_data.id

        else:
            if data.report_id:
                raise reportNotAllowed()
        chat_data = ChatSession(
            id=uuid.uuid4(),  # optional (auto by default)
            user_id=user_id,  # guest → NULL
            report_id=report_id or None,
            mode=data.mode,  # or "document" / "triage"
            title=None,  # will be filled after first message
            language="en",
            is_guest=False,
            guest_token=None,
            # * Triage fields only for result
            triage_status=None,
            triage_result=None,
            triage_completed_at=None,
        )
        self.db.add(chat_data)
        self.db.commit()
        self.db.refresh(chat_data)
        set_audit_state(
            request,
            action="CHAT_READ",
            resource_type="chat_message",
            outcome="SUCCESS",
            resource_id=chat_data.id,
        )
        return chat_data

    def get_session(self, request, session_id):
        session_obj = (
            self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
        )
        set_audit_state(
            request,
            action="CHAT_READ",
            resource_type="chat_message",
            outcome="SUCCESS",
            resource_id=session_id,
        )
        return session_obj

    def get_report(self, request, report_id):
        report_obj = self.db.query(Report).filter(Report.id == report_id).first()
        set_audit_state(
            request,
            action="CHAT_READ",
            resource_type="chat_message",
            outcome="SUCCESS",
            resource_id=report_id,
        )
        return report_obj

    def to_dict(self, obj):
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

    def add_message(
        self,
        request: Request,
        user_data: ChatMessageObject,
        assistant_data: ChatMessageObject,
    ):

        get_Previous_messages = (
            self.db.query(ChatMessage)
            .filter(ChatMessage.session_id == assistant_data.session_id)
            .order_by(ChatMessage.created_at)
            .all()
        )
        user_message = ChatMessage(
            id=uuid.uuid4(),
            session_id=user_data.session_id,
            content_enc=AES256Service.encrypt(user_data.content),
            role=user_data.role,
            retrieved_chunk_ids=user_data.retrieved_chunk_ids,
            finish_reason=user_data.finish_reason,
            prompt_tokens=user_data.prompt_tokens,
            completion_tokens=user_data.completion_tokens,
            patient_rating=user_data.patient_rating,
            patient_rating_at=user_data.patient_rating_at,
            user_feedback_flag=user_data.user_feedback_flag,
            guardrail_triggered=user_data.guardrail_triggered,
            guardrail_reason=user_data.guardrail_reason,
            fallback_used=user_data.fallback_used,
            response_language=user_data.response_language,
            question_language=user_data.question_language,
            question_category=user_data.question_category,
            ft_eligible=user_data.ft_eligible,
            ft_excluded_reason=user_data.ft_excluded_reason,
            created_at=user_data.created_at,
        )
        assistant_message = ChatMessage(
            id=uuid.uuid4(),
            session_id=assistant_data.session_id,
            content_enc=AES256Service.encrypt(assistant_data.content),
            role=assistant_data.role,
            retrieved_chunk_ids=assistant_data.retrieved_chunk_ids,
            finish_reason=assistant_data.finish_reason,
            prompt_tokens=assistant_data.prompt_tokens,
            completion_tokens=assistant_data.completion_tokens,
            patient_rating=assistant_data.patient_rating,
            patient_rating_at=assistant_data.patient_rating_at,
            user_feedback_flag=assistant_data.user_feedback_flag,
            guardrail_triggered=assistant_data.guardrail_triggered,
            guardrail_reason=assistant_data.guardrail_reason,
            fallback_used=assistant_data.fallback_used,
            response_language=assistant_data.response_language,
            question_language=assistant_data.question_language,
            question_category=assistant_data.question_category,
            ft_eligible=assistant_data.ft_eligible,
            ft_excluded_reason=assistant_data.ft_excluded_reason,
            created_at=assistant_data.created_at,
        )
        self.db.add(assistant_message)
        self.db.add(user_message)
        self.db.commit()
        self.db.refresh(user_message)
        self.db.refresh(assistant_message)
        return {"user": user_message, "assistant": assistant_message}

    def list_chat_sessions(self, request, user_id, offset, limit, mode=None):
        try:
            query = (
                self.db.query(
                    ChatSession.id,
                    ChatSession.mode,
                    ChatSession.title,
                    ChatSession.report_id,
                    Report.report_type.label("report_type"),
                    ChatSession.triage_result,
                    func.count(ChatMessage.id).label("message_count"),
                    ChatSession.last_message_at,
                    ChatSession.language,
                )
                .outerjoin(ChatMessage, ChatMessage.session_id == ChatSession.id)
                .outerjoin(Report, Report.id == ChatSession.report_id)
                .filter(ChatSession.user_id == user_id)
                .group_by(
                    ChatSession.id,
                    ChatSession.mode,
                    ChatSession.title,
                    ChatSession.report_id,
                    Report.report_type,
                    ChatSession.triage_result,
                    ChatSession.last_message_at,
                    ChatSession.language,
                )
                .order_by(ChatSession.last_message_at.desc())
                .offset(offset)
                .limit(limit)
            )

            if mode:
                query = query.filter(ChatSession.mode == mode)

            report_data_list = query.all()
            set_audit_state(
                request,
                action="CHAT_READ",
                resource_type="chat_message",
                outcome="SUCCESS",
                resource_id=None,
            )
            return self.report_data_list(chat_sessions=report_data_list)

        except Exception as e:
            self.db.rollback()
            set_audit_state(
                request,
                action="CHAT_READ",
                resource_type="chat_message",
                outcome="FAILURE",
                resource_id=None,
            )
            print(e)
            raise HTTPException(
                status_code=500,
                detail={
                    "message_ar": msg("errors", "db_failed", "ar"),
                    "message_en": msg("errors", "db_failed", "en"),
                },
            )

    def get_session_messages(self, request, session_id, user_id):
        try:
            query = (
                self.db.query(ChatMessage)
                .filter(ChatMessage.session_id == session_id)
                .all()
            )
            set_audit_state(
                request,
                action="CHAT_READ",
                resource_type="chat_message",
                outcome="SUCCESS",
                resource_id=None,
            )
            return query
        except Exception as e:
            set_audit_state(
                request,
                action="CHAT_READ",
                resource_type="chat_message",
                outcome="FAILURE",
                resource_id=None,
            )
            raise HTTPException(
                status_code=500,
                detail={
                    "message_ar": msg("errors", "db_failed", "ar"),
                    "message_en": msg("errors", "db_failed", "en"),
                },
            )

    def get_non_finetuned_assistant_response_messages(self):
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        result = self.db.execute(
            select(ChatMessage).filter(
                ChatMessage.role == "assistant",
                ChatMessage.created_at > cutoff,
                ChatMessage.ft_eligible.is_(None),
            )
        )
        return result.scalars().all()

    def get_all_messages_before_date(self, session_id, date):
        all_messages = (
            self.db.execute(
                select(ChatMessage)
                .filter(
                    ChatMessage.session_id == session_id,
                    ChatMessage.created_at < date,
                )
                .order_by(ChatMessage.created_at.asc())
            )
            .scalars()
            .all()
        )
        return all_messages

    def get_user_messages(self, session_id, date):
        return (
            self.db.execute(
                select(ChatMessage)
                .filter(
                    ChatMessage.session_id == session_id,
                    ChatMessage.created_at < date,
                    ChatMessage.role == "user",
                )
                .order_by(ChatMessage.created_at.desc())
                .limit(1)
            )
            .scalars()
            .first()
        )

    def mark_message(self, message: ChatMessage, eligible: bool, reason: str = None):

        self.db.query(ChatMessage).filter(ChatMessage.id == message.id).update(
            {"ft_eligible": eligible, "ft_excluded_reason": reason}
        )

    def check_user_research_consent(self, message_session_id):
        message_session = (
            self.db.query(ChatSession)
            .filter(ChatSession.id == message_session_id)
            .first()
        )
        user_obj = (
            self.db.query(User).filter(User.id == message_session.user_id).first()
        )
        if not user_obj or not user_obj.research_consent:
            return False
        return True

    def get_user_from_session(self, message_session_id):
        message_session = (
            self.db.query(ChatSession)
            .filter(ChatSession.id == message_session_id)
            .first()
        )
        user_obj = (
            self.db.query(User).filter(User.id == message_session.user_id).first()
        )
        return user_obj

    def get_data_from_session(self, message_session_id):
        message_session = (
            self.db.query(ChatSession)
            .filter(ChatSession.id == message_session_id)
            .first()
        )
        report_data = (
            self.db.query(Report).filter(Report.id == message_session.report_id).first()
        )

        return {
            "mode": message_session.mode,
            "report_type": report_data.report_type if report_data else None,
            "quality": report_data.document_quality if report_data else None,
        }

    def get_session_ids_from_messages(self, messages: list[ChatMessage]) -> dict:
        # * get all unique session ids from all messages of assistant
        session_ids = list(set(message.session_id for message in messages))

        # * get session objects from database using IN for only unique objects
        all_session_objects = (
            self.db.query(ChatSession).filter(ChatSession.id.in_(session_ids)).all()
        )
        # * return everything in O(1) structure
        # * { "id" : object ,... }
        return {str(s.id): s for s in all_session_objects}

    def get_users_from_sessions(self, sessions: dict):
        user_ids = list(
            set(
                session_obj.user_id
                for session_obj in sessions.values()
                if (session_obj.user_id)
            )
        )
        users_obj = self.db.query(User).filter(User.id.in_(user_ids)).all()
        return {str(user.id): user for user in users_obj}

    def get_reports_from_sessions(self, sessions: dict):
        reports_ids = list(
            set(
                session_obj.report_id
                for session_obj in sessions.values()
                if session_obj.report_id
            )
        )
        if not reports_ids:
            return {}
        report_objs = self.db.query(Report).filter(Report.id.in_(reports_ids)).all()
        return {str(report_obj.id): report_obj for report_obj in report_objs}

    def get_demographics_data(self, user_ids: list) -> dict:
        demo_ids = list(set(user_id for user_id in user_ids))
        demo_objs = self.db.query(PatientDemographics).filter(
            PatientDemographics.user_id.in_(demo_ids)
        )
        return {str(demo_obj.user_id): demo_obj for demo_obj in demo_objs}

    def get_all_messages_group_by_session(self, session_ids: list) -> dict:
        messages = (
            self.db.query(ChatMessage)
            .filter(ChatMessage.session_id.in_(session_ids))
            .order_by(ChatMessage.created_at.asc())
            .all()
        )
        grouped = {}
        for message in messages:
            key = str(message.session_id)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(message)
        return grouped

    def create_guest_chat_session(self, request, guest_token):
        try:
            existing_session = (
                self.db.query(ChatSession)
                .filter(ChatSession.guest_token == guest_token)
                .first()
            )
            if existing_session:
                set_audit_state(
                    request,
                    action="CHAT_READ",
                    resource_type="chat_message",
                    outcome="FAILURE",
                    resource_id=None,
                )
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "message_ar": msg("errors", "guest_session_exist", "ar"),
                        "message_en": msg("errors", "guest_session_exist", "en"),
                    },
                )
            else:

                chat_data = ChatSession(
                    id=uuid.uuid4(),  # optional (auto by default)
                    user_id=None,  # guest → NULL
                    report_id=None,
                    mode="triage",  # or "document" / "triage"
                    title=None,  # will be filled after first message
                    language="en",
                    is_guest=True,
                    guest_token=guest_token,
                    triage_status=None,
                    triage_result=None,
                    triage_completed_at=None,
                )
                self.db.add(chat_data)
                self.db.commit()
                self.db.refresh(chat_data)
                set_audit_state(
                    request,
                    action="CHAT_READ",
                    resource_type="chat_message",
                    outcome="SUCCESS",
                    resource_id=chat_data.id,
                )
                return chat_data
        except HTTPException:
            raise
        except Exception as e:
            set_audit_state(
                request,
                action="CHAT_READ",
                resource_type="chat_message",
                outcome="FAILURE",
                resource_id=None,
            )
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail={
                    "message_ar": msg("errors", "report_not_found", "ar"),
                    "message_en": msg("errors", "report_not_found", "en"),
                },
            )
