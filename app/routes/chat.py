from fastapi import APIRouter, Depends, Request, status
from api.chat.index import ChatController
from DTOs.chatSchema import (
    ChatCreationValidation,
    ChatListValidation,
    ChatMessageValidation,
)
from DTOs.userSchema import ResearchConsent
from db.session import get_DB
from middlewares.auth import consent_gate, session_gate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/chat")


def get_auth_controller(db: Session = Depends(get_DB)):
    return ChatController(db)


# * create chat session
@router.post("/sessions", status_code=status.HTTP_201_CREATED)
def sessions(
    request: Request,
    body: ChatCreationValidation,
    token_data: dict = Depends(session_gate),
    controller: ChatController = Depends(get_auth_controller),
):

    return controller.post_create_sessions(request, body, token_data)


# * get all chat session
@router.get("/sessions", status_code=status.HTTP_201_CREATED)
def sessions(
    request: Request,
    body: ChatListValidation,
    token_data: dict = Depends(session_gate),
    controller: ChatController = Depends(get_auth_controller),
):
    return controller.get_list_sessions(request, body, token_data.get("id"))


# * send message in session
@router.post("/sessions/{session_id}/messages", status_code=status.HTTP_201_CREATED)
async def send_session_message(
    request: Request,
    session_id: str,
    body: ChatMessageValidation,
    token_data: dict = Depends(consent_gate),
    controller: ChatController = Depends(get_auth_controller),
):
    return await controller.send_session_message(
        request, body.message, session_id, token_data.get("id")
    )


# * get all messages in session
@router.get("/sessions/{session_id}/messages", status_code=status.HTTP_201_CREATED)
def send_session_message(
    request: Request,
    session_id: str,
    token_data: dict = Depends(consent_gate),
    controller: ChatController = Depends(get_auth_controller),
):
    return controller.get_session_messages(request, session_id, token_data.get("id"))
