import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.chatSessions import ChatSession

dummy_chat_sessions = [
    {
        "id": uuid.UUID("4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae"),
        "user_id": uuid.UUID("604c02aa-b8f3-4c9c-b500-40bd75eec8c1"),  # Ahmed Al-Rashidi
        "report_id": uuid.UUID("9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6"),  # CBC report
        "mode": "document",
        "title": "تحليل CBC - يناير 2025",
        "language": "ar",
        "is_guest": False,
        "guest_token": None,
        "triage_status": None,
        "triage_result": None,
        "triage_completed_at": None,
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 557722, tzinfo=timezone.utc),
        "last_message_at": datetime(2026, 5, 1, 6, 28, 30, 557722, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("e2385da2-08c4-4b7e-af76-97b947567d09"),
        "user_id": uuid.UUID("043262a7-c7c5-4db0-bd64-77a664535f5c"),  # Sarah Mitchell
        "report_id": None,
        "mode": "triage",
        "title": "Symptom check — headache and nausea",
        "language": "en",
        "is_guest": False,
        "guest_token": None,
        "triage_status": "completed",
        "triage_result": "yellow",
        "triage_completed_at": datetime(2026, 5, 1, 6, 28, 30, 557722, tzinfo=timezone.utc),
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 557722, tzinfo=timezone.utc),
        "last_message_at": datetime(2026, 5, 1, 6, 28, 30, 557722, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("92b927dc-115b-41a1-a0aa-0abf81528e5c"),
        "user_id": None,                # guest — no user_id
        "report_id": None,
        "mode": "triage",
        "title": None,                  # no title yet — triage in progress
        "language": "ar",
        "is_guest": True,
        "guest_token": "guest:bb2dc801-b094-471d-85f0-4733956925df",
        "triage_status": "in_progress",
        "triage_result": None,          # not completed yet
        "triage_completed_at": None,
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 557722, tzinfo=timezone.utc),
        "last_message_at": datetime(2026, 5, 1, 6, 28, 30, 557722, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("7f9950a5-8f1d-4c79-967e-e356355deac0"),
        "user_id": uuid.UUID("043262a7-c7c5-4db0-bd64-77a664535f5c"),  # Sarah Mitchell
        "report_id": None,
        "mode": "document",
        "title": "Full checkup review — March 2025",
        "language": "en",
        "is_guest": False,
        "guest_token": None,
        "triage_status": None,
        "triage_result": None,
        "triage_completed_at": None,
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 557722, tzinfo=timezone.utc),
        "last_message_at": datetime(2026, 5, 1, 6, 28, 30, 557722, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("e794391b-accd-4d36-915a-6140c93daffe"),
        "user_id": uuid.UUID("604c02aa-b8f3-4c9c-b500-40bd75eec8c1"),  # Ahmed Al-Rashidi
        "report_id": None,
        "mode": "general",
        "title": "سؤال عن أدوية ضغط الدم",
        "language": "ar",
        "is_guest": False,
        "guest_token": None,
        "triage_status": None,
        "triage_result": None,
        "triage_completed_at": None,
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 557722, tzinfo=timezone.utc),
        "last_message_at": datetime(2026, 5, 1, 6, 28, 30, 557722, tzinfo=timezone.utc),
    },
]


def seed_chat_sessions(db: Session):
    print("➡️ Seeding triage results...")

    for data in dummy_chat_sessions:
        db.merge(ChatSession(**data))  # safe re-run

    db.flush()  # no commit here
    db.commit() 

    print(f"✅ Seeded {len(dummy_chat_sessions)} clinical review")