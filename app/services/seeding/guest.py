import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.guest import GuestSession

dummy_guest_sessions = [
    {
        "id": uuid.UUID("5f43455a-cffb-486f-9977-81d58a060fb6"),
        "guest_token": "guest_token_001",
        "tos_accepted": True,
        "tos_accepted_at": datetime(2025, 1, 10, 8, 0, tzinfo=timezone.utc),
        "research_consent": False,
        "age_range": "26-35",
        "gender": "male",
        "nationality": "SA",
        "claimed_user_id": None,
        "created_at": datetime(2025, 1, 10, 8, 0, tzinfo=timezone.utc),
        "triage_count": 0,
        "expires_at": datetime(2025, 1, 11, 8, 0, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("7063a7d8-947b-4320-bc1f-24006d8c327f"),
        "guest_token": "guest_token_002",
        "tos_accepted": True,
        "tos_accepted_at": datetime(2025, 2, 14, 10, 0, tzinfo=timezone.utc),
        "research_consent": True,
        "age_range": "36-45",
        "gender": "female",
        "nationality": "AE",
        "claimed_user_id": None,
        "created_at": datetime(2025, 2, 14, 10, 0, tzinfo=timezone.utc),
        "triage_count": 1,
        "expires_at": datetime(2025, 2, 15, 10, 0, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("6a89299e-4554-4451-9bad-105506e0339c"),
        "guest_token": "guest_token_003",
        "tos_accepted": True,
        "tos_accepted_at": datetime(2025, 3, 1, 9, 0, tzinfo=timezone.utc),
        "research_consent": True,
        "age_range": "18-25",
        "gender": "female",
        "nationality": "SA",
        "claimed_user_id": uuid.UUID("043262a7-c7c5-4db0-bd64-77a664535f5c"),  # Sarah Mitchell
        "created_at": datetime(2025, 3, 1, 9, 0, tzinfo=timezone.utc),
        "triage_count": 1,
        "expires_at": datetime(2025, 3, 2, 9, 0, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("b8d540e6-a340-4e8d-8345-5d25f63104a6"),
        "guest_token": "guest_token_004",
        "tos_accepted": True,
        "tos_accepted_at": datetime(2025, 1, 1, 6, 0, tzinfo=timezone.utc),
        "research_consent": False,
        "age_range": "46-55",
        "gender": "male",
        "nationality": "KW",
        "claimed_user_id": None,
        "created_at": datetime(2025, 1, 1, 6, 0, tzinfo=timezone.utc),
        "triage_count": 0,
        "expires_at": datetime(2025, 1, 2, 6, 0, tzinfo=timezone.utc),  # expired
    },
    {
        "id": uuid.UUID("946f7183-7da6-4ba6-8281-6566fcdfe8ab"),
        "guest_token": "guest_token_005",
        "tos_accepted": False,
        "tos_accepted_at": None,
        "research_consent": False,
        "age_range": "56-65",
        "gender": "prefer_not_to_say",
        "nationality": None,
        "claimed_user_id": None,
        "created_at": datetime(2025, 4, 10, 12, 0, tzinfo=timezone.utc),
        "triage_count": 0,
        "expires_at": datetime(2025, 4, 11, 12, 0, tzinfo=timezone.utc),
    },
]


def seed_guest_sessions(db: Session):
    print("➡️ Seeding triage results...")

    for data in dummy_guest_sessions:
        db.merge(GuestSession(**data))  # safe re-run

    db.flush()  # no commit here
    db.commit() 

    print(f"✅ Seeded {len(dummy_guest_sessions)} guest sessions")