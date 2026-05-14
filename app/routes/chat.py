from fastapi import APIRouter, Depends, Request, status  # type: ignore
from api.chat.index import ChatController
from DTOs.chatSchema import (
    ChatCreationValidation,
    ChatListValidation,
    ChatMessageValidation,
)
from DTOs.userSchema import ResearchConsent
from middlewares.consent_gate import consent_gate
from db.session import get_DB
from middlewares.auth import session_gate
from sqlalchemy.orm import Session  # type: ignore
from middlewares.rate_limiter import limiter
from fastapi import Query

router = APIRouter(prefix="/chat")


def get_auth_controller(db: Session = Depends(get_DB)):
    return ChatController(db)


def get_user_id_from_token(request: Request) -> str:
    return request.state.user_id


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
    mode: str | None = Query(default=None),
    offset: int = Query(default=0),
    limit: int = Query(default=20),
    token_data: dict = Depends(session_gate),
    controller: ChatController = Depends(get_auth_controller),
):
    return controller.get_list_sessions(
        request,
        ChatListValidation(limit=limit, mode=mode, offset=offset),
        token_data.get("id"),
    )


# * send message in session
@limiter.limit("10/minute", key_func=get_user_id_from_token)
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
