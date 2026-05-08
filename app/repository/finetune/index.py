from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException, Request
import uuid
import json
from sqlalchemy import func, select
from DTOs.chatSchema import ChatCreationValidation, ChatMessageValidation

from sqlalchemy.orm import Session

from DTOs.chatMessage import ChatMessageObject
from models.fineTuning import FineTuningExample
from models.user import User
from services.encryption_service import AES256Service
from models.chatMessage import ChatMessage
from models.chatSessions import ChatSession
from helpers.msg import msg
from models.reports import Report


class FineTuneRepo:

    def __init__(self, db: Session):
        self.db = db

    def bulk_insert(self, insert_data):
        self.db.bulk_save_objects(insert_data)
        self.db.commit()

    def build_object(
        self,
        message,
        report_obj,
        session_obj,
        system_prompt,
        stripped_context,
        conversation_history,
        stripped_question,
        stripped_response,
        triage_result_level,
        document_quality,
        demographic_obj,
    ) -> FineTuningExample:
        return FineTuningExample(
            id=str(uuid.uuid4()),
            source_message_id=str(message.id),
            source_session_id=str(message.session_id),
            source_report_type=report_obj.report_type if report_obj else "none",
            session_mode=session_obj.mode,
            system_prompt=system_prompt,
            report_context=stripped_context,
            conversation_history=json.dumps(conversation_history),
            user_question=stripped_question,
            assistant_response=stripped_response,
            triage_result_level=triage_result_level,
            interaction_language=message.question_language,
            question_category=message.question_category,
            report_panel="",
            document_quality=document_quality,
            age_range=demographic_obj.age_range if demographic_obj else None,
            gender=demographic_obj.gender if demographic_obj else None,
            nationality=demographic_obj.nationality if demographic_obj else None,
            patient_rating=message.patient_rating,
            guardrail_triggered=message.guardrail_triggered,
            clinician_rating=None,
            clinician_validated=False,
            auto_quality_score=None,
            included_in_export=False,
            export_batch_id=None,
            phi_scan_passed=True,
            phi_scan_at=datetime.now(timezone.utc),
            dataset_version="v1.0",
            created_at=datetime.now(timezone.utc),
        )
