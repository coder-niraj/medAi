from fastapi import APIRouter
from app.routes.auth  import router as auth
from app.routes.chat import router as chat
from app.routes.health import router as health
from app.routes.internal import router as internal
from app.routes.reports import router as reports
from app.routes.triage import router as triage
from app.routes.users import router as users
router =APIRouter()
router.include_router(auth)
router.include_router(chat)
router.include_router(health)
router.include_router(internal)
router.include_router(reports)
router.include_router(triage)
router.include_router(users)