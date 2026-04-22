from fastapi import APIRouter
from api.health.index import HealthController
router = APIRouter(prefix="/health")
router.get("/health")(HealthController.health)