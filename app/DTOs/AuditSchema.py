from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date, datetime


class AuditAction(str, Enum):
    upload = "UPLOAD"
    read = "READ"
    delete = "DELETE"
    export = "EXPORT"
    login = "LOGIN"
    admin_Access = "ADMIN_ACCESS"
    consent_given = "CONSENT_GIVEN"
    research_consent = "RESEARCH_CONSENT_CHANGED"
    cardiac_urgency = "CARDIAC_URGENCY_FLAGGED"


class AuditResource(str, Enum):
    report = "report"
    chat_message = "chat"
    lab_value = "lab_values"
    user_profile = "user_profile"
    triage_result = "triage_result"


class AuditOutCome(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class AuditDTO(BaseModel):
    id: UUID
    user_id: Optional[str] = None
    action: AuditAction
    resource_type: AuditResource
    resource_id: Optional[str] = None
    outcome: AuditOutCome
    ip_address_enc: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime
