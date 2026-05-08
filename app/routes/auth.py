from fastapi import APIRouter, Depends, Header, Request, status
from sqlalchemy.orm import Session
from api.auth.index import AuthController
from tasks.ft_curation_job import run
from tasks.cleanup_job import run as guest_run
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


@router.post("/seed", status_code=status.HTTP_201_CREATED)
def register():
    run_all_seeds()
    return "seeded"


@router.post("/run", status_code=status.HTTP_201_CREATED)
def register():
    run()


@router.post("/guest_run", status_code=status.HTTP_201_CREATED)
def register():
    return guest_run()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    request: Request,
    body: UserRegisterValidation,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.register(request, user_dto=body)


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    request: Request,
    body: AuthRequest,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.login(
        request,
        user_dto=body,
    )


@router.post("/consent", status_code=status.HTTP_200_OK)
def consent(
    request: Request,
    body: ResearchConsent,
    token_data: dict = Depends(get_current_user),
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.consent(request, body, token_data)


@router.post("/guest-consent", status_code=status.HTTP_201_CREATED)
# @limiter.limit("10/minute")
def guest_consent(
    request: Request,
    body: GuestBase,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.guest_consent(request, guest_data=body)


@router.post("/patient-demographics", status_code=status.HTTP_201_CREATED)
def demographics(
    request: Request,
    body: UserDemographics,
    token_data: dict = Depends(get_demographic_patient),
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.patient_demographics(request, body, user_id=token_data.get("id"))
