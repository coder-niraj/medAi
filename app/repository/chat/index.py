from typing import Any

from fastapi import HTTPException, Request
import uuid

from sqlalchemy import func
from DTOs.chatSchema import ChatCreationValidation, ChatMessageValidation

from sqlalchemy.orm import Session

from DTOs.chatMessage import ChatMessageObject
from services.encryption_service import AES256Service
from models.chatMessage import ChatMessage
from models.chatSessions import ChatSession
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

    def create_chat_session(self, data: ChatCreationValidation, user_id):
        try:
            report_data = (
                self.db.query(Report).filter(Report.id == data.report_id).first()
            )
            chat_data = ChatSession(
                id=uuid.uuid4(),  # optional (auto by default)
                user_id=user_id,  # guest → NULL
                report_id=report_data.id,
                mode="general",  # or "document" / "triage"
                title=None,  # will be filled after first message
                language="en",
                is_guest=False,
                guest_token=None,
                triage_status=None,
                triage_result=None,
                triage_completed_at=None,
            )
            self.db.add(chat_data)
            self.db.commit()
            self.db.refresh(chat_data)
            return chat_data
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

    def add_message(self, request: Request, message_data: ChatMessageObject):
        if message_data.role == "assistant":
            get_Previous_messages = (
                self.db.query(ChatMessage)
                .filter(ChatMessage.session_id == message_data.session_id)
                .order_by(ChatMessage.created_at)
                .all()
            )
        user_message = ChatMessage(
            id=uuid.uuid4(),
            session_id=message_data.session_id,
            content_enc=AES256Service.encrypt(message_data.content),
            role=message_data.role,
            retrieved_chunk_ids=message_data.retrieved_chunk_ids,
            finish_reason=message_data.finish_reason,
            prompt_tokens=message_data.prompt_tokens,
            completion_tokens=message_data.completion_tokens,
            patient_rating=message_data.patient_rating,
            patient_rating_at=message_data.patient_rating_at,
            user_feedback_flag=message_data.user_feedback_flag,
            guardrail_triggered=message_data.guardrail_triggered,
            guardrail_reason=message_data.guardrail_reason,
            fallback_used=message_data.fallback_used,
            response_language=message_data.response_language,
            question_language=message_data.question_language,
            question_category=message_data.question_category,
            ft_eligible=message_data.ft_eligible,
            ft_excluded_reason=message_data.ft_excluded_reason,
            created_at=message_data.created_at,
        )
        self.db.add(user_message)
        self.db.commit()
        self.db.refresh(user_message)
        return user_message

    def list_chat_sessions(self, user_id, offset, limit, mode=None):
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
            return self.report_data_list(chat_sessions=report_data_list)

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

    def get_session_messages(self, session_id, user_id):
        query = (
            self.db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .all()
        )
        return query
