import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models.clinicalReview import ClinicianReview

dummy_clinician_reviews = [
    # 1. Perfect review — all 5 stars, no errors,
    #    safe to train on, well above 30 sec threshold
    {
        "id": uuid.UUID("adef58c6-7a61-4cf1-8f95-91791699efaa"),
        "message_id": uuid.UUID("28fd1664-1c46-4353-9b38-e14291ab4f59"),  # Arabic user message
        "reviewer_id": uuid.UUID("ff4975b9-2b05-4625-b9bc-e614af62e323"), # Dr. Khalid
        "accuracy_rating": 5,
        "safety_rating": 5,
        "completeness_rating": 5,
        "contains_error": False,
        "error_description": None,
        "suggested_correction": None,
        "is_safe_to_train_on": True,
        "reviewed_at": datetime(2026, 5, 1, 6, 28, 30, 557717, tzinfo=timezone.utc),
        "review_duration_sec": 142,     # well above 30 sec threshold
    },

    # 2. Partial review — completeness low,
    #    correction suggested, still safe to train on
    {
        "id": uuid.UUID("45177fee-fdf2-433d-988c-2f1c8e7d71c2"),
        "message_id": uuid.UUID("636a35a4-7548-4720-afe7-6590b9524eff"),  # assistant Arabic response
        "reviewer_id": uuid.UUID("ff4975b9-2b05-4625-b9bc-e614af62e323"), # Dr. Khalid
        "accuracy_rating": 4,
        "safety_rating": 5,
        "completeness_rating": 3,       # missing fasting retest mention
        "contains_error": False,
        "error_description": None,
        "suggested_correction": "Response should mention that a fasting lipid retest is typically required before clinical decisions are made on borderline results.",
        "is_safe_to_train_on": True,    # safe despite incomplete
        "reviewed_at": datetime(2026, 5, 1, 6, 28, 30, 557717, tzinfo=timezone.utc),
        "review_duration_sec": 98,
    },

    # 3. Failed review — contains clinical error,
    #    wrong HbA1c target cited, NOT safe to train on
    {
        "id": uuid.UUID("96c670b8-1a3a-4c3a-9929-1ac1b378f9ea"),
        "message_id": uuid.UUID("caf6858e-f52b-4371-a31a-00b8112698d1"),  # triage user message
        "reviewer_id": uuid.UUID("ff4975b9-2b05-4625-b9bc-e614af62e323"), # Dr. Khalid
        "accuracy_rating": 2,           # clinical error present
        "safety_rating": 3,             # could cause patient anxiety
        "completeness_rating": 3,
        "contains_error": True,
        "error_description": "The response stated the HbA1c target for diabetic patients is below 6.0%. The correct general target for most adults with type 2 diabetes is below 7.0% (ADA guideline). Citing 6.0% could cause unnecessary patient anxiety.",
        "suggested_correction": "Replace '6.0%' with '7.0%' and note that individual targets vary — some patients may have a higher target set by their doctor depending on age and comorbidities.",
        "is_safe_to_train_on": False,   # blocked from fine-tuning
        "reviewed_at": datetime(2026, 5, 1, 6, 28, 30, 557717, tzinfo=timezone.utc),
        "review_duration_sec": 187,     # thorough review
    },
]




def seed_clinician_reviews(db: Session):
    print("➡️ Seeding triage results...")

    for data in dummy_clinician_reviews:
        db.merge(ClinicianReview(**data))  # safe re-run

    db.flush()  # no commit here
    db.commit() 

    print(f"✅ Seeded {len(dummy_clinician_reviews)} clinical review")