import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.triage import TriageResult

dummy_triage_results = [
    {
        "id": uuid.UUID("472f5b9f-cbcc-4062-8c4c-3a05227c529c"),
        "session_id": uuid.UUID("4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae"),  # Ahmed document session
        "user_id": uuid.UUID("604c02aa-b8f3-4c9c-b500-40bd75eec8c1"),    # Ahmed Al-Rashidi
        "result_level": "green",
        "urgency_score": 2,             # Green = 1-3
        "result_summary_enc": "AES256:enc:...mild_symptoms_summary...",
        "result_recommendation_enc": "AES256:enc:...rest_and_hydration...",
        "symptoms_reported_enc": "AES256:enc:...headache_fatigue...",
        "result_language": "ar",
        "generated_at": datetime(2025, 1, 10, 9, 30, tzinfo=timezone.utc),
        "viewed_at": datetime(2025, 1, 10, 9, 31, tzinfo=timezone.utc),
        "patient_acted": "monitored_at_home",
    },
    {
        "id": uuid.UUID("ebbad186-7815-45e4-a6d0-2878f1aaf1d7"),
        "session_id": uuid.UUID("e2385da2-08c4-4b7e-af76-97b947567d09"),  # Sarah triage session
        "user_id": uuid.UUID("043262a7-c7c5-4db0-bd64-77a664535f5c"),    # Sarah Mitchell
        "result_level": "yellow",
        "urgency_score": 5,             # Yellow = 4-6
        "result_summary_enc": "AES256:enc:...moderate_symptoms_summary...",
        "result_recommendation_enc": "AES256:enc:...visit_doctor_within_48hrs...",
        "symptoms_reported_enc": "AES256:enc:...chest_discomfort_shortness_of_breath...",
        "result_language": "en",
        "generated_at": datetime(2025, 2, 14, 11, 0, tzinfo=timezone.utc),
        "viewed_at": datetime(2025, 2, 14, 11, 2, tzinfo=timezone.utc),
        "patient_acted": "sought_care",
    },
    {
        "id": uuid.UUID("df42b479-49c4-43dc-b781-b02f8597afe7"),
        "session_id": uuid.UUID("e794391b-accd-4d36-915a-6140c93daffe"),  # Ahmed general session
        "user_id": uuid.UUID("604c02aa-b8f3-4c9c-b500-40bd75eec8c1"),    # Ahmed Al-Rashidi
        "result_level": "red",
        "urgency_score": 9,             # Red = 7-10
        "result_summary_enc": "AES256:enc:...severe_symptoms_summary...",
        "result_recommendation_enc": "AES256:enc:...seek_emergency_care_immediately...",
        "symptoms_reported_enc": "AES256:enc:...chest_pain_sweating_arm_pain...",
        "result_language": "ar",
        "generated_at": datetime(2025, 3, 1, 14, 0, tzinfo=timezone.utc),
        "viewed_at": datetime(2025, 3, 1, 14, 1, tzinfo=timezone.utc),
        "patient_acted": "ignored",     # flagged for 48hr follow up
    },
]


def seed_triage_results(db: Session):
    print("➡️ Seeding triage results...")

    for data in dummy_triage_results:
        db.merge(TriageResult(**data))  # safe re-run

    db.flush()  # no commit here
    db.commit() 

    print(f"✅ Seeded {len(dummy_triage_results)} triage results")