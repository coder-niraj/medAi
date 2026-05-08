from sqlalchemy import text


class HealthRepo:
    def __init__(self, db):
        self.db = db

    def get_health_db(self):
        try:
            self.db.execute(text("SELECT 1"))
            return "ok"
        except Exception:
            print("here +++++++++++ ", Exception)
            return "error"

    def check_vertex_ai(self) -> str:
        # client credentials not yet provided
        return "pending"

    def check_storage(self) -> str:
        # client credentials not yet provided
        return "pending"

    def llm_traces():
        print("llm traces")
