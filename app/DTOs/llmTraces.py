import asyncio
import time
import uuid
import random
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import AsyncGenerator, Optional

from pydantic import BaseModel


class ConversationMode(str, Enum):
    DOCUMENT = "document"
    GENERAL = "general"
    TRIAGE = "triage"


class TriageLevel(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class GuardrailCheck(str, Enum):
    FINISH_REASON_SAFETY = "finish_reason_safety"
    KEYWORD_MATCH = "keyword_match"
    CARDIAC_URGENCY_OVERRIDE = "cardiac_urgency_override"
    TUMOUR_MARKER_DISCLAIMER_MISSING = "tumour_marker_disclaimer_missing"
    IMAGE_ANALYSIS_ATTEMPT = "image_analysis_attempt"
    TRIAGE_DIAGNOSIS_PATTERN = "triage_diagnosis_pattern"
    RED_DOWNGRADE_ATTEMPT = "red_downgrade_attempt"


class QuestionCategory(str, Enum):
    LAB_EXPLANATION = "lab_explanation"
    SYMPTOM_TRIAGE = "symptom_triage"
    TREND = "trend"
    COMPARISON = "comparison"
    GENERAL = "general"
    MEDICATION_QUERY = "medication_query"
    PANEL_SPECIFIC_QUERY = "panel_specific_query"


class MockChunk(BaseModel):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    section_name: str = "CBC"  # panel name from section_map
    chunk_text: str = ""
    cosine_score: float = 0.0


class LLMTraceRow:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = None
    message_id: Optional[str] = None
    report_id: Optional[str] = None
    call_type: str = "chat"  # 'chat'|'triage_completion'|'summary'|'embedding'
    assembled_prompt_enc: str = ""  # AES-256 encrypted in production
    raw_response_enc: str = ""  # AES-256 encrypted in production
    guardrail_fired: bool = False
    guardrail_check: Optional[str] = None
    guardrail_trigger_text_enc: Optional[str] = None
    retrieved_chunk_ids: list = field(default_factory=list)
    cosine_scores: list = field(default_factory=list)
    panel_coverage: Optional[dict] = None
    zone1_tokens: int = 0
    zone2_tokens: int = 0
    zone3_tokens: int = 0
    zone4_tokens: int = 0
    total_prompt_tokens: int = 0
    completion_tokens: int = 0
    finish_reason: str = "STOP"
    embedding_duration_ms: Optional[int] = None
    retrieval_duration_ms: Optional[int] = None
    llm_duration_ms: int = 0
    total_duration_ms: int = 0
    model_version: str = "gemini-1.5-pro"
    temperature: float = 0.1
    error_code: Optional[str] = None
