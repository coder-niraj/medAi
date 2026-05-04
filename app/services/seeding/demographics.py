import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models.patient import PatientDemographics

dummy_patient_demographics = [
    {
        "id": uuid.UUID("48d53614-852d-4d30-8e07-4f5931e65341"),
        "user_id": uuid.UUID("604c02aa-b8f3-4c9c-b500-40bd75eec8c1"),  # Ahmed Al-Rashidi
        "age_range": "26-35",
        "gender": "male",
        "nationality": "SA",
        "region": "riyadh",
        "health_literacy": "medium",
        "chronic_conditions": ["diabetes", "hypertension"],
        "consent_for_research": True,
        "consent_given_at": datetime(2025, 1, 10, 8, 5, tzinfo=timezone.utc),
        "created_at": datetime(2025, 1, 10, 8, 5, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("ad7848b1-c6c7-44d7-9e72-488ed1763e5e"),
        "user_id": uuid.UUID("043262a7-c7c5-4db0-bd64-77a664535f5c"),  # Sarah Mitchell
        "age_range": "36-45",
        "gender": "female",
        "nationality": "AE",
        "region": "dubai",
        "health_literacy": "high",
        "chronic_conditions": [],
        "consent_for_research": False,
        "consent_given_at": None,       # no research consent given
        "created_at": datetime(2025, 2, 14, 10, 35, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("3d98909b-abd6-4b0c-9a26-1b5bf7ecd455"),
        "user_id": uuid.UUID("ff4975b9-2b05-4625-b9bc-e614af62e323"),  # Dr. Khalid
        "age_range": "46-55",
        "gender": "male",
        "nationality": "SA",
        "region": "jeddah",
        "health_literacy": "high",
        "chronic_conditions": [],
        "consent_for_research": True,
        "consent_given_at": datetime(2025, 1, 5, 9, 10, tzinfo=timezone.utc),
        "created_at": datetime(2025, 1, 5, 9, 10, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("33fde3f8-76db-4018-a40c-0d83154c895f"),
        "user_id": uuid.UUID("677f7b41-19fc-4d5f-8d4f-d65c716dfcae"),  # Fatima Al-Zahra
        "age_range": "56-65",
        "gender": "prefer_not_to_say",
        "nationality": "SA",
        "region": "eastern_province",
        "health_literacy": "low",
        "chronic_conditions": ["diabetes", "hypertension", "thyroid"],
        "consent_for_research": False,
        "consent_given_at": None,
        "created_at": datetime(2025, 3, 1, 14, 0, tzinfo=timezone.utc),
    },
]


def seed_patient_demographics(db: Session):
    print("➡️ Seeding triage results...")

    for data in dummy_patient_demographics:
        db.merge(PatientDemographics(**data))  # safe re-run

    db.flush()  # no commit here
    db.commit() 

    print(f"✅ Seeded {len(dummy_patient_demographics)} patient demographic")