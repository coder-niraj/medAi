from fastapi import APIRouter

from app.api.auth.index import AuthController
router = APIRouter(prefix="/auth")

router.post("/register")(AuthController.register)
router.post("/login")(AuthController.login)
router.post("/consent")(AuthController.consent)
router.post("/guest-consent")(AuthController.guest_consent)
