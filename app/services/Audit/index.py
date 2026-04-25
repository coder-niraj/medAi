from repository.audit.index import AuditRepo
from schemas.AuditSchema import AuditDTO


class AuditService:
    def __init__(self, audit_repo: AuditRepo):
        self.audit_repo = audit_repo

    def create_log(self, audit_data: AuditDTO):
        self.audit_repo.Log(audit_data)
