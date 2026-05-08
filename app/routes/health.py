from fastapi import APIRouter, Depends, Request, status
from api.health.index import HealthController
from sqlalchemy.orm import Session
from middlewares.auth import consent_gate
from db.session import get_DB

router = APIRouter(prefix="/health")


def get_health_controller(db: Session = Depends(get_DB)):
    return HealthController(db)


@router.get("/", status_code=status.HTTP_201_CREATED)
def checkup(
    request: Request,
    token_data: dict = Depends(consent_gate),
    controller: HealthController = Depends(get_health_controller),
):
    return controller.health()
