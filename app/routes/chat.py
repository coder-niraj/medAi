from fastapi import APIRouter, Depends, Request
from api.chat.index import ChatController
from DTOs.chatSchema import (
    ChatCreationValidation,
    ChatListValidation,
    ChatMessageValidation,
)
from DTOs.userSchema import ResearchConsent
from db.session import get_DB
from middlewares.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/chat")


def get_auth_controller(db: Session = Depends(get_DB)):
    return ChatController(db)


@router.post("/sessions")
def sessions(
    request: Request,
    body: ChatCreationValidation,
    token_data: dict = Depends(get_current_user),
    controller: ChatController = Depends(get_auth_controller),
):
    return controller.post_create_sessions(request, body, token_data.get("id"))


@router.get("/sessions")
def sessions(
    request: Request,
    body: ChatListValidation,
    token_data: dict = Depends(get_current_user),
    controller: ChatController = Depends(get_auth_controller),
):
    return controller.get_list_sessions(request, body, token_data.get("id"))


# router.get("/sessions")(ChatController.get_sessions)
@router.post("/sessions/{session_id}/messages")
def send_session_message(
    request: Request,
    session_id: str,
    body: ChatMessageValidation,
    token_data: dict = Depends(get_current_user),
    controller: ChatController = Depends(get_auth_controller),
):
    return controller.send_session_message(
        request, body.message, session_id, token_data.get("id")
    )


@router.get("/sessions/{session_id}/messages")
def send_session_message(
    request: Request,
    session_id: str,
    token_data: dict = Depends(get_current_user),
    controller: ChatController = Depends(get_auth_controller),
):
    return controller.get_session_messages(request, session_id, token_data.get("id"))
