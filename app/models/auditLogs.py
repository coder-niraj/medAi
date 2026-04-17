import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class AuditHook(Base):
    __tablename__ = "audit_hooks"

    # id: UUID PK
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # user_id: FK nullable
    # NULL for guest activities or system-level automation
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="SET NULL"), 
        nullable=True,
        index=True
    )

    # action: Categorized event type
    action = Column(String(50), nullable=False, index=True)

    # resource_type: report | chat_message | etc.
    resource_type = Column(String(50), nullable=False)

    # resource_id: The specific row affected
    resource_id = Column(UUID(as_uuid=True), nullable=False)

    # outcome: SUCCESS | FAILURE
    outcome = Column(
        Enum("SUCCESS", "FAILURE", name="audit_outcome_enum"), 
        nullable=False
    )

    # ip_address_enc: AES-256 encrypted (PHI: Med)
    ip_address_enc = Column(Text, nullable=False)

    # user_agent: Device/browser string
    user_agent = Column(Text, nullable=True)

    # timestamp: UTC with millisecond precision
    timestamp = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False,
        index=True
    )

    def __repr__(self):
        return f"<AuditHook(action={self.action}, user={self.user_id}, outcome={self.outcome})>"