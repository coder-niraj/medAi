import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Enum, ForeignKey, Text, SmallInteger
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from db.base import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    # id: UUID PK
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # session_id: UUID FK - Links to chat_sessions
    session_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("chat_sessions.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )

    # role: user | assistant
    role = Column(
        Enum("user", "assistant", name="message_role_enum"), 
        nullable=False
    )

    # content_enc: AES-256 encrypted message text (PHI: High)
    content_enc = Column(Text, nullable=False)

    # retrieved_chunk_ids: Array of EMBEDDINGS.id (Postgres Array)
    retrieved_chunk_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True)

    # Monitoring & Costs
    finish_reason = Column(String(50), nullable=True) # STOP | MAX_TOKENS | etc.
    prompt_tokens = Column(Integer, default=0, nullable=False)
    completion_tokens = Column(Integer, default=0, nullable=False)

    # User Feedback
    patient_rating = Column(SmallInteger, nullable=True) # 1-5 stars
    patient_rating_at = Column(DateTime(timezone=True), nullable=True)
    user_feedback_flag = Column(
        Enum("helpful", "wrong", "unsafe", "too_vague", name="feedback_flag_enum"),
        nullable=True
    )

    # Guardrails & Safety
    guardrail_triggered = Column(Boolean, default=False, nullable=False)
    guardrail_reason = Column(String(100), nullable=True)
    fallback_used = Column(Boolean, default=False, nullable=False)

    # Language & Classification
    response_language = Column(String(5), nullable=True) # ar | en
    question_language = Column(String(5), nullable=True) # ar | en
    question_category = Column(String(100), nullable=True) # lab_explanation, trend, etc.

    # Fine-tuning Pipeline Metadata (Computed Nightly)
    ft_eligible = Column(Boolean, nullable=True)
    ft_excluded_reason = Column(String(255), nullable=True)

    # Audit Timestamp with Millisecond Precision
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False,
        index=True
    )

    def __repr__(self):
        return f"<ChatMessage(role={self.role}, session={self.session_id}, created={self.created_at})>"