import os
from sqlalchemy.orm import Session
from fastapi import  Request
from repository.audit.index import AuditRepo
from DTOs.auditSchema import AuditDTO
from services.Audit.index import AuditService
from helpers.audit_context import set_audit_state
from db.session import get_DB, sessionLocal
from datetime import timezone, datetime
import uuid

async def audit_logger_middleware(request: Request, call_next):
    # 1. Let the request pass through to the controller IMMEDIATELY
    response = await call_next(request)

    # 2. EVERYTHING BELOW THIS LINE runs only AFTER the controller is finished
    print("__________ audit (POST-CONTROLLER) __________")

    path = request.url.path
    # Safely get state
    action = getattr(request.state, "action", None)
    # We only log if an action was set by the controller
    if action:
        resource_id = getattr(request.state, "resource_id", None)

        resource_type = getattr(request.state, "resource_type", None)
        outcome = getattr(request.state, "outcome", None)
        user = getattr(request.state, "user_id", None)
        user = str(user) if user is not None else None
        resource_id = str(resource_id) if resource_id is not None else None
        db = sessionLocal()
        try:
            print("---------------",resource_id)
            audit_object = AuditDTO(
                id=uuid.uuid4(),
                action=action,
                outcome=outcome,
                resource_id=resource_id,
                resource_type=resource_type,
                user_id=user,
                timestamp=datetime.utcnow(),
                ip_address_enc=request.client.host if request.client else None,
            )
            service_repo = AuditRepo(db)
            service_object = AuditService(audit_repo=service_repo)
            service_object.create_log(audit_data=audit_object)
            print(
                f"Action: {action} | Path: {path} | ID: {resource_id} | Outcome: {outcome} | User_Id : {user}"
            )
        except Exception as e:
            print("Audit logger failed:", e)
        finally:
            db.close()

    return response