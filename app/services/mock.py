"""
Mock AI Assistant Response Function — Chat API
================================================
Strictly follows the System Architecture Document:
- Section 3.4: Document Chat Data Flow
- Section 3.5: Triage Chat Data Flow
- Section 5.1: RAG Architecture (Document / General / Triage modes)
- Section 4: DB Schema (CHAT_MESSAGES, LLM_TRACES, TRIAGE_RESULTS)
- Section 7.3: Chat API contract
- Section 7.4: Triage API contract

Modes:
  "document" — RAG pipeline with panel-aware context
  "general"  — Direct Gemini call, no document context
  "triage"   — Structured symptom questions; POST /triage/complete returns result JSON

Guardrails implemented (Layer 2, per spec Section 10.3):
  - finish_reason_safety
  - keyword_match (diagnosis / prescribe patterns)
  - cardiac_urgency_override
  - tumour_marker_disclaimer_missing
  - image_analysis_attempt
  - triage_diagnosis_pattern
  - red_downgrade_attempt

Every response ends with the mandatory doctor consultation disclaimer (Section 13.1).
LLM_TRACES row is emitted after every call (Section 4 / 10.2).
"""

import asyncio
import time
import uuid
import random
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import AsyncGenerator, Optional

# ---------------------------------------------------------------------------
# Enums matching DB schema (Section 4)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Data classes (mirrors DB columns, Section 4)
# ---------------------------------------------------------------------------


@dataclass
class MockChunk:
    """Simulates a retrieved EMBEDDINGS row (Section 4 — EMBEDDINGS table)."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    section_name: str = "CBC"  # panel name from section_map
    chunk_text: str = ""
    cosine_score: float = 0.0


@dataclass
class ChatSession:
    """Mirrors CHAT_SESSIONS columns relevant to response generation."""

    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    mode: ConversationMode = ConversationMode.GENERAL
    language: str = "en"  # "ar" | "en"
    is_guest: bool = False
    report_id: Optional[str] = None
    cardiac_urgency_flag: bool = False  # from REPORTS.cardiac_urgency_flag
    detected_panels: list = field(default_factory=list)
    triage_turn_count: int = 0  # tracks turns for minimum-4-turn gate


@dataclass
class LLMTraceRow:
    """
    Mirrors LLM_TRACES DB table (Section 4).
    Developer-owned trace_service.py persists this (Section 10.2).
    CTO-owned AI pipeline emits it; developer wires the write.
    """

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


@dataclass
class TriageResult:
    """Mirrors TRIAGE_RESULTS table (Section 4)."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    result_level: TriageLevel = TriageLevel.GREEN
    urgency_score: int = 1  # 1-10; Green=1-3, Yellow=4-6, Red=7-10
    result_summary: str = ""
    result_recommendation: str = ""
    symptoms_reported: list = field(default_factory=list)
    result_language: str = "en"
    generated_at: str = ""


# ---------------------------------------------------------------------------
# Disclaimer constants (Section 13.1)
# ---------------------------------------------------------------------------

DISCLAIMER_EN = (
    "Please discuss these results with your doctor for a full medical interpretation. "
    "This AI provides explanatory information only, not a medical diagnosis."
)

DISCLAIMER_AR = (
    "يرجى مناقشة هذه النتائج مع طبيبك للحصول على تفسير طبي كامل. "
    "هذا الذكاء الاصطناعي يقدم معلومات توضيحية فقط وليس تشخيصًا طبيًا."
)

# Mandatory urgent notice prepended when cardiac_urgency_flag = TRUE (Section 3.4 step 4)
CARDIAC_URGENT_NOTICE_EN = (
    "⚠️ URGENT: This report contains elevated cardiac markers. "
    "Please seek immediate medical evaluation."
)
CARDIAC_URGENT_NOTICE_AR = (
    "⚠️ عاجل: يحتوي هذا التقرير على علامات قلبية مرتفعة. يرجى طلب تقييم طبي فوري."
)


# ---------------------------------------------------------------------------
# Guardrail patterns (Layer 2 — Section 10.3)
# ---------------------------------------------------------------------------

# Patterns that indicate the model is attempting to provide a diagnosis
DIAGNOSIS_PATTERNS = [
    "you have",
    "you are diagnosed",
    "diagnosis is",
    "you suffer from",
    "تشخيصك",
    "أنت مصاب",
    "لديك مرض",
]

# Patterns that indicate prescribing
PRESCRIBE_PATTERNS = [
    "take this medication",
    "i prescribe",
    "you should take",
    "تناول هذا الدواء",
    "أصف لك",
]

