from repository.triage.index import TriageRepo


class TriageService:
    def __init__(self, triage_repo: TriageRepo):
        self.triage_repo = triage_repo

    def claim_guest_triage(self, request, guest_token, user_id):
        return self.triage_repo.claim_guest_triage(guest_token, user_id)
