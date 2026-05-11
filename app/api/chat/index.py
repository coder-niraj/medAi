from fastapi import HTTPException, Request, status

from DTOs.chatSchema import ChatCreationValidation, ChatListValidation
from helpers.audit_context import set_audit_state
from helpers.msg import msg
from repository.chat.index import ChatRepo
from services.chat.index import ChatService
from sqlalchemy.orm import Session


class ChatController:
    def __init__(self, db: Session):
        self.chat_repo = ChatRepo(db)
        self.chat_service = ChatService(self.chat_repo)

    def post_create_sessions(
        self, request: Request, chat_dto: ChatCreationValidation, token_data
    ):
        if token_data.get("is_guest"):
            if chat_dto.mode != "triage":
                set_audit_state(
                    request,
                    action="CHAT_READ",
                    resource_type="chat_message",
                    outcome="FAILURE",
                    resource_id=None,
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                        "message_ar": msg("errors", "db_failed", "ar"),
                        "message_en": msg("errors", "db_failed", "en"),
                    },
                )
            else:
                print("guest creates this")
                return self.chat_service.create_guest_chat_session(
                    request, token_data.get("guest_token")
                )
        else:
            return self.chat_service.create_chat_session(
                request, chat_dto, token_data.get("id")
            )

    def get_list_sessions(
        self, request: Request, chat_dto: ChatListValidation, user_id
    ):
        return self.chat_service.get_list_session(
            request,
            offset=chat_dto.offset,
            limit=chat_dto.limit,
            user_id=user_id,
        )

    def get_session_messages(self, request, session_id, user_id):
        return self.chat_service.get_all_chat_in_session(request, session_id, user_id)

    async def send_session_message(
        self, request: Request, message, session_id, user_id
    ):
        return await self.chat_service.send_session_message(
            request, message, session_id, user_id
        )