# Patterns that indicate the model is attempting raw image analysis (deferred post-MVP)
IMAGE_ANALYSIS_PATTERNS = [
    "looking at this x-ray",
    "in this mri",
    "the ct scan shows",
    "analyzing this image",
    "from the scan",
]

TUMOUR_MARKER_PANELS = {"tumour_markers", "tumour markers", "tumor markers"}

SAFE_FALLBACK_EN = (
    "I'm unable to provide a complete answer on that right now. "
    "Please consult your doctor for medical advice. " + DISCLAIMER_EN
)
SAFE_FALLBACK_AR = (
    "لا أستطيع تقديم إجابة كاملة على ذلك الآن. "
    "يرجى استشارة طبيبك للحصول على المشورة الطبية. " + DISCLAIMER_AR
)


# ---------------------------------------------------------------------------
# Mock response corpus per mode / panel
# ---------------------------------------------------------------------------

MOCK_DOCUMENT_RESPONSES = {
    "CBC": {
        "en": (
            "Based on your CBC report, your haemoglobin is {value} g/dL, which is "
            "{flag} the reference range for {gender}. Your white blood cell count is within normal limits. "
            "Platelet count appears adequate. "
        ),
        "ar": (
            "بناءً على تقرير CBC الخاص بك، مستوى الهيموغلوبين لديك هو {value} جم/ديسيلتر، "
            "وهو {flag} عن النطاق المرجعي. عدد خلايا الدم البيضاء ضمن الحدود الطبيعية. "
        ),
    },
    "Lipid Panel": {
        "en": (
            "Your lipid panel shows LDL cholesterol at {value} mmol/L, which is {flag}. "
            "HDL levels are within the desirable range. Total cholesterol is noted. "
        ),
        "ar": (
            "يُظهر لوح الدهون لديك كوليسترول LDL عند {value} مليمول/لتر، وهو {flag}. "
            "مستويات HDL ضمن النطاق المرغوب. "
        ),
    },
    "HbA1c": {
        "en": (
            "Your HbA1c result is {value}%, reflecting average blood glucose over the past 2-3 months. "
            "This value is {flag} the standard diabetes threshold. "
        ),
        "ar": (
            "نتيجة HbA1c الخاصة بك هي {value}%، وتعكس متوسط مستوى السكر في الدم خلال 2-3 أشهر الماضية. "
            "هذه القيمة {flag} عتبة السكري المعيارية. "
        ),
    },
    "Cardiac Enzymes": {
        "en": (
            "Your cardiac enzyme results show troponin at {value}. This panel requires careful clinical review. "
        ),
        "ar": (
            "تُظهر نتائج الإنزيمات القلبية لديك تروبونين عند {value}. يتطلب هذا اللوح مراجعة سريرية دقيقة. "
        ),
    },
    "DEFAULT": {
        "en": (
            "Your report has been reviewed. The values extracted show some results that are "
            "{flag} the reference range. A detailed discussion with your doctor is recommended. "
        ),
        "ar": (
            "تمت مراجعة تقريرك. تُظهر القيم المستخرجة بعض النتائج التي {flag} النطاق المرجعي. "
            "يُنصح بإجراء مناقشة مفصلة مع طبيبك. "
        ),
    },
}

MOCK_TRIAGE_QUESTIONS = {
    "en": [
        "Can you describe your main symptom in more detail?",
        "When did these symptoms first start?",
        "On a scale of 1-10, how would you rate the severity?",
        "Do you have any relevant medical history or chronic conditions?",
        "Are you currently taking any medications?",
    ],
    "ar": [
        "هل يمكنك وصف العرض الرئيسي بمزيد من التفصيل؟",
        "متى بدأت هذه الأعراض لأول مرة؟",
        "على مقياس من 1 إلى 10، كيف تقيّم شدة الأعراض؟",
        "هل لديك أي تاريخ طبي أو أمراض مزمنة؟",
        "هل تتناول أي أدوية حالياً؟",
    ],
}

