from fastapi import APIRouter
from routes.auth  import router as auth
from routes.chat import router as chat
from routes.health import router as health
from routes.internal import router as internal
from routes.reports import router as reports
from routes.triage import router as triage
from routes.users import router as users
router =APIRouter()
router.include_router(auth)
router.include_router(chat)
router.include_router(health)
router.include_router(internal)
router.include_router(reports)
router.include_router(triage)
router.include_router(users)