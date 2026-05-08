from sqlalchemy.orm import Session
from services.health import HealthService
from repository.health.index import HealthRepo


class HealthController:
    def __init__(self, db: Session):
        self.health_repo = HealthRepo(db)
        self.health_service = HealthService(self.health_repo)

    def health(self):
        return self.health_service.check_health()
