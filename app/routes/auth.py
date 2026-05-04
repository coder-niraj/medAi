from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session
from api.auth.index import AuthController
from services.seeding.index import run_all_seeds
from middlewares.auth import get_current_user, get_demographic_patient
from DTOs.userSchema import (
    AuthRequest,
    ResearchConsent,
    UserCreate,
    UserDemographics,
    UserRegisterValidation,
)
from middlewares.rate_limiter import limiter
from DTOs.guestSchema import GuestBase
from db.session import get_DB

router = APIRouter(prefix="/auth")


def get_auth_controller(db: Session = Depends(get_DB)):
    return AuthController(db)


@router.post("/seed")
def register():
    run_all_seeds()
    return "seeded"


@router.post("/register")
def register(
    request: Request,
    body: UserRegisterValidation,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.register(request, user_dto=body)


@router.post("/login")
def login(
    request: Request,
    body: AuthRequest = None,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.login(
        request,
        user_dto=body,
    )


@router.post("/consent")
def consent(
    request: Request,
    body: ResearchConsent,
    token_data: dict = Depends(get_current_user),
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.consent(request, body, token_data)


@router.post("/guest-consent")
# @limiter.limit("10/minute")
def guest_consent(
    request: Request,
    body: GuestBase,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.guest_consent(request, guest_data=body)


@router.post("/patient-demographics")
def demographics(
    request: Request,
    body: UserDemographics,
    token_data: dict = Depends(get_demographic_patient),
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.patient_demographics(request, body, user_id=token_data.get("id"))
