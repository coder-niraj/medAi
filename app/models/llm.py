import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Enum, ForeignKey, Text, Numeric, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from app.db.base import Base

class LLMTrace(Base):
    __tablename__ = "llm_traces"

    # id: UUID PK
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Relationships (Foreign Keys)
    # References CHAT_SESSIONS.id (One-to-one via unique=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"), unique=True, nullable=True)
    
    # References CHAT_MESSAGES.id
    message_id = Column(UUID(as_uuid=True), ForeignKey("chat_messages.id"), nullable=True)
    
    # References REPORTS.id
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=True)

    # Call Metadata
    call_type = Column(
        Enum("chat", "triage_completion", "summary", "embedding", name="call_type_enum"),
        nullable=False
    )

    # Encrypted PHI Fields (AES-256)
    assembled_prompt_enc = Column(Text, nullable=False)
    raw_response_enc = Column(Text, nullable=True) # NULL if call failed
    guardrail_trigger_text_enc = Column(Text, nullable=True)
    error_message_enc = Column(Text, nullable=True)

    # Guardrail Tracking
    guardrail_fired = Column(Boolean, default=False, nullable=False)
    guardrail_check = Column(String(100), nullable=True)

    # RAG / Retrieval Data (Postgres Arrays)
    retrieved_chunk_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    cosine_scores = Column(ARRAY(Float), nullable=True)
    panel_coverage = Column(JSONB, nullable=True) # e.g. '{"CBC": 2}'

    # Token Usage Tracking
    zone1_tokens = Column(Integer, default=0, nullable=False) # System
    zone2_tokens = Column(Integer, default=0, nullable=False) # Context/RAG
    zone3_tokens = Column(Integer, default=0, nullable=False) # History
    zone4_tokens = Column(Integer, default=0, nullable=False) # User Question
    total_prompt_tokens = Column(Integer, nullable=False)
    completion_tokens = Column(Integer, default=0, nullable=False)

    # Gemini Metadata
    finish_reason = Column(String(50), nullable=False) # STOP | MAX_TOKENS | SAFETY | ERROR
    model_version = Column(String(50), default="gemini-1.5-pro", nullable=False)
    temperature = Column(Numeric(3, 2), nullable=False) # 0.0 or 0.1
    error_code = Column(String(100), nullable=True)

    # Performance Metrics (ms)
    ocr_duration_ms = Column(Integer, nullable=True)
    embedding_duration_ms = Column(Integer, nullable=True)
    retrieval_duration_ms = Column(Integer, nullable=True)
    llm_duration_ms = Column(Integer, nullable=False)
    total_duration_ms = Column(Integer, nullable=False)

    # Audit Timestamp
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    def __repr__(self):
        return f"<LLMTrace(id={self.id}, type={self.call_type}, duration={self.total_duration_ms}ms)>"