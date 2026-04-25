from fastapi import HTTPException
from sqlalchemy.orm import Session

from helpers.error_management import msg
from models.auditLogs import AuditHook
from schemas.AuditSchema import AuditDTO


class AuditRepo:
    def __init__(self, db: Session):
        self.db = db

    def Log(self, audit_data: AuditDTO):
        try:
            audit_log = AuditHook(
                id=audit_data.id,
                user_id=audit_data.user_id,
                action=audit_data.action,
                resource_type=audit_data.resource_type,
                resource_id=audit_data.resource_id,
                outcome=audit_data.outcome,
                ip_address_enc=audit_data.ip_address_enc,
                user_agent=audit_data.user_agent,
                timestamp=audit_data.timestamp,
            )
            self.db.add(audit_log)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
