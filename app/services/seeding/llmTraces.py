import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from decimal import Decimal
from models.llm import LLMTrace

dummy_llm_traces = [
    # 1. Chat call — document mode, RAG retrieval, no guardrail
    {
        "id": uuid.UUID("978420fc-67ac-4c61-bcd3-b24f8035a3ee"),
        "session_id": uuid.UUID("4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae"),  # Ahmed document session
        "message_id": uuid.UUID("28fd1664-1c46-4353-9b38-e14291ab4f59"),  # user message
        "report_id": uuid.UUID("9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6"),  # CBC report
        "call_type": "chat",
        "assembled_prompt_enc": "AES256:enc:...zone1+zone2+zone3+zone4...",
        "raw_response_enc": "AES256:enc:...gemini_raw_response...",
        "guardrail_trigger_text_enc": None,
        "error_message_enc": None,
        "guardrail_fired": False,
        "guardrail_check": None,
        "retrieved_chunk_ids": [
            uuid.UUID("2f0de9e2-2c3a-4f85-9d1f-9baf0946360e"),
            uuid.UUID("c019ae54-4fd4-42be-a704-2d6ded509711"),
            uuid.UUID("2dc152ec-f82f-49c7-ae70-a350e1fc894c"),
        ],
        "cosine_scores": [0.92, 0.88, 0.85],
        "panel_coverage": {"CBC": 3},
        "zone1_tokens": 450,
        "zone2_tokens": 800,
        "zone3_tokens": 300,
        "zone4_tokens": 50,
        "total_prompt_tokens": 1600,
        "completion_tokens": 320,
        "finish_reason": "STOP",
        "model_version": "gemini-1.5-pro",
        "temperature": Decimal("0.10"),
        "error_code": None,
        "ocr_duration_ms": None,
        "embedding_duration_ms": 120,
        "retrieval_duration_ms": 85,
        "llm_duration_ms": 2100,
        "total_duration_ms": 2350,
        "created_at": datetime(2025, 1, 10, 9, 30, tzinfo=timezone.utc),
    },

    # 2. Triage completion — no RAG, temperature 0.0,
    #    full conversation history in Zone 3
    {
        "id": uuid.UUID("f53ba1b3-78eb-4de2-aef3-76a51d6d1e8f"),
        "session_id": uuid.UUID("e794391b-accd-4d36-915a-6140c93daffe"),  # Ahmed general session
        "message_id": uuid.UUID("caf6858e-f52b-4371-a31a-00b8112698d1"),  # user triage message
        "report_id": None,              # triage has no report
        "call_type": "triage_completion",
        "assembled_prompt_enc": "AES256:enc:...triage_full_conversation_history...",
        "raw_response_enc": "AES256:enc:...triage_result_json...",
        "guardrail_trigger_text_enc": None,
        "error_message_enc": None,
        "guardrail_fired": False,
        "guardrail_check": None,
        "retrieved_chunk_ids": None,    # no RAG in triage
        "cosine_scores": None,
        "panel_coverage": None,
        "zone1_tokens": 450,
        "zone2_tokens": 0,              # no context/RAG
        "zone3_tokens": 1200,           # full conversation history
        "zone4_tokens": 0,
        "total_prompt_tokens": 1650,
        "completion_tokens": 180,
        "finish_reason": "STOP",
        "model_version": "gemini-1.5-pro",
        "temperature": Decimal("0.00"), # triage uses 0.0
        "error_code": None,
        "ocr_duration_ms": None,
        "embedding_duration_ms": None,
        "retrieval_duration_ms": None,
        "llm_duration_ms": 1800,
        "total_duration_ms": 1900,
        "created_at": datetime(2025, 2, 14, 11, 0, tzinfo=timezone.utc),
    },

    # 3. Summary call — full checkup multi panel,
    #    cardiac urgency guardrail fired
    {
        "id": uuid.UUID("787f8804-c5f8-41a6-9590-ce820b5f48f0"),
        "session_id": uuid.UUID("e2385da2-08c4-4b7e-af76-97b947567d09"),  # Sarah triage session
        "message_id": None,             # summary call has no message_id
        "report_id": uuid.UUID("df7b626b-0ea5-425a-940e-44fb037e88a6"),  # full checkup report
        "call_type": "summary",
        "assembled_prompt_enc": "AES256:enc:...full_checkup_summary_prompt...",
        "raw_response_enc": "AES256:enc:...full_checkup_summary_response...",
        "guardrail_trigger_text_enc": "AES256:enc:...cardiac_enzyme_text_that_triggered...",
        "error_message_enc": None,
        "guardrail_fired": True,        # cardiac urgency override fired
        "guardrail_check": "cardiac_urgency_override",
        "retrieved_chunk_ids": [
            uuid.UUID("9e6893f2-734d-4ebf-bef4-7274420599ed"),
            uuid.UUID("a43ea41d-6ab9-4329-84ea-c0ba92c2df11"),
            uuid.UUID("91dd30d8-d15a-4cee-84d2-fd60a43bd21f"),
            uuid.UUID("733594f0-6725-4148-9bbe-f5cde896ee97"),
        ],
        "cosine_scores": [0.95, 0.91, 0.89, 0.86, 0.82],
        "panel_coverage": {
            "CBC": 2,
            "Lipid Panel": 1,
            "Cardiac Enzymes": 2,
        },
        "zone1_tokens": 450,
        "zone2_tokens": 1200,           # multi panel chunks
        "zone3_tokens": 0,
        "zone4_tokens": 80,
        "total_prompt_tokens": 1730,
        "completion_tokens": 420,
        "finish_reason": "STOP",
        "model_version": "gemini-1.5-pro",
        "temperature": Decimal("0.10"),
        "error_code": None,
        "ocr_duration_ms": 3200,
        "embedding_duration_ms": 250,
        "retrieval_duration_ms": 110,
        "llm_duration_ms": 3800,
        "total_duration_ms": 7400,
        "created_at": datetime(2025, 3, 1, 14, 0, tzinfo=timezone.utc),
    },

    # 4. Embedding call — upload pipeline,
    #    session_id NULL, raw_response NULL
    {
        "id": uuid.UUID("31bc7458-a2ca-4727-8eeb-138c49385c1e"),
        "session_id": None,             # embedding has no session
        "message_id": None,
        "report_id": uuid.UUID("9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6"),  # CBC report
        "call_type": "embedding",
        "assembled_prompt_enc": "AES256:enc:...chunk_text_batch...",
        "raw_response_enc": None,       # no LLM response for embedding
        "guardrail_trigger_text_enc": None,
        "error_message_enc": None,
        "guardrail_fired": False,
        "guardrail_check": None,
        "retrieved_chunk_ids": None,
        "cosine_scores": None,
        "panel_coverage": None,
        "zone1_tokens": 0,
        "zone2_tokens": 0,
        "zone3_tokens": 0,
        "zone4_tokens": 0,
        "total_prompt_tokens": 1200,    # total chunk tokens embedded
        "completion_tokens": 0,
        "finish_reason": "STOP",
        "model_version": "gemini-1.5-pro",
        "temperature": Decimal("0.00"),
        "error_code": None,
        "ocr_duration_ms": 2800,
        "embedding_duration_ms": 340,
        "retrieval_duration_ms": None,
        "llm_duration_ms": 340,
        "total_duration_ms": 3200,
        "created_at": datetime(2025, 4, 5, 8, 0, tzinfo=timezone.utc),
    },

    # 5. Chat call — Vertex AI error,
    #    raw_response NULL, error_code set
   
]


def seed_llm_traces(db: Session):
    print("➡️ Seeding triage results...")

    for data in dummy_llm_traces:
        db.merge(LLMTrace(**data))  # safe re-run

    db.flush()  # no commit here
    db.commit() 

    print(f"✅ Seeded {len(dummy_llm_traces)} llm traces")