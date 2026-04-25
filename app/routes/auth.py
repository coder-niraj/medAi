from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session
from api.auth.index import AuthController
from middlewares.index import get_current_user, get_demographic_patient
from schemas.userSchema import (
    AuthRequest,
    ResearchConsent,
    UserCreate,
    UserDemographics,
    UserRegisterVlidation,
)
from schemas.guestSchema import GuestBase
from db.session import get_DB

router = APIRouter(prefix="/auth")


def get_auth_controller(db: Session = Depends(get_DB)):
    return AuthController(db)


@router.post("/register")
def register(
    request: Request,
    user_dto: UserRegisterVlidation,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.register(request, user_dto=user_dto)


@router.post("/login")
def login(
    request: Request,
    user_dto: AuthRequest = None,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.login(
        request,
        user_dto=user_dto,
    )


@router.post("/consent")
def consent(
    request: Request,
    consent_data: ResearchConsent,
    token_data: dict = Depends(get_current_user),
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.consent(request, consent_data, token_data)


@router.post("/guest-consent")
def guest_consent(
    request: Request,
    guest_data: GuestBase,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.guest_consent(request, guest_data=guest_data)


@router.post("/patient-demographics")
def demographics(
    request: Request,
    patient_data: UserDemographics,
    token_data: dict = Depends(get_demographic_patient),
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.patient_demographics(
        request, patient_data, user_id=token_data.get("id")
    )
