# app/DTOs/fineTune.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FineTuningStruct(BaseModel):
    id: str
    source_session_id: str
    source_message_id: str
    source_report_type: str
    session_mode: str
    system_prompt: str
    report_context: str
    conversation_history: str  # JSON string of list[dict]
    user_question: str
    assistant_response: str

    triage_result_level: Optional[str]  # None if not triage mode
    interaction_language: Optional[str]
    question_category: Optional[str]
    report_panel: Optional[str]
    document_quality: Optional[str]  # None if not document mode

    age_range: Optional[str]
    gender: Optional[str]
    nationality: Optional[str]

    patient_rating: Optional[int]  # 1-5, not str
    guardrail_triggered: bool  # not str
    clinician_validated: bool  # not str
    clinician_rating: Optional[int]  # None until reviewed
    auto_quality_score: Optional[float]  # None until quality job runs
    included_in_export: bool  # not str
    export_batch_id: Optional[str]  # None until exported
    phi_scan_passed: bool  # not str
    phi_scan_at: datetime  # not str
    dataset_version: str
    created_at: datetime  # not str

    class Config:
        from_attributes = True
