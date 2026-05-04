import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.chatMessage import ChatMessage

dummy_chat_messages = [
    {
        "id": uuid.UUID("28fd1664-1c46-4353-9b38-e14291ab4f59"),
        "session_id": uuid.UUID("4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae"),
        "role": "user",
        "content_enc": "AES256:enc:...ما معنى ارتفاع خلايا الدم البيضاء؟...",
        "retrieved_chunk_ids": None,
        "finish_reason": None,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "patient_rating": None,
        "patient_rating_at": None,
        "user_feedback_flag": None,
        "guardrail_triggered": False,
        "guardrail_reason": None,
        "fallback_used": False,
        "response_language": None,
        "question_language": "ar",
        "question_category": "lab_explanation",
        "ft_eligible": None,
        "ft_excluded_reason": None,
        "created_at": datetime(2025, 1, 10, 9, 30, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("636a35a4-7548-4720-afe7-6590b9524eff"),
        "session_id": uuid.UUID("4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae"),
        "role": "assistant",
        "content_enc": "AES256:enc:...ارتفاع خلايا الدم البيضاء يشير إلى...",
        "retrieved_chunk_ids": [
            uuid.UUID("a29bc5a5-af1b-469e-941a-22931f49a8df"),
            uuid.UUID("c71f80c8-8731-4cc1-a9e0-81ec478ff795"),
            uuid.UUID("63e32535-308f-4046-a138-75873da8677a"),
        ],
        "finish_reason": "STOP",
        "prompt_tokens": 1600,
        "completion_tokens": 320,
        "patient_rating": 5,
        "patient_rating_at": datetime(2025, 1, 10, 9, 32, tzinfo=timezone.utc),
        "user_feedback_flag": "helpful",
        "guardrail_triggered": False,
        "guardrail_reason": None,
        "fallback_used": False,
        "response_language": "ar",
        "question_language": "ar",
        "question_category": "lab_explanation",
        "ft_eligible": True,
        "ft_excluded_reason": None,
        "created_at": datetime(2025, 1, 10, 9, 31, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("caf6858e-f52b-4371-a31a-00b8112698d1"),
        "session_id": uuid.UUID("e2385da2-08c4-4b7e-af76-97b947567d09"),
        "role": "user",
        "content_enc": "AES256:enc:...I have chest pain and shortness of breath...",
        "retrieved_chunk_ids": None,
        "finish_reason": None,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "patient_rating": None,
        "patient_rating_at": None,
        "user_feedback_flag": None,
        "guardrail_triggered": False,
        "guardrail_reason": None,
        "fallback_used": False,
        "response_language": None,
        "question_language": "en",
        "question_category": "symptom_triage",
        "ft_eligible": None,
        "ft_excluded_reason": None,
        "created_at": datetime(2025, 2, 14, 11, 0, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("45d2de49-527e-430c-852e-7adcdcea2e3f"),
        "session_id": uuid.UUID("4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae"),
        "role": "assistant",
        "content_enc": "AES256:enc:...your HbA1c level suggests...",
        "retrieved_chunk_ids": [
            uuid.UUID("a709a7e2-c00f-46a3-b726-d81f5fa6b63f"),
            uuid.UUID("8afd8739-bb4b-4cf3-82ba-71cfd36c48d1"),
        ],
        "finish_reason": "STOP",
        "prompt_tokens": 1400,
        "completion_tokens": 280,
        "patient_rating": 2,
        "patient_rating_at": datetime(2025, 4, 10, 10, 5, tzinfo=timezone.utc),
        "user_feedback_flag": "wrong",
        "guardrail_triggered": False,
        "guardrail_reason": None,
        "fallback_used": False,
        "response_language": "en",
        "question_language": "en",
        "question_category": "lab_explanation",
        "ft_eligible": False,
        "ft_excluded_reason": "patient_rating_below_threshold",
        "created_at": datetime(2025, 4, 10, 10, 4, tzinfo=timezone.utc),
    },
]

def seed_chat_messages(db: Session):
    print("➡️ Seeding triage results...")

    for data in dummy_chat_messages:
        db.merge(ChatMessage(**data))  # safe re-run

    db.flush()  # no commit here
    db.commit() 

    print(f"✅ Seeded {len(dummy_chat_messages)} clinical review")