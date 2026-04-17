import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, Enum, ForeignKey, Text, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class TriageResult(Base):
    __tablename__ = "triage_results"

    # id: UUID PK
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )

    # session_id: UUID FK (One-to-one with CHAT_SESSIONS)
    # Note: unique=True enforces the 1:1 relationship
    session_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("chat_sessions.id"), 
        unique=True, 
        nullable=False
    )

    # user_id: UUID FK nullable
    # NULL if guest triage. Set after POST /triage/claim.
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id"), 
        nullable=True
    )

    # result_level: ENUM (green | yellow | red)
    result_level = Column(
        Enum("green", "yellow", "red", name="result_level_enum"),
        nullable=False
    )

    # urgency_score: SMALLINT (1-10)
    urgency_score = Column(SmallInteger, nullable=False)

    # Encrypted Fields (AES-256) - PHI: High
    result_summary_enc = Column(Text, nullable=False)
    result_recommendation_enc = Column(Text, nullable=False)
    symptoms_reported_enc = Column(Text, nullable=False)

    # result_language: VARCHAR (ar | en)
    result_language = Column(String(5), nullable=False, default="en")

    # generated_at: TIMESTAMP (UTC)
    generated_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    # viewed_at: TIMESTAMP nullable
    viewed_at = Column(DateTime(timezone=True), nullable=True)

    # patient_acted: ENUM nullable
    patient_acted = Column(
        Enum(
            "sought_care", 
            "monitored_at_home", 
            "ignored", 
            name="patient_action_enum"
        ),
        nullable=True
    )

    def __repr__(self):
        return f"<TriageResult(id={self.id}, level={self.result_level}, score={self.urgency_score})>"