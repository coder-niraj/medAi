from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from api.auth.index import AuthController
from helpers.index import get_current_user, get_demo_graphic_patent
from schemas.userSchema import (
    AuthRequest,
    ResearchConsent,
    UserCreate,
    UserDemoGraphics,
)
from schemas.guestSchema import GuestBase
from db.session import get_DB

router = APIRouter(prefix="/auth")


def get_auth_controller(db: Session = Depends(get_DB)):
    return AuthController(db)


@router.post("/register")
async def register(
    user_dto: UserCreate, controller: AuthController = Depends(get_auth_controller)
):
    return await controller.register(user_dto=user_dto)


@router.post("/login")
async def login(
    user_dto: AuthRequest = None,
    controller: AuthController = Depends(get_auth_controller),
):
    return await controller.login(
        user_dto=user_dto,
    )


@router.post("/consent")
async def consent(
    consent_data: ResearchConsent,
    token_data: dict = Depends(get_current_user),
    controller: AuthController = Depends(get_auth_controller),
):
    return await controller.consent(consent_data, token_data)


@router.post("/guest-consent")
async def guest_consent(
    guest_data: GuestBase,
    controller: AuthController = Depends(get_auth_controller),
):
    return await controller.guest_consent(guest_data=guest_data)


@router.post("/patient-demographics")
async def demographics(
    patient_data: UserDemoGraphics,
    token_data: dict = Depends(get_demo_graphic_patent),
    controller: AuthController = Depends(get_auth_controller),
):
    return await controller.patient_demographics(
        patient_data, user_id=token_data.get("id")
    )
