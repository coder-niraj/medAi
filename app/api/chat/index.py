from fastapi import Request

from DTOs.chatSchema import ChatCreationValidation, ChatListValidation
from repository.chat.index import ChatRepo
from services.chat.index import ChatService
from sqlalchemy.orm import Session


class ChatController:
    def __init__(self, db: Session):
        self.chat_repo = ChatRepo(db)
        self.chat_service = ChatService(self.chat_repo)

    def post_create_sessions(
        self, request: Request, chat_dto: ChatCreationValidation, user_id
    ):
        return self.chat_service.create_chat_session(request, chat_dto, user_id)

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

    def send_session_message(self, request: Request, message, session_id, user_id):
        return self.chat_service.send_session_message(
            request, message, session_id, user_id
        )