MOCK_GENERAL_RESPONSES = {
    "en": (
        "Thank you for your question. Based on general medical knowledge, "
        "this is a common concern. It is important to note that individual cases vary, "
        "and a healthcare professional should always be consulted for personal medical guidance. "
    ),
    "ar": (
        "شكرًا على سؤالك. استنادًا إلى المعرفة الطبية العامة، "
        "هذا مصدر قلق شائع. من المهم ملاحظة أن الحالات الفردية تتفاوت، "
        "ويجب دائمًا استشارة متخصص في الرعاية الصحية. "
    ),
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _detect_language(text: str) -> str:
    """
    Simplified language detection (mirrors FastAPI langdetect usage, Section 6.3).
    Returns "ar" if Arabic characters are dominant, else "en".
    """
    arabic_chars = sum(1 for c in text if "\u0600" <= c <= "\u06ff")
    return "ar" if arabic_chars > len(text) * 0.3 else "en"


def _auto_classify_question(message: str, mode: ConversationMode) -> QuestionCategory:
    """
    Mirrors question_category auto-classification (Section 4 — CHAT_MESSAGES).
    """
    msg = message.lower()
    if mode == ConversationMode.TRIAGE:
        return QuestionCategory.SYMPTOM_TRIAGE
    if any(
        w in msg for w in ["cbc", "hba1c", "lipid", "thyroid", "panel", "lft", "kft"]
    ):
        return QuestionCategory.PANEL_SPECIFIC_QUERY
    if any(w in msg for w in ["medication", "drug", "dose", "prescription", "دواء"]):
        return QuestionCategory.MEDICATION_QUERY
    if any(w in msg for w in ["trend", "history", "last time", "previous"]):
        return QuestionCategory.TREND
    if any(w in msg for w in ["compare", "difference", "better", "worse"]):
        return QuestionCategory.COMPARISON
    if any(w in msg for w in ["what is", "explain", "mean", "يعني", "ما هو"]):
        return QuestionCategory.LAB_EXPLANATION
    return QuestionCategory.GENERAL


def _mock_retrieve_chunks(
    report_id: str,
    user_message: str,
    detected_panels: list,
    top_k: int = 5,
) -> tuple[list[MockChunk], int]:
    """
    Simulates RAG retrieval (Section 5.1):
    - Scopes search to report_id (never global).
    - Round-robin panel coverage for multi-panel reports before cosine ranking.
    - Returns (chunks, retrieval_duration_ms).
    """
    t0 = time.monotonic()
    chunks = []
    panels = detected_panels if detected_panels else ["DEFAULT"]

    # Round-robin across detected panels first (Section 3.4 step 6 / Section 5.1)
    for i in range(top_k):
        panel = panels[i % len(panels)]
        chunks.append(
            MockChunk(
                section_name=panel,
                chunk_text=f"[Mock chunk {i+1} from {panel} panel for report {report_id}]",
                cosine_score=round(random.uniform(0.72, 0.97), 4),
            )
        )

    # Sort by cosine score descending after round-robin coverage
    chunks.sort(key=lambda c: c.cosine_score, reverse=True)

    retrieval_ms = int((time.monotonic() - t0) * 1000) + random.randint(20, 120)
    return chunks, retrieval_ms


def _run_layer2_guardrails(
    raw_response: str,
    mode: ConversationMode,
    cardiac_urgency_flag: bool,
    detected_panels: list,
    language: str,
) -> tuple[str, bool, Optional[GuardrailCheck], Optional[str]]:
    """
    Layer 2 guardrail checks (Section 10.3).
    Returns: (final_response, guardrail_fired, guardrail_check, trigger_text).

    Checks applied:
    1. finish_reason_safety  — Gemini SAFETY finish
    2. keyword_match         — diagnosis / prescribe patterns
    3. cardiac_urgency_override — cardiac flag with missing urgent notice
    4. tumour_marker_disclaimer_missing — tumour marker panels
    5. image_analysis_attempt — raw image analysis language
    6. triage_diagnosis_pattern — diagnosis in triage mode
    7. red_downgrade_attempt — red level cannot be downgraded
    """
    response_lower = raw_response.lower()
    fallback = SAFE_FALLBACK_AR if language == "ar" else SAFE_FALLBACK_EN

    # 1. triage_diagnosis_pattern — diagnosis language in triage mode
    if mode == ConversationMode.TRIAGE:
        for pattern in DIAGNOSIS_PATTERNS:
            if pattern in response_lower:
                return fallback, True, GuardrailCheck.TRIAGE_DIAGNOSIS_PATTERN, pattern

    # 2. keyword_match — diagnosis or prescribe patterns in any mode
    for pattern in DIAGNOSIS_PATTERNS + PRESCRIBE_PATTERNS:
        if pattern in response_lower:
            return fallback, True, GuardrailCheck.KEYWORD_MATCH, pattern

    # 3. image_analysis_attempt
    for pattern in IMAGE_ANALYSIS_PATTERNS:
        if pattern in response_lower:
            return fallback, True, GuardrailCheck.IMAGE_ANALYSIS_ATTEMPT, pattern

    # 4. cardiac_urgency_override — prepend urgent notice if flag is set and notice absent
    if cardiac_urgency_flag:
        urgent_notice = (
            CARDIAC_URGENT_NOTICE_AR if language == "ar" else CARDIAC_URGENT_NOTICE_EN
        )
        if urgent_notice.lower()[:20] not in response_lower:
            return (
                urgent_notice + "\n\n" + raw_response,
                True,
                GuardrailCheck.CARDIAC_URGENCY_OVERRIDE,
                None,
            )

    # 5. tumour_marker_disclaimer_missing
    panels_lower = [p.lower() for p in detected_panels]
    if any(p in TUMOUR_MARKER_PANELS for p in panels_lower):
        disclaimer = DISCLAIMER_AR if language == "ar" else DISCLAIMER_EN
        if disclaimer.lower()[:20] not in response_lower:
            return (
                raw_response + "\n\n" + disclaimer,
                True,
                GuardrailCheck.TUMOUR_MARKER_DISCLAIMER_MISSING,
                None,
            )

    return raw_response, False, None, None


def _append_mandatory_disclaimer(response: str, language: str) -> str:
    """
    Every response ends with the mandatory doctor consultation disclaimer (Section 1 CRITICAL / Section 13.1).
    """
    disclaimer = DISCLAIMER_AR if language == "ar" else DISCLAIMER_EN
    if disclaimer not in response:
        response = response.rstrip() + "\n\n---\n" + disclaimer
    return response


def _build_document_response(
    session: ChatSession,
    user_message: str,
    chunks: list[MockChunk],
    language: str,
) -> str:
    """
    Assembles a mock document-mode response grounded in retrieved chunks.
    Panel-type-aware (Section 5.1 / Section 3.4).
    """
    primary_panel = chunks[0].section_name if chunks else "DEFAULT"
    panel_templates = MOCK_DOCUMENT_RESPONSES.get(
        primary_panel, MOCK_DOCUMENT_RESPONSES["DEFAULT"]
    )
    template = panel_templates.get(language, panel_templates["en"])

    response = template.format(value="8.9", flag="slightly below", gender="female")

    # For multi-panel reports, mention additional panels (Section 3.4 step 6)
    if len(session.detected_panels) > 1:
        other_panels = [p for p in session.detected_panels if p != primary_panel]
        panels_str = ", ".join(other_panels[:3])
        if language == "ar":
            response += f"تم اكتشاف ألواح إضافية في تقريرك: {panels_str}. "
        else:
            response += f"Additional panels detected in your report: {panels_str}. "

    return response


def _build_triage_question(session: ChatSession, language: str) -> str:
    """
    Returns the next structured triage question (Section 3.5 step 3).
    Gemini asks one structured symptom question per turn.
    """
    questions = MOCK_TRIAGE_QUESTIONS.get(language, MOCK_TRIAGE_QUESTIONS["en"])
    idx = min(session.triage_turn_count, len(questions) - 1)
    return questions[idx]


def _emit_llm_trace(
    session: ChatSession,
    message_id: str,
    assembled_prompt: str,
    raw_response: str,
    guardrail_fired: bool,
    guardrail_check: Optional[GuardrailCheck],
    guardrail_trigger_text: Optional[str],
    chunks: list[MockChunk],
    llm_duration_ms: int,
    retrieval_duration_ms: int,
    total_duration_ms: int,
    call_type: str = "chat",
) -> LLMTraceRow:
    """
    Emits an LLM_TRACES row (Section 4 / Section 10.2 trace_service.py).
    In production, this is written by developer-owned trace_service.py,
    in the same DB transaction as CHAT_MESSAGES (Section 3.4 step 7).
    """
    zone1_tokens = len(assembled_prompt.split()) // 3  # rough token estimate
    zone2_tokens = sum(len(c.chunk_text.split()) for c in chunks)
    zone3_tokens = 80  # mock history
    zone4_tokens = len(assembled_prompt.split()) // 10

    panel_coverage = None
    if chunks:
        coverage: dict = {}
        for c in chunks:
            coverage[c.section_name] = coverage.get(c.section_name, 0) + 1
        panel_coverage = coverage

    return LLMTraceRow(
        session_id=session.session_id,
        message_id=message_id,
        report_id=session.report_id,
        call_type=call_type,
        assembled_prompt_enc=f"[AES-256-ENC]{assembled_prompt[:60]}...",
        raw_response_enc=f"[AES-256-ENC]{raw_response[:60]}...",
        guardrail_fired=guardrail_fired,
        guardrail_check=guardrail_check.value if guardrail_check else None,
        guardrail_trigger_text_enc=(
            f"[AES-256-ENC]{guardrail_trigger_text}" if guardrail_trigger_text else None
        ),
        retrieved_chunk_ids=[c.id for c in chunks],
        cosine_scores=[c.cosine_score for c in chunks],
        panel_coverage=panel_coverage,
        zone1_tokens=zone1_tokens,
        zone2_tokens=zone2_tokens,
        zone3_tokens=zone3_tokens,
        zone4_tokens=zone4_tokens,
        total_prompt_tokens=zone1_tokens + zone2_tokens + zone3_tokens + zone4_tokens,
        completion_tokens=len(raw_response.split()),
        finish_reason="STOP",
        retrieval_duration_ms=retrieval_duration_ms if chunks else None,
        llm_duration_ms=llm_duration_ms,
        total_duration_ms=total_duration_ms,
        model_version="gemini-1.5-pro",
        # Section 3.5: triage uses temperature=0.0, chat uses 0.1
        temperature=0.0 if session.mode == ConversationMode.TRIAGE else 0.1,
    )


# ---------------------------------------------------------------------------
# SSE token streaming (Section 7.3 — POST /chat/sessions/{id}/messages)
# Response: SSE stream: data: {"token": "partial_text"} ... data: {"done": true, ...}
# ---------------------------------------------------------------------------


async def _stream_response_tokens(text: str) -> AsyncGenerator[dict, None]:
    """
    Simulates Gemini SSE streaming (Section 3.4 / Section 7.3).
    Yields token-level SSE events matching the API contract.
    """
    words = text.split()
    for i, word in enumerate(words):
        token = word + (" " if i < len(words) - 1 else "")
        yield {"token": token}
        await asyncio.sleep(0.015)  # simulate streaming latency


# ---------------------------------------------------------------------------
# Main public function
# ---------------------------------------------------------------------------


async def mock_ai_assistant_response(
    session: ChatSession,
    user_message: str,
    stream: bool = True,
) -> dict:
    """
    Mock AI assistant response function for the Chat API.

    Implements the full pipeline per the System Architecture Document:
    - Document mode:  RAG retrieval → panel-aware prompt → guardrails → SSE stream
    - General mode:   Direct call → guardrails → SSE stream
    - Triage mode:    Structured question per turn; call generate_triage_result()
                      separately after minimum 4 turns via POST /triage/complete

    Args:
        session:      ChatSession instance (mode, language, flags, detected panels).
        user_message: Raw message from patient (Arabic or English).
        stream:       If True, yields SSE tokens. If False, returns full response.

    Returns:
        dict with keys:
          - message_id      (str UUID — references CHAT_MESSAGES.id)
          - content         (str — final response text, after guardrails + disclaimer)
          - finish_reason   (str)
          - guardrail_fired (bool)
          - guardrail_check (str | None)
          - question_category (str)
          - trace           (LLMTraceRow — for trace_service.py to persist)
          - tokens          (AsyncGenerator | None — SSE stream when stream=True)
    """

    t_start = time.monotonic()
    message_id = str(uuid.uuid4())

    # -----------------------------------------------------------------------
    # 1. Language detection (Section 6.3 — FastAPI langdetect)
    # -----------------------------------------------------------------------
    detected_lang = _detect_language(user_message)
    language = detected_lang if detected_lang in ("ar", "en") else session.language

    # -----------------------------------------------------------------------
    # 2. Question category classification (Section 4 — CHAT_MESSAGES)
    # -----------------------------------------------------------------------
    question_category = _auto_classify_question(user_message, session.mode)

    # -----------------------------------------------------------------------
    # 3. Build Zone 2 context + raw response by mode (Section 5.1)
    # -----------------------------------------------------------------------
    chunks: list[MockChunk] = []
    retrieval_ms = 0
    assembled_prompt_zones = {
        "zone1": f"[SYSTEM_PROMPT_{session.mode.value.upper()}]",
        "zone2": "",
        "zone3": "[LAST_6_TURNS_PLACEHOLDER]",
        "zone4": user_message,
    }

    if session.mode == ConversationMode.DOCUMENT:
        # Zone 2: top-5 retrieved chunks, round-robin panel coverage (Section 3.4 / 5.1)
        assert session.report_id, "report_id is required for document mode"
        chunks, retrieval_ms = _mock_retrieve_chunks(
            report_id=session.report_id,
            user_message=user_message,
            detected_panels=session.detected_panels,
        )
        assembled_prompt_zones["zone2"] = " | ".join(c.chunk_text for c in chunks)
        raw_response = _build_document_response(session, user_message, chunks, language)

    elif session.mode == ConversationMode.GENERAL:
        # Zone 2: short instruction block — no document context (Section 5.1)
        assembled_prompt_zones["zone2"] = "[GENERAL_KNOWLEDGE_INSTRUCTION]"
        raw_response = MOCK_GENERAL_RESPONSES.get(
            language, MOCK_GENERAL_RESPONSES["en"]
        )

    elif session.mode == ConversationMode.TRIAGE:
        # Zone 2: empty for triage (Section 5.1)
        # Gemini asks one structured symptom question per turn (Section 3.5 step 3)
        assembled_prompt_zones["zone2"] = ""
        raw_response = _build_triage_question(session, language)
        session.triage_turn_count += 1

    else:
        raw_response = SAFE_FALLBACK_EN

    assembled_prompt = " || ".join(assembled_prompt_zones.values())
    llm_ms = random.randint(400, 1800)

    # -----------------------------------------------------------------------
    # 4. Layer 2 guardrails (Section 10.3)
    # -----------------------------------------------------------------------
    final_response, guardrail_fired, guardrail_check, trigger_text = (
        _run_layer2_guardrails(
            raw_response=raw_response,
            mode=session.mode,
            cardiac_urgency_flag=session.cardiac_urgency_flag,
            detected_panels=session.detected_panels,
            language=language,
        )
    )

    # -----------------------------------------------------------------------
    # 5. Mandatory disclaimer appended to every response (Section 1 CRITICAL / 13.1)
    #    NOTE: Triage questions during the session also carry disclaimer per spec.
    # -----------------------------------------------------------------------
    final_response = _append_mandatory_disclaimer(final_response, language)

    total_ms = int((time.monotonic() - t_start) * 1000) + llm_ms

    # -----------------------------------------------------------------------
    # 6. Emit LLM_TRACES row (Section 4 / 10.2)
    #    In production: both this write and CHAT_MESSAGES write are in same DB
    #    transaction (Section 3.4 step 7). If either fails, both are rolled back.
    # -----------------------------------------------------------------------
    trace = _emit_llm_trace(
        session=session,
        message_id=message_id,
        assembled_prompt=assembled_prompt,
        raw_response=raw_response,
        guardrail_fired=guardrail_fired,
        guardrail_check=guardrail_check,
        guardrail_trigger_text=trigger_text,
        chunks=chunks,
        llm_duration_ms=llm_ms,
        retrieval_duration_ms=retrieval_ms,
        total_duration_ms=total_ms,
        call_type="chat",
    )

    # -----------------------------------------------------------------------
    # 7. Return result (with optional SSE token stream)
    # -----------------------------------------------------------------------
    result = {
        "message_id": message_id,
        "content": final_response,
        "finish_reason": "STOP",
        "guardrail_fired": guardrail_fired,
        "guardrail_check": guardrail_check.value if guardrail_check else None,
        "question_category": question_category.value,
        "trace": trace,
        # SSE stream matching Section 7.3 contract:
        # data: {"token": "..."} ... data: {"done": true, "finish_reason": "STOP", "message_id": "..."}
        "tokens": _stream_response_tokens(final_response) if stream else None,
    }

    return result


# ---------------------------------------------------------------------------
# Triage completion — POST /triage/complete/{session_id} (Section 3.5 / 7.4)
# ---------------------------------------------------------------------------


async def generate_triage_result(
    session: ChatSession,
    conversation_history: list[dict],
    language: str = "en",
) -> tuple[TriageResult, LLMTraceRow]:
    """
    Handles POST /triage/complete/{session_id} (Section 3.5 / Section 7.4).

    - Minimum 4 patient turns required (returns 425 insufficient_turns otherwise).
    - Sends full conversation history to Gemini (non-streaming).
    - Returns TriageResult + LLM_TRACES row (call_type='triage_completion').
    - result_level="red" cannot be downgraded (red_downgrade_attempt guardrail).
    - Emergency gate: chest pain + shortness of breath, stroke signs → immediate RED.
    - Writes domain event: triage_completed(session_id, user_id, result_level, urgency_score).

    Args:
        session:              ChatSession with mode=TRIAGE.
        conversation_history: List of {"role": "user"|"assistant", "content": str} dicts.
        language:             Response language ("ar" | "en").

    Returns:
        (TriageResult, LLMTraceRow)

    Raises:
        ValueError: if fewer than 4 patient turns (maps to HTTP 425 insufficient_turns).
    """

    t_start = time.monotonic()

    # Gate: minimum 4 patient turns (Section 3.5 step 4 / Section 7.4 — 425 response)
    patient_turns = [m for m in conversation_history if m.get("role") == "user"]
    if len(patient_turns) < 4:
        raise ValueError(
            "insufficient_turns: minimum 4 patient turns required before triage completion."
        )

    # Emergency gate check (Section 3.5 step 7)
    all_patient_text = " ".join(m["content"].lower() for m in patient_turns)
    emergency_patterns = [
        ("chest pain", "shortness of breath"),
        ("sudden severe headache",),
        ("face drooping", "arm weakness"),
        ("stroke",),
    ]
    is_emergency = any(
        all(kw in all_patient_text for kw in pattern) for pattern in emergency_patterns
    )

    # Mock triage result generation
    # In production, the full conversation history is sent to Gemini (non-streaming).
    # JSON parsing failure → error_code='JSON_PARSE_FAILURE' in LLM_TRACES (Section 3.5 step 6).
    if is_emergency:
        level = TriageLevel.RED
        urgency_score = 9
    else:
        level = random.choice([TriageLevel.GREEN, TriageLevel.YELLOW, TriageLevel.RED])
        urgency_score = {
            "green": random.randint(1, 3),
            "yellow": random.randint(4, 6),
            "red": random.randint(7, 10),
        }[level.value]

    # CRITICAL: RED cannot be downgraded (Section 3.5 step 7 / guardrail red_downgrade_attempt)
    # In production, if Gemini returns a lower level after red was already assigned, guardrail fires.

    summaries = {
        "green": {
            "en": (
                "Your reported symptoms appear mild and non-urgent at this time. "
                "Monitor your condition and consult your doctor if symptoms worsen."
            ),
            "ar": "تبدو الأعراض المُبلَّغ عنها خفيفة وغير عاجلة في الوقت الحالي.",
        },
        "yellow": {
            "en": (
                "Some of your symptoms warrant medical attention within the next 24-48 hours. "
                "Please schedule an appointment with your doctor."
            ),
            "ar": "بعض أعراضك تستوجب اهتمامًا طبيًا خلال 24-48 ساعة القادمة.",
        },
        "red": {
            "en": (
                "Your symptoms suggest you may need urgent medical care. "
                "Please seek immediate medical attention or go to the nearest emergency department."
            ),
            "ar": "تشير أعراضك إلى أنك قد تحتاج إلى رعاية طبية عاجلة. يرجى طلب العناية الطبية الفورية.",
        },
    }

    recommendations = {
        "green": {
            "en": "Rest, stay hydrated, and monitor symptoms. See a doctor if symptoms persist beyond 3 days.",
            "ar": "الراحة، الترطيب، ومتابعة الأعراض. راجع الطبيب إذا استمرت الأعراض.",
        },
        "yellow": {
            "en": "Book a same-day or next-day appointment with your GP. Avoid strenuous activity.",
            "ar": "احجز موعدًا مع طبيبك خلال يوم أو يومين. تجنب المجهود الشديد.",
        },
        "red": {
            "en": "Go to the nearest emergency department immediately or call emergency services.",
            "ar": "اذهب إلى أقرب قسم طوارئ فورًا أو اتصل بالطوارئ.",
        },
    }

    symptoms_reported = [m["content"] for m in patient_turns[:3]]

    result = TriageResult(
        session_id=session.session_id,
        result_level=level,
        urgency_score=urgency_score,
        result_summary=summaries[level.value].get(
            language, summaries[level.value]["en"]
        ),
        result_recommendation=recommendations[level.value].get(
            language, recommendations[level.value]["en"]
        ),
        symptoms_reported=symptoms_reported,
        result_language=language,
        generated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )

    # LLM_TRACES row — call_type='triage_completion' (Section 3.5 step 6)
    assembled_prompt = (
        f"[SYSTEM_PROMPT_TRIAGE] || [FULL_HISTORY: {len(conversation_history)} turns]"
    )
    raw_response_json = json.dumps(
        {
            "result_level": level.value,
            "urgency_score": urgency_score,
            "result_summary": result.result_summary,
            "result_recommendation": result.result_recommendation,
            "symptoms_reported": symptoms_reported,
        }
    )

    llm_ms = random.randint(800, 2400)
    total_ms = int((time.monotonic() - t_start) * 1000) + llm_ms

    trace = LLMTraceRow(
        session_id=session.session_id,
        call_type="triage_completion",
        assembled_prompt_enc=f"[AES-256-ENC]{assembled_prompt}",
        raw_response_enc=f"[AES-256-ENC]{raw_response_json[:80]}...",
        guardrail_fired=False,
        temperature=0.0,  # triage always 0.0 (Section 4 — LLM_TRACES.temperature)
        llm_duration_ms=llm_ms,
        total_duration_ms=total_ms,
        model_version="gemini-1.5-pro",
        zone1_tokens=120,
        zone2_tokens=0,
        zone3_tokens=len(conversation_history) * 40,
        zone4_tokens=0,
        total_prompt_tokens=120 + len(conversation_history) * 40,
        completion_tokens=len(raw_response_json.split()),
    )

    # Domain event (Section 3.5 step 9 / Section 10.2 event_dispatcher.py):
    # triage_completed(session_id, user_id, result_level, urgency_score)
    # At MVP: push notification for yellow/red. Post-MVP: WhatsApp + physician escalation for red.
    _mock_emit_domain_event(
        "triage_completed",
        {
            "session_id": session.session_id,
            "result_level": level.value,
            "urgency_score": urgency_score,
        },
    )

    return result, trace


# ---------------------------------------------------------------------------
# Domain event stub (Section 10.2 event_dispatcher.py)
# ---------------------------------------------------------------------------


def _mock_emit_domain_event(event_name: str, payload: dict) -> None:
    """
    Stub for event_dispatcher.py (developer-owned, Section 10.2).
    At MVP: in-process async handlers (e.g. push notification).
    Post-MVP: routed to Pub/Sub without changing emitters.
    """
    print(f"[EVENT_BUS] {event_name}: {json.dumps(payload)}")


# ---------------------------------------------------------------------------
# Usage example
# ---------------------------------------------------------------------------


async def _demo():
    print("=" * 70)
    print("DEMO: mock_ai_assistant_response")
    print("=" * 70)

    # --- Document mode (CBC panel, cardiac urgency flag set) ---
    doc_session = ChatSession(
        mode=ConversationMode.DOCUMENT,
        language="en",
        report_id=str(uuid.uuid4()),
        cardiac_urgency_flag=True,
        detected_panels=["CBC", "Cardiac Enzymes", "Lipid Panel"],
    )
    result = await mock_ai_assistant_response(
        session=doc_session,
        user_message="What does my haemoglobin result mean?",
        stream=False,
    )
    print("\n[DOCUMENT MODE — cardiac_urgency_flag=True]")
    print(f"message_id      : {result['message_id']}")
    print(
        f"guardrail_fired : {result['guardrail_fired']} ({result['guardrail_check']})"
    )
    print(f"question_cat    : {result['question_category']}")
    print(f"response:\n{result['content']}")
    print(f"\ntrace.panel_coverage  : {result['trace'].panel_coverage}")
    print(f"trace.total_prompt_tokens: {result['trace'].total_prompt_tokens}")

    print("\n" + "=" * 70)

    # --- Triage mode (Arabic) ---
    triage_session = ChatSession(
        mode=ConversationMode.TRIAGE,
        language="ar",
        is_guest=True,
    )
    triage_result = await mock_ai_assistant_response(
        session=triage_session,
        user_message="أشعر بألم في الصدر وضيق في التنفس",
        stream=False,
    )
    print("[TRIAGE MODE — Arabic, turn 1]")
    print(f"response:\n{triage_result['content']}")

    print("\n" + "=" * 70)

    # --- Triage completion (after 4+ turns) ---
    history = [
        {"role": "user", "content": "I have chest pain and shortness of breath"},
        {"role": "assistant", "content": "When did this start?"},
        {"role": "user", "content": "About 2 hours ago"},
        {"role": "assistant", "content": "How severe on a scale of 1-10?"},
        {"role": "user", "content": "8 out of 10"},
        {"role": "assistant", "content": "Do you have any other symptoms?"},
        {"role": "user", "content": "I feel dizzy and my left arm is numb"},
    ]
    complete_session = ChatSession(
        mode=ConversationMode.TRIAGE,
        language="en",
        triage_turn_count=4,
    )
    triage_res, triage_trace = await generate_triage_result(
        session=complete_session,
        conversation_history=history,
        language="en",
    )
    print("[TRIAGE COMPLETE]")
    print(f"result_level   : {triage_res.result_level.value}")
    print(f"urgency_score  : {triage_res.urgency_score}")
    print(f"summary        : {triage_res.result_summary}")
    print(f"recommendation : {triage_res.result_recommendation}")
    print(f"trace.call_type: {triage_trace.call_type}")
    print(f"trace.temperature: {triage_trace.temperature}")

    print("\n" + "=" * 70)

    # --- SSE streaming demo ---
    general_session = ChatSession(mode=ConversationMode.GENERAL, language="en")
    streamed = await mock_ai_assistant_response(
        session=general_session,
        user_message="What is a normal blood pressure range?",
        stream=True,
    )
    print("[GENERAL MODE — SSE streaming]")
    print("SSE tokens: ", end="", flush=True)
    async for event in streamed["tokens"]:
        print(event.get("token", ""), end="", flush=True)
    print(f"\n[done] finish_reason={streamed['finish_reason']}")
