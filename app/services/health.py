from repository.health.index import HealthRepo


class HealthService:
    def __init__(self, health_repo: HealthRepo):
        self.health_repo = health_repo

    def check_health(self):
        db_status = self.health_repo.get_health_db()
        if db_status == "error":
            status = "degraded"
        else:
            status = "healthy"  # pending is not degraded

        return {
            "status": status,
            "db": db_status,
            "vertex_ai": self.health_repo.check_vertex_ai(),
            "storage": self.health_repo.check_storage(),
            "version": "1.0.0",
        }
