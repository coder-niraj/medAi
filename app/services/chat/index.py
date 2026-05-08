from datetime import datetime, timezone
import uuid

from fastapi import HTTPException, Request

from DTOs.chatMessage import ChatMessageObject
from helpers.exception import (
    demographicsNotFound,
    reportIdNotFound,
    reportNotAllowed,
    reportNotFound,
)
from helpers.msg import msg
from services.mock import ChatSession, ConversationMode, mock_ai_assistant_response
from repository.chat.index import ChatRepo


class ChatService:
    def __init__(self, chat_repo: ChatRepo):
        self.chat_repo = chat_repo

    def create_chat_session(self, request, data, user_id):
        request.state.user_id = user_id
        try:
            return self.chat_repo.create_chat_session(data, user_id)
        except demographicsNotFound as e:
            raise HTTPException(
                status_code=403,
                detail={
                    "message_ar": msg("errors", "demographics_required", "ar"),
                    "message_en": msg("errors", "demographics_required", "en"),
                },
            )
        except reportIdNotFound as e:
            raise HTTPException(
                status_code=403,
                detail={
                    "message_ar": msg("errors", "report_not_found", "ar"),
                    "message_en": msg("errors", "report_not_found", "en"),
                },
            )
        except reportNotFound as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "message_ar": msg("errors", "report_not_found", "ar"),
                    "message_en": msg("errors", "report_not_found", "en"),
                },
            )
        except reportNotAllowed as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "message_ar": msg("errors", "report_not_Allowed", "ar"),
                    "message_en": msg("errors", "report_not_Allowed", "en"),
                },
            )

    def create_guest_chat_session(self, request, guest_token):
        request.state.user_id = guest_token
        return self.chat_repo.create_guest_chat_session(guest_token)

    def get_list_session(self, request, offset, limit, user_id):
        return self.chat_repo.list_chat_sessions(user_id, offset, limit)

    def get_all_chat_in_session(self, request, session_id, user_id):
        return self.chat_repo.get_session_messages(session_id, user_id)

    async def send_session_message(
        self, request: Request, message, session_id, user_id
    ):
        user_message_block = ChatMessageObject(
            id=uuid.uuid4(),
            session_id=session_id,
            role="user",
            content=message,
            retrieved_chunk_ids=None,
            prompt_tokens=0,
            finish_reason=None,
            completion_tokens=0,
            patient_rating=None,
            patient_rating_at=None,
            user_feedback_flag=None,
            guardrail_triggered=False,
            guardrail_reason=None,
            fallback_used=False,
            response_language=None,
            question_language="EN",
            question_category=None,
            ft_eligible=None,
            ft_excluded_reason=None,
            created_at=datetime.now(timezone.utc),
        )
        session_row = self.chat_repo.get_session(session_id)
        detected_panels = []
        if session_row.report_id:
            report_row = self.chat_repo.get_report(session_row.report_id)
            if report_row:
                cardiac_urgency_flag = report_row.cardiac_urgency_flag or False
                detected_panels = report_row.detected_panels or []

        session_obj = ChatSession(
            session_id=str(session_row.id),
            mode=ConversationMode(session_row.mode),
            language=session_row.language or "en",
            is_guest=session_row.is_guest or False,
            report_id=str(session_row.report_id) if session_row.report_id else None,
            cardiac_urgency_flag=cardiac_urgency_flag,
            detected_panels=detected_panels,
        )
        result = await mock_ai_assistant_response(
            session=session_obj,
            user_message="What does my HbA1c result mean?",
            stream=False,
        )
        assistant_message_block = ChatMessageObject(
            id=uuid.uuid4(),
            session_id=session_id,
            role="assistant",  # fix: was "user"
            content=result["content"],  # fix: was using raw message
            retrieved_chunk_ids=None,
            prompt_tokens=result["trace"].total_prompt_tokens,
            finish_reason=result["finish_reason"],
            completion_tokens=result["trace"].completion_tokens,
            patient_rating=None,
            patient_rating_at=None,
            user_feedback_flag=None,
            guardrail_triggered=result["guardrail_fired"],
            guardrail_reason=result["guardrail_check"],
            fallback_used=False,
            response_language=session_obj.language,
            question_language="EN",
            question_category=result["question_category"],
            ft_eligible=None,
            ft_excluded_reason=None,
            created_at=datetime.now(timezone.utc),
        )
        message_response = self.chat_repo.add_message(
            request, user_message_block, assistant_message_block
        )
        return {
            "user": self.chat_repo.to_dict(message_response.get("user")),
            "assistant": self.chat_repo.to_dict(message_response.get("assistant")),
        }
