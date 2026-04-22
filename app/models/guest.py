import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db.base import Base


class GuestSession(Base):
    __tablename__ = "guest_sessions"

    # id: UUID PK
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # guest_token: UUID issued to Flutter local storage
    guest_token = Column(String(255), unique=True, nullable=False, index=True)

    # Compliance & Consent
    tos_accepted = Column(Boolean, default=False, nullable=False)
    tos_accepted_at = Column(DateTime(timezone=True), nullable=True)
    research_consent = Column(Boolean, default=False, nullable=False)

    # Medical Context (Required for Triage logic)
    # Age and Gender are critical for MENA-specific reference ranges
    age_range = Column(String(20), nullable=False)
    gender = Column(String(20), nullable=False)
    nationality = Column(String(255), nullable=True)  # Optional ISO 3166-1 alpha-2

    # Conversion Tracking
    # Set when the guest registers and claims this session
    claimed_user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Lifecycle Management
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    triage_count = Column(Integer, default=0, nullable=False)
    # expires_at: created_at + 24 hours
    expires_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(hours=24),
        nullable=False,
        index=True,  # Indexed for the background cleanup job
    )

    def __repr__(self):
        return f"<GuestSession(id={self.id}, token={self.guest_token}, claimed={self.claimed_user_id})>"
