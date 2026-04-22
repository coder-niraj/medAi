import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db.base import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    # id: UUID PK
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # user_id: UUID FK nullable (NULL for guests)
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=True,
        index=True
    )

    # report_id: UUID FK nullable (Specific to document mode)
    report_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("reports.id", ondelete="SET NULL"), 
        nullable=True
    )

    # mode: document | general | triage
    mode = Column(
        Enum("document", "general", "triage", name="session_mode_enum"),
        nullable=False
    )

    # title: Auto-generated from first message
    title = Column(String(60), nullable=True)

    # language: ar | en (Controls Gemini response)
    language = Column(String(5), nullable=False, default="en")

    # Guest Handling
    is_guest = Column(Boolean, default=False, nullable=False)
    guest_token = Column(String(255), nullable=True, index=True)

    # Triage State Tracking
    triage_status = Column(
        Enum("in_progress", "completed", "abandoned", name="triage_status_enum"),
        nullable=True
    )
    triage_result = Column(
        Enum("green", "yellow", "red", name="triage_result_enum"),
        nullable=True
    )
    triage_completed_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    # last_message_at: Updated on each new message for idle timeout
    last_message_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def __repr__(self):
        return f"<ChatSession(id={self.id}, mode={self.mode}, user={self.user_id})>"