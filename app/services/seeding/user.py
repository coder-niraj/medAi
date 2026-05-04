import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.user import User

dummy_users = [
    {
        "id": uuid.UUID("604c02aa-b8f3-4c9c-b500-40bd75eec8c1"),
        "name": "Ahmed Al-Rashidi",
        "email_enc": "AES256:enc:ahmed.alrashidi@gmail.com",
        "phone_enc": "AES256:enc:+966501234567",
        "dob_enc": "AES256:enc:1990-05-15",
        "preferred_language": "ar",
        "role": "patient",
        "firebase_uid": "firebase_uid_001",
        "created_at": datetime(2025, 1, 10, 8, 0, tzinfo=timezone.utc),
        "consent_given_at": datetime(2025, 1, 10, 8, 5, tzinfo=timezone.utc),
        "research_consent": True,
        "triage_count": 2,
    },
    {
        "id": uuid.UUID("043262a7-c7c5-4db0-bd64-77a664535f5c"),
        "name": "Sarah Mitchell",
        "email_enc": "AES256:enc:sarah.mitchell@gmail.com",
        "phone_enc": "AES256:enc:+971501234567",
        "dob_enc": "AES256:enc:1985-09-22",
        "preferred_language": "en",
        "role": "patient",
        "firebase_uid": "firebase_uid_002",
        "created_at": datetime(2025, 2, 14, 10, 30, tzinfo=timezone.utc),
        "consent_given_at": datetime(2025, 2, 14, 10, 35, tzinfo=timezone.utc),
        "research_consent": False,
        "triage_count": 1,
    },
    {
        "id": uuid.UUID("ff4975b9-2b05-4625-b9bc-e614af62e323"),
        "name": "Dr. Khalid Al-Otaibi",
        "email_enc": "AES256:enc:khalid.otaibi@hospital.sa",
        "phone_enc": "AES256:enc:+966509876543",
        "dob_enc": None,
        "preferred_language": "ar",
        "role": "doctor",
        "firebase_uid": "firebase_uid_003",
        "created_at": datetime(2025, 1, 5, 9, 0, tzinfo=timezone.utc),
        "consent_given_at": datetime(2025, 1, 5, 9, 10, tzinfo=timezone.utc),
        "research_consent": True,
        "triage_count": 0,
    },
    {
        "id": uuid.UUID("677f7b41-19fc-4d5f-8d4f-d65c716dfcae"),
        "name": "Fatima Al-Zahra",
        "email_enc": "AES256:enc:fatima.zahra@gmail.com",
        "phone_enc": None,
        "dob_enc": None,
        "preferred_language": "ar",
        "role": "patient",
        "firebase_uid": "firebase_uid_004",
        "created_at": datetime(2025, 3, 1, 14, 0, tzinfo=timezone.utc),
        "consent_given_at": None,
        "research_consent": False,
        "triage_count": 0,
    },
    {
        "id": uuid.UUID("9c4ed973-c0a2-4eab-9cd3-93b3ca8d8828"),
        "name": "Admin User",
        "email_enc": "AES256:enc:admin@platform.com",
        "phone_enc": None,
        "dob_enc": None,
        "preferred_language": "en",
        "role": "admin",
        "firebase_uid": "firebase_uid_005",
        "created_at": datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc),
        "consent_given_at": datetime(2025, 1, 1, 0, 1, tzinfo=timezone.utc),
        "research_consent": False,
        "triage_count": 0,
    },
]


def seed_users(db: Session):
    print("➡️ Seeding users...")

    users = [User(**data) for data in dummy_users]

    for user in users:
        db.merge(user)  # prevents duplicates on rerun

    db.flush()  # push to DB without committing yet
    db.commit() 

    print(f"✅ Seeded {len(users)} users")