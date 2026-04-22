from fastapi import APIRouter
from api.chat.index import ChatController
router = APIRouter(prefix="/chat")

router.post("/sessions")(ChatController.post_sessions)
router.get("/sessions")(ChatController.get_sessions)
router.post("/sessions/{session_id}/messages")(ChatController.send_session_message)
router.get("/sessions/{session_id}/messages")(ChatController.get_session_messages)
