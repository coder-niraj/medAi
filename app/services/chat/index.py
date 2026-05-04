from datetime import datetime, timezone
import uuid

from fastapi import Request

from DTOs.chatMessage import ChatMessageObject
from repository.chat.index import ChatRepo


class ChatService:
    def __init__(self, guest_repo: ChatRepo):
        self.chat_repo = guest_repo

    def create_chat_session(self, request, data, user_id):
        request.state.user_id = user_id
        return self.chat_repo.create_chat_session(data, user_id)

    def get_list_session(self, request, offset, limit, user_id):
        return self.chat_repo.list_chat_sessions(user_id, offset, limit)

    def get_all_chat_in_session(self, request, session_id, user_id):
        return self.chat_repo.get_session_messages(session_id, user_id)

    def send_session_message(self, request: Request, message, session_id, user_id):
        message_data = ChatMessageObject(
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
        return self.chat_repo.add_message(request, message_data)
