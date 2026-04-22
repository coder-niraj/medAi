import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Enum, ForeignKey, Text, SmallInteger, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from db.base import Base

class Report(Base):
    __tablename__ = "reports"

    # id: UUID PK
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # user_id: UUID FK - References USERS.id. DELETE CASCADE
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )

    # file_url: GCS URI (gs://bucket/{user_id}/{uuid})
    file_url = Column(Text, nullable=False)

    # display_name: Varchar friendly name
    display_name = Column(String(255), nullable=False)

    # AES-256 encrypted fields
    ocr_text_enc = Column(Text, nullable=True) # NULL for image_only
    summary_enc = Column(Text, nullable=True)

    # report_type: Enum for AI prompt templating
    report_type = Column(
        Enum(
            "cbc", "diabetes_panel", "lipid_panel", "vitamins_minerals", 
            "thyroid", "lft", "kft", "urinalysis", "cardiac_enzymes", 
            "hormones", "tumour_markers", "full_checkup", "prescription", 
            "imaging_report", "other", 
            name="report_type_enum"
        ),
        nullable=False
    )

    # report_subtype: Auto-detected by OCR (e.g. cbc_with_differential)
    report_subtype = Column(String(255), nullable=True)

    # detected_panels: Array of panel names
    detected_panels = Column(JSONB, nullable=True) # e.g. ["CBC", "Lipid Panel"]

    # panel_count: SmallINT
    panel_count = Column(SmallInteger, default=1, nullable=False)

    # cardiac_urgency_flag: Default FALSE. 
    # Logic: Set TRUE if high/critical cardiac enzymes detected.
    cardiac_urgency_flag = Column(Boolean, default=False, nullable=False)

    # Language Metadata
    detected_language = Column(String(20), nullable=True) # ar | en | bilingual
    is_bilingual = Column(Boolean, default=False, nullable=False)
    report_language_mix = Column(JSONB, nullable=True) # { "ar": 0.65, "en": 0.35 }

    # status: Workflow state
    status = Column(
        Enum(
            "uploaded", "image_only", "ocr_complete", 
            "ready", "ocr_failed", "embed_failed", 
            name="report_status_enum"
        ),
        default="uploaded",
        nullable=False
    )

    # OCR Quality Metrics
    ocr_avg_confidence = Column(Numeric(5, 4), nullable=True)
    ocr_min_confidence = Column(Numeric(5, 4), nullable=True)
    document_quality = Column(
        Enum("high", "medium", "low", name="document_quality_enum"),
        nullable=True
    )
    low_confidence_blocks = Column(JSONB, nullable=True)

    # Timestamps
    uploaded_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    # retention_expires_at: uploaded_at + 2 years
    retention_expires_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc) + timedelta(days=730), 
        nullable=False
    )

    def __repr__(self):
        return f"<Report(id={self.id}, type={self.report_type}, status={self.status})>"