import uuid
from datetime import datetime, timezone
from pydantic import BaseModel
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Enum,
    ForeignKey,
    Text,
    SmallInteger,
    Numeric,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from db.base import Base


class FineTuningExample(BaseModel):
    id: str
    source_session_id: str
    source_message_id: str
    source_report_type: str

    session_mode: str
    
    system_prompt: str
    report_context: str
    conversation_history: str
    user_question: str
    assistant_response: str
    triage_result_level: str
    interaction_language: str
    question_category: str
    report_panel: str
    age_range: str
    gender: str
    nationality: str
    document_quality: str
    patient_rating: str
    guardrail_triggered: str
    clinician_validated: str
    clinician_rating: str
    auto_quality_score: str
    dataset_version: str
    included_in_export: str
    export_batch_id: str
    phi_scan_passed: str
    phi_scan_at: str
    created_at: str


source_message_id    = msg.id,
                source_session_id    = msg.session_id,
                source_report_type   = msg.session.report_type or "none",
                session_mode         = msg.session.mode,
                user_question        = stripped_question,
                assistant_response   = stripped_response,
                report_context       = stripped_context,
                interaction_language = msg.question_language,
                question_category    = msg.question_category,
                report_panel         = msg.retrieved_panel,
                guardrail_triggered  = msg.guardrail_triggered,
                patient_rating       = msg.patient_rating,
                phi_scan_passed      = True,
                phi_scan_at          = datetime.now(timezone.utc),
                # Demographics — only if research consent given
                age_range    = demo.age_range if demo else None,
                gender       = demo.gender if demo else None,
                nationality  = demo.nationality if demo else None,
                dataset_version = "v1.0",
                created_at   = datetime.now(timezone.utc),