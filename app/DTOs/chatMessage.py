from enum import Enum

from typing import List, Optional

from click import Option
from numpy import number
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date, datetime


class GuardrailReason(str, Enum):
    lab_explanation = "lab_explanation"
    symptom_triage = "symptom_triage"
    trend = "trend"
    comparison = "comparison"
    general = "general"
    medication_query = "medication_query"
    panel_specific_query = "panel_specific_query"


class FeedBackFlag(str, Enum):
    helpful = "helpful"
    wrong = "wrong"
    unsafe = "unsafe"
    too_vague = "too_vague"


class Role(str, Enum):
    user = "user"
    assistant = "assistant"


class ChatMessageObject(BaseModel):
    id: Optional[UUID]
    session_id: Optional[UUID]
    role: Role
    content: Optional[str]
    retrieved_chunk_ids: Optional[List[UUID]] = None
    prompt_tokens: int = 0
    finish_reason: Optional[str] = None
    completion_tokens: int = 0
    patient_rating: Optional[int] = None
    patient_rating_at: Optional[datetime] = None
    user_feedback_flag: Optional[FeedBackFlag] = None
    guardrail_triggered: bool = False
    guardrail_reason: Optional[str] = None
    fallback_used: bool = False
    response_language: Optional[str] = None
    question_language: Optional[str]
    question_category: Optional[str] = None
    ft_eligible: Optional[bool] = None
    ft_excluded_reason: Optional[str] = None
    created_at: Optional[datetime]
