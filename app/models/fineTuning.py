import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Enum, ForeignKey, Text, SmallInteger, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from db.base import Base

class FineTuningExample(Base):
    __tablename__ = "fine_tuning_examples"

    # id: UUID PK
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Source IDs (Reference for lineage, but no hard FK to allow deletion of source data)
    source_session_id = Column(UUID(as_uuid=True), nullable=False)
    source_message_id = Column(UUID(as_uuid=True), nullable=False)
    
    # Metadata context
    source_report_type = Column(String(50), nullable=True) # Matches REPORTS enum values
    session_mode = Column(
        Enum("document", "general", "triage", name="session_mode_enum"),
        nullable=False
    )

    # The Training Data (PHI MUST BE STRIPPED BEFORE INSERT)
    system_prompt = Column(Text, nullable=False)
    report_context = Column(Text, nullable=True) # De-identified chunks
    conversation_history = Column(JSONB, nullable=False) # Prior turns
    user_question = Column(Text, nullable=False)
    assistant_response = Column(Text, nullable=False)

    # Contextual labels for stratification
    triage_result_level = Column(
        Enum("green", "yellow", "red", name="triage_level_enum"), 
        nullable=True
    )
    interaction_language = Column(String(20), nullable=False) # ar | en | mixed
    question_category = Column(String(100), nullable=True)
    report_panel = Column(String(100), nullable=True) # e.g., CBC, Lipid Panel

    # Demographic data (Only if research consent was TRUE at time of snapshot)
    age_range = Column(String(20), nullable=True)
    gender = Column(String(20), nullable=True)
    nationality = Column(String(2), nullable=True)

    # Quality Metrics
    document_quality = Column(String(20), nullable=True)
    patient_rating = Column(SmallInteger, nullable=True)
    guardrail_triggered = Column(Boolean, default=False, nullable=False)
    
    # Human-in-the-loop validation
    clinician_validated = Column(Boolean, default=False, nullable=False)
    clinician_rating = Column(SmallInteger, nullable=True)
    auto_quality_score = Column(Numeric(3, 2), nullable=True) # Composite 0-1

    # Export Management
    dataset_version = Column(String(20), default="v1.0", nullable=False)
    included_in_export = Column(Boolean, default=False, nullable=False)
    export_batch_id = Column(UUID(as_uuid=True), nullable=True)

    # Safety Checks
    phi_scan_passed = Column(Boolean, default=False, nullable=False)
    phi_scan_at = Column(DateTime(timezone=True), nullable=True)
    
    # Audit Timestamp
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    def __repr__(self):
        return f"<FineTuningExample(id={self.id}, mode={self.session_mode}, validated={self.clinician_validated})>"