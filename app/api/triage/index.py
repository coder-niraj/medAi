from DTOs.triageSchema import TriageClaim
from repository.triage.index import TriageRepo
from services.triage.index import TriageService
from sqlalchemy.orm import Session


class TriageController:
    def __init__(self, db: Session):
        self.triage_repo = TriageRepo(db)
        self.triage_service = TriageService(self.triage_repo)

    def triage_result():
        return "triage result"

    def triage_guest_token_claim(self, request, token_data: dict, body: TriageClaim):
        return self.triage_service.claim_guest_triage(
            request, body.guest_token, user_id=token_data.get("id")
        )

    def specific_triage_result():
        return "result of specific triage"

    def all_triage_results():
        return "all triage"

    def rating_flag():
        return "rating"
