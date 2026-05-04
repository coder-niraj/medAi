from datetime import datetime, timezone
from decimal import Decimal
import uuid
import random

now = datetime.now(timezone.utc)

dummy_users = [
    # 1. Arabic patient with full consent
    {
        "id": "604c02aa-b8f3-4c9c-b500-40bd75eec8c1",
        "name": "Ahmed Al-Rashidi",
        "email_enc": "AES256:enc:ahmed.alrashidi@gmail.com",
        "phone_enc": "AES256:enc:+966501234567",
        "dob_enc": "AES256:enc:1990-05-15",
        "preferred_language": "ar",
        "role": "patient",
        "firebase_uid": "firebase_uid_001",
        "created_at": datetime(2025, 1, 10, 8, 0, 0),
        "consent_given_at": datetime(2025, 1, 10, 8, 5, 0),
        "research_consent": True,
        "triage_count": 2,
    },

    # 2. English patient no research consent
    {
        "id": "043262a7-c7c5-4db0-bd64-77a664535f5c",
        "name": "Sarah Mitchell",
        "email_enc": "AES256:enc:sarah.mitchell@gmail.com",
        "phone_enc": "AES256:enc:+971501234567",
        "dob_enc": "AES256:enc:1985-09-22",
        "preferred_language": "en",
        "role": "patient",
        "firebase_uid": "firebase_uid_002",
        "created_at": datetime(2025, 2, 14, 10, 30, 0),
        "consent_given_at": datetime(2025, 2, 14, 10, 35, 0),
        "research_consent": False,
        "triage_count": 1,
    },

    # 3. Doctor role
    {
        "id":"ff4975b9-2b05-4625-b9bc-e614af62e323",
        "name": "Dr. Khalid Al-Otaibi",
        "email_enc": "AES256:enc:khalid.otaibi@hospital.sa",
        "phone_enc": "AES256:enc:+966509876543",
        "dob_enc": None,
        "preferred_language": "ar",
        "role": "doctor",
        "firebase_uid": "firebase_uid_003",
        "created_at": datetime(2025, 1, 5, 9, 0, 0),
        "consent_given_at": datetime(2025, 1, 5, 9, 10, 0),
        "research_consent": True,
        "triage_count": 0,
    },

    # 4. Patient consent NOT yet given — AI features blocked
    {
        "id": "677f7b41-19fc-4d5f-8d4f-d65c716dfcae",
        "name": "Fatima Al-Zahra",
        "email_enc": "AES256:enc:fatima.zahra@gmail.com",
        "phone_enc": None,
        "dob_enc": None,
        "preferred_language": "ar",
        "role": "patient",
        "firebase_uid": "firebase_uid_004",
        "created_at": datetime(2025, 3, 1, 14, 0, 0),
        "consent_given_at": None,
        "research_consent": False,
        "triage_count": 0,
    },

    # 5. Admin role
    {
        "id": "9c4ed973-c0a2-4eab-9cd3-93b3ca8d8828",
        "name": "Admin User",
        "email_enc": "AES256:enc:admin@platform.com",
        "phone_enc": None,
        "dob_enc": None,
        "preferred_language": "en",
        "role": "admin",
        "firebase_uid": "firebase_uid_005",
        "created_at": datetime(2025, 1, 1, 0, 0, 0),
        "consent_given_at": datetime(2025, 1, 1, 0, 1, 0),
        "research_consent": False,
        "triage_count": 0,
    },
]



dummy_guest_sessions = [
    # 1. Fresh guest — ToS accepted, triage not yet started
    {
        "id": "5f43455a-cffb-486f-9977-81d58a060fb6",
        "guest_token": "guest_token_001",
        "tos_accepted": True,
        "tos_accepted_at": datetime(2025, 1, 10, 8, 0, 0, tzinfo=timezone.utc),
        "research_consent": False,
        "age_range": "26-35",
        "gender": "male",
        "nationality": "SA",
        "claimed_user_id": None,
        "created_at": datetime(2025, 1, 10, 8, 0, 0, tzinfo=timezone.utc),
        "triage_count": 0,
        "expires_at": datetime(2025, 1, 11, 8, 0, 0, tzinfo=timezone.utc),
    },

    # 2. Guest with research consent — triage completed
    {
        "id": "7063a7d8-947b-4320-bc1f-24006d8c327f",
        "guest_token": "guest_token_002",
        "tos_accepted": True,
        "tos_accepted_at": datetime(2025, 2, 14, 10, 0, 0, tzinfo=timezone.utc),
        "research_consent": True,
        "age_range": "36-45",
        "gender": "female",
        "nationality": "AE",
        "claimed_user_id": None,
        "created_at": datetime(2025, 2, 14, 10, 0, 0, tzinfo=timezone.utc),
        "triage_count": 1,
        "expires_at": datetime(2025, 2, 15, 10, 0, 0, tzinfo=timezone.utc),
    },

    # 3. Guest session claimed by registered user
    {
        "id": "6a89299e-4554-4451-9bad-105506e0339c",
        "guest_token": "guest_token_003",
        "tos_accepted": True,
        "tos_accepted_at": datetime(2025, 3, 1, 9, 0, 0, tzinfo=timezone.utc),
        "research_consent": True,
        "age_range": "18-25",
        "gender": "female",
        "nationality": "SA",
        "claimed_user_id":"043262a7-c7c5-4db0-bd64-77a664535f5c",  # linked to registered user
        "created_at": datetime(2025, 3, 1, 9, 0, 0, tzinfo=timezone.utc),
        "triage_count": 1,
        "expires_at": datetime(2025, 3, 2, 9, 0, 0, tzinfo=timezone.utc),
    },

    # 4. Expired guest session — not claimed, cleanup job should delete
    {
        "id": "b8d540e6-a340-4e8d-8345-5d25f63104a6",
        "guest_token": "guest_token_004",
        "tos_accepted": True,
        "tos_accepted_at": datetime(2025, 1, 1, 6, 0, 0, tzinfo=timezone.utc),
        "research_consent": False,
        "age_range": "46-55",
        "gender": "male",
        "nationality": "KW",
        "claimed_user_id": None,
        "created_at": datetime(2025, 1, 1, 6, 0, 0, tzinfo=timezone.utc),
        "triage_count": 0,
        "expires_at": datetime(2025, 1, 2, 6, 0, 0, tzinfo=timezone.utc),  # expired
    },

    # 5. Guest ToS NOT accepted — AI features blocked
    {
        "id": "946f7183-7da6-4ba6-8281-6566fcdfe8ab",
        "guest_token": "guest_token_005",
        "tos_accepted": False,
        "tos_accepted_at": None,
        "research_consent": False,
        "age_range": "56-65",
        "gender": "prefer_not_to_say",
        "nationality": None,
        "claimed_user_id": None,
        "created_at": datetime(2025, 4, 10, 12, 0, 0, tzinfo=timezone.utc),
        "triage_count": 0,
        "expires_at": datetime(2025, 4, 11, 12, 0, 0, tzinfo=timezone.utc),
    },
]


# Reference user_id from dummy_users
user_id_1 = "604c02aa-b8f3-4c9c-b500-40bd75eec8c1"  
user_id_2 = "043262a7-c7c5-4db0-bd64-77a664535f5c"  

dummy_reports = [
    # 1. Single panel CBC report — ready, Arabic, high quality
    {
        "id": "9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6",
        "user_id": user_id_1,
        "file_url": f"gs://med-ai-bucket/{user_id_1}/cbc_report_001.pdf",
        "display_name": "CBC January 2025",
        "ocr_text_enc": "AES256:enc:...cbc_ocr_text...",
        "summary_enc": "AES256:enc:...cbc_summary...",
        "report_type": "cbc",
        "report_subtype": "cbc_with_differential",
        "detected_panels": ["CBC"],
        "panel_count": 1,
        "cardiac_urgency_flag": False,
        "detected_language": "ar",
        "is_bilingual": False,
        "report_language_mix": {"ar": 1.0, "en": 0.0},
        "status": "ready",
        "ocr_avg_confidence": 0.95,
        "ocr_min_confidence": 0.91,
        "document_quality": "high",
        "low_confidence_blocks": [],
        "uploaded_at": datetime(2025, 1, 10, 9, 0, 0, tzinfo=timezone.utc),
        "retention_expires_at": datetime(2027, 1, 10, 9, 0, 0, tzinfo=timezone.utc),
    },

    # 2. Full checkup — multi panel, bilingual, cardiac urgency flagged
    {
        "id": "df7b626b-0ea5-425a-940e-44fb037e88a6",
        "user_id": user_id_1,
        "file_url": f"gs://med-ai-bucket/{user_id_1}/full_checkup_001.pdf",
        "display_name": "Full Body Checkup March 2025",
        "ocr_text_enc": "AES256:enc:...full_checkup_ocr_text...",
        "summary_enc": "AES256:enc:...full_checkup_summary...",
        "report_type": "full_checkup",
        "report_subtype": None,
        "detected_panels": ["CBC", "Lipid Panel", "LFTs", "TFTs", "Cardiac Enzymes"],
        "panel_count": 5,
        "cardiac_urgency_flag": True,  # cardiac enzymes high/critical
        "detected_language": "bilingual",
        "is_bilingual": True,
        "report_language_mix": {"ar": 0.65, "en": 0.35},
        "status": "ready",
        "ocr_avg_confidence": 0.88,
        "ocr_min_confidence": 0.76,
        "document_quality": "medium",
        "low_confidence_blocks": [
            {"block_id": "b001", "text": "...", "confidence": 0.74},
            {"block_id": "b002", "text": "...", "confidence": 0.71},
        ],
        "uploaded_at": datetime(2025, 3, 1, 10, 0, 0, tzinfo=timezone.utc),
        "retention_expires_at": datetime(2027, 3, 1, 10, 0, 0, tzinfo=timezone.utc),
    },

    # 3. Image only report — no OCR, no AI pipeline
    {
        "id": "50318f00-371b-482c-8c8d-1ab7e0f440df",
        "user_id": user_id_2,
        "file_url": f"gs://med-ai-bucket/{user_id_2}/xray_001.jpg",
        "display_name": "Chest X-Ray February 2025",
        "ocr_text_enc": None,   # NULL for image_only
        "summary_enc": None,    # NULL for image_only
        "report_type": "imaging_report",
        "report_subtype": None,
        "detected_panels": None,
        "panel_count": 1,
        "cardiac_urgency_flag": False,
        "detected_language": None,
        "is_bilingual": False,
        "report_language_mix": None,
        "status": "image_only",  # OCR pipeline NOT initiated
        "ocr_avg_confidence": None,
        "ocr_min_confidence": None,
        "document_quality": None,
        "low_confidence_blocks": None,
        "uploaded_at": datetime(2025, 2, 14, 11, 0, 0, tzinfo=timezone.utc),
        "retention_expires_at": datetime(2027, 2, 14, 11, 0, 0, tzinfo=timezone.utc),
    },

    # 4. OCR failed report — low quality scan
    {
        "id": "f1ae82e6-c118-4de0-bd1b-97adb88eddf2",
        "user_id": user_id_2,
        "file_url": f"gs://med-ai-bucket/{user_id_2}/lipid_scan_001.pdf",
        "display_name": "Lipid Panel April 2025",
        "ocr_text_enc": None,
        "summary_enc": None,
        "report_type": "lipid_panel",
        "report_subtype": None,
        "detected_panels": None,
        "panel_count": 1,
        "cardiac_urgency_flag": False,
        "detected_language": None,
        "is_bilingual": False,
        "report_language_mix": None,
        "status": "ocr_failed",
        "ocr_avg_confidence": 0.60,
        "ocr_min_confidence": 0.45,
        "document_quality": "low",
        "low_confidence_blocks": [
            {"block_id": "b001", "text": "...", "confidence": 0.55},
            {"block_id": "b002", "text": "...", "confidence": 0.45},
        ],
        "uploaded_at": datetime(2025, 4, 5, 8, 0, 0, tzinfo=timezone.utc),
        "retention_expires_at": datetime(2027, 4, 5, 8, 0, 0, tzinfo=timezone.utc),
    },

    # 5. Diabetes panel — English, just uploaded, processing not complete
    {
        "id": "260bbbfe-2b9c-4d9a-82a2-29134ba2f98c",
        "user_id": user_id_1,
        "file_url": f"gs://med-ai-bucket/{user_id_1}/diabetes_001.pdf",
        "display_name": "HbA1c Diabetes Panel May 2025",
        "ocr_text_enc": None,
        "summary_enc": None,
        "report_type": "diabetes_panel",
        "report_subtype": None,
        "detected_panels": None,
        "panel_count": 1,
        "cardiac_urgency_flag": False,
        "detected_language": "en",
        "is_bilingual": False,
        "report_language_mix": {"ar": 0.0, "en": 1.0},
        "status": "uploaded",  # pipeline not started yet
        "ocr_avg_confidence": None,
        "ocr_min_confidence": None,
        "document_quality": None,
        "low_confidence_blocks": None,
        "uploaded_at": datetime(2025, 5, 1, 7, 0, 0, tzinfo=timezone.utc),
        "retention_expires_at": datetime(2027, 5, 1, 7, 0, 0, tzinfo=timezone.utc),
    },
]


# Reference same user_ids from dummy_users
user_id_1 = "604c02aa-b8f3-4c9c-b500-40bd75eec8c1"  
user_id_2 = "043262a7-c7c5-4db0-bd64-77a664535f5c"  
user_id_3 = "ff4975b9-2b05-4625-b9bc-e614af62e323"  # Dr. Khalid Al-Otaibi
user_id_4 = "677f7b41-19fc-4d5f-8d4f-d65c716dfcae"  # Fatima Al-Zahra


dummy_patient_demographics = [
    # 1. Saudi male, Riyadh, research consent given, chronic conditions
    {
        "id": "48d53614-852d-4d30-8e07-4f5931e65341",
        "user_id": user_id_1,
        "age_range": "26-35",
        "gender": "male",
        "nationality": "SA",
        "region": "riyadh",
        "health_literacy": "medium",
        "chronic_conditions": ["diabetes", "hypertension"],
        "consent_for_research": True,
        "consent_given_at": datetime(2025, 1, 10, 8, 5, 0, tzinfo=timezone.utc),
        "created_at": datetime(2025, 1, 10, 8, 5, 0, tzinfo=timezone.utc),
    },

    # 2. UAE female, Dubai, no research consent, no chronic conditions
    {
        "id":"ad7848b1-c6c7-44d7-9e72-488ed1763e5e",
        "user_id": user_id_2,
        "age_range": "36-45",
        "gender": "female",
        "nationality": "AE",
        "region": "dubai",
        "health_literacy": "high",
        "chronic_conditions": [],
        "consent_for_research": False,
        "consent_given_at": None,  # no research consent given
        "created_at": datetime(2025, 2, 14, 10, 35, 0, tzinfo=timezone.utc),
    },

    # 3. Doctor — Jeddah, research consent, no chronic conditions
    {
        "id": "3d98909b-abd6-4b0c-9a26-1b5bf7ecd455",
        "user_id": user_id_3,
        "age_range": "46-55",
        "gender": "male",
        "nationality": "SA",
        "region": "jeddah",
        "health_literacy": "high",
        "chronic_conditions": [],
        "consent_for_research": True,
        "consent_given_at": datetime(2025, 1, 5, 9, 10, 0, tzinfo=timezone.utc),
        "created_at": datetime(2025, 1, 5, 9, 10, 0, tzinfo=timezone.utc),
    },

    # 4. Saudi female, Eastern Province, prefer not to say gender,
    #    low health literacy, multiple chronic conditions
    {
        "id": "33fde3f8-76db-4018-a40c-0d83154c895f",
        "user_id": user_id_4,
        "age_range": "56-65",
        "gender": "prefer_not_to_say",
        "nationality": "SA",
        "region": "eastern_province",
        "health_literacy": "low",
        "chronic_conditions": ["diabetes", "hypertension", "thyroid"],
        "consent_for_research": False,
        "consent_given_at": None,
        "created_at": datetime(2025, 3, 1, 14, 0, 0, tzinfo=timezone.utc),
    },

    
    
]



# Reference ids from previous dummy data
session_id_1 = "4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae"
session_id_2 = "e2385da2-08c4-4b7e-af76-97b947567d09"
session_id_3 ="e794391b-accd-4d36-915a-6140c93daffe"


user_id_1 = "604c02aa-b8f3-4c9c-b500-40bd75eec8c1"  
user_id_2 = "043262a7-c7c5-4db0-bd64-77a664535f5c"  


dummy_triage_results = [
    # 1. Green result — registered user, low urgency, acted monitored at home
    {
        "id": "472f5b9f-cbcc-4062-8c4c-3a05227c529c",
        "session_id": session_id_1,
        "user_id": user_id_1,
        "result_level": "green",
        "urgency_score": 2,  # Green = 1-3
        "result_summary_enc": "AES256:enc:...mild_symptoms_summary...",
        "result_recommendation_enc": "AES256:enc:...rest_and_hydration...",
        "symptoms_reported_enc": "AES256:enc:...headache_fatigue...",
        "result_language": "ar",
        "generated_at": datetime(2025, 1, 10, 9, 30, 0, tzinfo=timezone.utc),
        "viewed_at": datetime(2025, 1, 10, 9, 31, 0, tzinfo=timezone.utc),
        "patient_acted": "monitored_at_home",
    },

    # 2. Yellow result — registered user, medium urgency, sought care
    {
        "id": "ebbad186-7815-45e4-a6d0-2878f1aaf1d7",
        "session_id": session_id_2,
        "user_id": user_id_2,
        "result_level": "yellow",
        "urgency_score": 5,  # Yellow = 4-6
        "result_summary_enc": "AES256:enc:...moderate_symptoms_summary...",
        "result_recommendation_enc": "AES256:enc:...visit_doctor_within_48hrs...",
        "symptoms_reported_enc": "AES256:enc:...chest_discomfort_shortness_of_breath...",
        "result_language": "en",
        "generated_at": datetime(2025, 2, 14, 11, 0, 0, tzinfo=timezone.utc),
        "viewed_at": datetime(2025, 2, 14, 11, 2, 0, tzinfo=timezone.utc),
        "patient_acted": "sought_care",
    },

    # 3. Red result — registered user, high urgency, ignored (48hr follow up)
    {
        "id": "df42b479-49c4-43dc-b781-b02f8597afe7",
        "session_id": session_id_3,
        "user_id": user_id_1,
        "result_level": "red",
        "urgency_score": 9,  # Red = 7-10
        "result_summary_enc": "AES256:enc:...severe_symptoms_summary...",
        "result_recommendation_enc": "AES256:enc:...seek_emergency_care_immediately...",
        "symptoms_reported_enc": "AES256:enc:...chest_pain_sweating_arm_pain...",
        "result_language": "ar",
        "generated_at": datetime(2025, 3, 1, 14, 0, 0, tzinfo=timezone.utc),
        "viewed_at": datetime(2025, 3, 1, 14, 1, 0, tzinfo=timezone.utc),
        "patient_acted": "ignored",  # flagged for follow up
    },
]



# Reference ids from previous dummy data
session_id_1 ="4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae"
session_id_2 = "e794391b-accd-4d36-915a-6140c93daffe"
session_id_3 = "e2385da2-08c4-4b7e-af76-97b947567d09"


message_id_1 = "28fd1664-1c46-4353-9b38-e14291ab4f59"
message_id_2 = "636a35a4-7548-4720-afe7-6590b9524eff"
message_id_3 = "caf6858e-f52b-4371-a31a-00b8112698d1"

report_id_1 ="9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6"  # CBC report
report_id_2 = "df7b626b-0ea5-425a-940e-44fb037e88a6"  # Full checkup report

dummy_llm_traces = [
    # 1. Chat call — document mode, RAG retrieval, no guardrail fired
    {
        "id": "978420fc-67ac-4c61-bcd3-b24f8035a3ee",
        "session_id": session_id_1,
        "message_id": message_id_1,
        "report_id": report_id_1,
        "call_type": "chat",
        "assembled_prompt_enc": "AES256:enc:...zone1+zone2+zone3+zone4...",
        "raw_response_enc": "AES256:enc:...gemini_raw_response...",
        "guardrail_trigger_text_enc": None,
        "error_message_enc": None,
        "guardrail_fired": False,
        "guardrail_check": None,
        "retrieved_chunk_ids": ["2f0de9e2-2c3a-4f85-9d1f-9baf0946360e", "c019ae54-4fd4-42be-a704-2d6ded509711", "2dc152ec-f82f-49c7-ae70-a350e1fc894c"],
        "cosine_scores": [0.92, 0.88, 0.85],
        "panel_coverage": {"CBC": 3},
        "zone1_tokens": 450,
        "zone2_tokens": 800,   # RAG chunks
        "zone3_tokens": 300,   # history
        "zone4_tokens": 50,    # user question
        "total_prompt_tokens": 1600,
        "completion_tokens": 320,
        "finish_reason": "STOP",
        "model_version": "gemini-1.5-pro",
        "temperature": 0.1,
        "error_code": None,
        "ocr_duration_ms": None,
        "embedding_duration_ms": 120,
        "retrieval_duration_ms": 85,
        "llm_duration_ms": 2100,
        "total_duration_ms": 2350,
        "created_at": datetime(2025, 1, 10, 9, 30, 0, tzinfo=timezone.utc),
    },

    # 2. Triage completion call — no RAG, temperature 0.0,
    #    full conversation history in prompt
    {
        "id": "f53ba1b3-78eb-4de2-aef3-76a51d6d1e8f",
        "session_id": session_id_2,
        "message_id": message_id_3,
        "report_id": None,      # triage has no report
        "call_type": "triage_completion",
        "assembled_prompt_enc": "AES256:enc:...triage_full_conversation_history...",
        "raw_response_enc": "AES256:enc:...triage_result_json...",
        "guardrail_trigger_text_enc": None,
        "error_message_enc": None,
        "guardrail_fired": False,
        "guardrail_check": None,
        "retrieved_chunk_ids": None,   # no RAG in triage
        "cosine_scores": None,
        "panel_coverage": None,
        "zone1_tokens": 450,
        "zone2_tokens": 0,      # no context/RAG
        "zone3_tokens": 1200,   # full conversation history
        "zone4_tokens": 0,
        "total_prompt_tokens": 1650,
        "completion_tokens": 180,
        "finish_reason": "STOP",
        "model_version": "gemini-1.5-pro",
        "temperature": 0.0,     # triage uses 0.0
        "error_code": None,
        "ocr_duration_ms": None,
        "embedding_duration_ms": None,
        "retrieval_duration_ms": None,
        "llm_duration_ms": 1800,
        "total_duration_ms": 1900,
        "created_at": datetime(2025, 2, 14, 11, 0, 0, tzinfo=timezone.utc),
    },

    # 3. Summary call — full checkup multi panel,
    #    cardiac urgency guardrail fired
    {
        "id": "787f8804-c5f8-41a6-9590-ce820b5f48f0",
        "session_id": session_id_3,
        "message_id": None,     # summary call has no message_id
        "report_id": report_id_2,
        "call_type": "summary",
        "assembled_prompt_enc": "AES256:enc:...full_checkup_summary_prompt...",
        "raw_response_enc": "AES256:enc:...full_checkup_summary_response...",
        "guardrail_trigger_text_enc": "AES256:enc:...cardiac_enzyme_text_that_triggered...",
        "error_message_enc": None,
        "guardrail_fired": True,
        "guardrail_check": "cardiac_urgency_override",
        "retrieved_chunk_ids": [
            "9e6893f2-734d-4ebf-bef4-7274420599ed", "a43ea41d-6ab9-4329-84ea-c0ba92c2df11",
            "91dd30d8-d15a-4cee-84d2-fd60a43bd21f", "733594f0-6725-4148-9bbe-f5cde896ee97",
        ],
        "cosine_scores": [0.95, 0.91, 0.89, 0.86, 0.82],
        "panel_coverage": {
            "CBC": 2,
            "Lipid Panel": 1,
            "Cardiac Enzymes": 2,
        },
        "zone1_tokens": 450,
        "zone2_tokens": 1200,   # multi panel chunks
        "zone3_tokens": 0,
        "zone4_tokens": 80,
        "total_prompt_tokens": 1730,
        "completion_tokens": 420,
        "finish_reason": "STOP",
        "model_version": "gemini-1.5-pro",
        "temperature": 0.1,
        "error_code": None,
        "ocr_duration_ms": 3200,
        "embedding_duration_ms": 250,
        "retrieval_duration_ms": 110,
        "llm_duration_ms": 3800,
        "total_duration_ms": 7400,
        "created_at": datetime(2025, 3, 1, 14, 0, 0, tzinfo=timezone.utc),
    },

    # 4. Embedding call — document upload pipeline,
    #    no LLM response, no guardrail
    {
        "id": "31bc7458-a2ca-4727-8eeb-138c49385c1e",
        "session_id": None,     # embedding call has no session
        "message_id": None,
        "report_id": report_id_1,
        "call_type": "embedding",
        "assembled_prompt_enc": "AES256:enc:...chunk_text_batch...",
        "raw_response_enc": None,   # no LLM response for embedding
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
        "total_prompt_tokens": 1200,  # total chunk tokens embedded
        "completion_tokens": 0,
        "finish_reason": "STOP",
        "model_version": "gemini-1.5-pro",
        "temperature": 0.0,
        "error_code": None,
        "ocr_duration_ms": 2800,
        "embedding_duration_ms": 340,
        "retrieval_duration_ms": None,
        "llm_duration_ms": 340,
        "total_duration_ms": 3200,
        "created_at": datetime(2025, 4, 5, 8, 0, 0, tzinfo=timezone.utc),
    },

    # 5. Chat call — Vertex AI error, call failed,
    #    raw_response NULL, error_code set
    {
        "id": "e705b6e0-cce0-467d-850f-62e77f14f8a4",
        "session_id": session_id_3,
        "message_id": message_id_2,
        "report_id": report_id_1,
        "call_type": "chat",
        "assembled_prompt_enc": "AES256:enc:...failed_call_prompt...",
        "raw_response_enc": None,   # NULL — call failed before response
        "guardrail_trigger_text_enc": None,
        "error_message_enc": "AES256:enc:...vertex_ai_503_error_message...",
        "guardrail_fired": False,
        "guardrail_check": None,
        "retrieved_chunk_ids": ["c8f71c85-7004-4355-bbcd-0ebd3c0ffc49","6c18ddea-3b54-49ee-9eb7-161f19c3692b"],
        "cosine_scores": [0.90, 0.87],
        "panel_coverage": {"CBC": 2},
        "zone1_tokens": 450,
        "zone2_tokens": 600,
        "zone3_tokens": 200,
        "zone4_tokens": 45,
        "total_prompt_tokens": 1295,
        "completion_tokens": 0,     # no completion — call failed
        "finish_reason": "ERROR",
        "model_version": "gemini-1.5-pro",
        "temperature": 0.1,
        "error_code": "VERTEX_AI_503",
        "ocr_duration_ms": None,
        "embedding_duration_ms": 115,
        "retrieval_duration_ms": 90,
        "llm_duration_ms": 5000,    # timeout
        "total_duration_ms": 5250,
        "created_at": datetime(2025, 4, 10, 10, 0, 0, tzinfo=timezone.utc),
    },
]

# Reference report_ids from dummy_reports
report_id_cbc = "9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6"          # CBC report
report_id_full_checkup = "df7b626b-0ea5-425a-940e-44fb037e88a6" # Full checkup report

dummy_lab_values = [
    # 1. CBC — Hemoglobin, normal range, Arabic test name
    {
        "id": "6bc2aeec-f662-4421-952d-e7a7d5e0522b",
        "report_id": report_id_cbc,
        "panel_name": "CBC",
        "test_category": "haematology",
        "test_name": "الهيموغلوبين",  # Arabic test name
        "value": Decimal("13.5"),
        "unit": "g/dL",
        "normal_range_low": Decimal("12.0"),
        "normal_range_high": Decimal("16.0"),
        "flag": "normal",
        "extracted_language": "ar",
    },

    # 2. CBC — White Blood Cell count, high flag
    {
        "id": "c84986df-4ea9-42c3-b504-3171f5f62826",
        "report_id": report_id_cbc,
        "panel_name": "CBC",
        "test_category": "haematology",
        "test_name": "White Blood Cell Count",
        "value": Decimal("11.8"),
        "unit": "10^3/uL",
        "normal_range_low": Decimal("4.5"),
        "normal_range_high": Decimal("11.0"),
        "flag": "high",
        "extracted_language": "en",
    },

    # 3. Cardiac Enzymes — Troponin I, critical flag
    #    triggers cardiac_urgency_flag on parent report
    {
        "id": "6a0fb206-1e05-4868-98f3-deefac50fe41",
        "report_id": report_id_full_checkup,
        "panel_name": "Cardiac Enzymes",
        "test_category": "cardiac_enzymes",  # triggers cardiac_urgency_flag
        "test_name": "Troponin I",
        "value": Decimal("2.85"),
        "unit": "ng/mL",
        "normal_range_low": Decimal("0.00"),
        "normal_range_high": Decimal("0.04"),
        "flag": "critical",              # critical + cardiac_enzymes = urgent flag
        "extracted_language": "en",
    },

    # 4. Lipid Panel — LDL Cholesterol, borderline high
    {
        "id": "0d5c8a1c-107f-422e-9b3c-e7f70bae0032",
        "report_id": report_id_full_checkup,
        "panel_name": "Lipid Panel",
        "test_category": "biochemistry",
        "test_name": "LDL Cholesterol",
        "value": Decimal("3.25"),
        "unit": "mmol/L",
        "normal_range_low": Decimal("0.00"),
        "normal_range_high": Decimal("3.00"),
        "flag": "borderline_high",
        "extracted_language": "en",
    },

    # 5. Thyroid — TSH, low flag, Arabic/English bilingual report
    {
        "id": "66e65c79-d66d-4ff0-9e6a-85e18821b1f3",
        "report_id": report_id_full_checkup,
        "panel_name": "TFTs",
        "test_category": "endocrinology",
        "test_name": "TSH",             # English name in bilingual report
        "value": Decimal("0.28"),
        "unit": "mIU/L",
        "normal_range_low": Decimal("0.40"),
        "normal_range_high": Decimal("4.00"),
        "flag": "low",
        "extracted_language": "en",
    },
]

fine_tuning_examples = [
    # 1. Document mode — CBC panel, English, clinician validated, export-ready
    {
        "id": "bb203870-4cfc-4afa-8220-16d49088a441",
        "source_session_id": "2bb77f2d-341f-44b2-aab2-d51f5643bf83",
        "source_message_id": "11e30dde-8ec7-4135-b55b-51a72149fcd5",
        "source_report_type": "cbc",
        "session_mode": "document",
        "system_prompt": "You are a medical AI assistant. Summarise lab results in plain language. Always end with a doctor consultation disclaimer. Never provide a diagnosis.",
        "report_context": "CBC Report — Male, 34. Hemoglobin: 9.2 g/dL (Low). WBC: 11.8 x10³/µL (High). Platelets: 145 x10³/µL (Normal).",
        "conversation_history": [
            {"role": "user", "content": "What does my blood test show?"},
            {"role": "assistant", "content": "Your report shows a lower than normal hemoglobin level and a slightly elevated white blood cell count. This may suggest anaemia alongside a possible infection or inflammation. Please discuss with your doctor."}
        ],
        "user_question": "Should I be worried about my hemoglobin being low?",
        "assistant_response": "A hemoglobin of 9.2 g/dL is below the normal range for adult males (13.5-17.5 g/dL), which indicates mild to moderate anaemia. This can cause fatigue and shortness of breath. Your doctor may investigate the underlying cause. Please discuss these results with your doctor for a full medical interpretation.",
        "triage_result_level": None,
        "interaction_language": "en",
        "question_category": "lab_explanation",
        "report_panel": "CBC",
        "age_range": "26-35",
        "gender": "male",
        "nationality": "SA",
        "document_quality": "high",
        "patient_rating": 5,
        "guardrail_triggered": False,
        "clinician_validated": True,
        "clinician_rating": 5,
        "auto_quality_score": Decimal("0.94"),
        "dataset_version": "v1.0",
        "included_in_export": True,
        "export_batch_id": "d0deeeb3-d784-4414-9a2f-70b1f5f8edce",
        "phi_scan_passed": True,
        "phi_scan_at": now,
        "created_at": now,
    },

    # 2. Triage mode — Arabic, yellow result, not yet clinician validated
    {
        "id": "8b52fb50-b50a-4909-ab70-6f436abce437",
        "source_session_id": "2bc992f8-0c97-4e51-9f20-1da1d2918af4",
        "source_message_id": "9c4cda96-5969-4841-b4fa-521b2149f46e",
        "source_report_type": "none",
        "session_mode": "triage",
        "system_prompt": "أنت مساعد طبي ذكاء اصطناعي. اطرح أسئلة منظمة حول الأعراض. لا تقدم تشخيصاً طبياً أبداً.",
        "report_context": None,
        "conversation_history": [
            {"role": "user", "content": "أعاني من صداع شديد منذ يومين مع غثيان"},
            {"role": "assistant", "content": "هل الصداع في منطقة معينة من الرأس؟ وهل تعاني من حساسية للضوء أو الصوت؟"},
            {"role": "user", "content": "نعم، في الجانب الأيسر فقط، ونعم أشعر بحساسية من الضوء"},
        ],
        "user_question": "ما الذي يسبب هذا الصداع؟",
        "assistant_response": "بناءً على ما وصفته — صداع شديد في جانب واحد مع غثيان وحساسية للضوء — قد تكون هذه أعراض الشقيقة (الصداع النصفي). يُنصح بمراجعة الطبيب لتقييم حالتك. يُرجى مناقشة هذه الأعراض مع طبيبك للحصول على تفسير طبي كامل.",
        "triage_result_level": "yellow",
        "interaction_language": "ar",
        "question_category": "symptom_triage",
        "report_panel": None,
        "age_range": "26-35",
        "gender": "female",
        "nationality": "SA",
        "document_quality": None,
        "patient_rating": 4,
        "guardrail_triggered": False,
        "clinician_validated": False,
        "clinician_rating": None,
        "auto_quality_score": Decimal("0.81"),
        "dataset_version": "v1.0",
        "included_in_export": False,
        "export_batch_id": None,
        "phi_scan_passed": True,
        "phi_scan_at": now,
        "created_at": now,
    },

    # 3. Document mode — full_checkup, bilingual (mixed), multi-panel, HbA1c panel query
    {
        "id": "b491fbf4-5834-421e-ac53-9f8267d8c385",
        "source_session_id": "83e61dc6-09ff-4a51-b897-c11b18fa1c72",
        "source_message_id": "d495e711-1374-4d32-b4f9-a992d894c31a",
        "source_report_type": "full_checkup",
        "session_mode": "document",
        "system_prompt": "You are a medical AI assistant. Respond in the same language as the patient's question. Summarise lab results by panel. Never provide a diagnosis.",
        "report_context": "HbA1c Panel — HbA1c: 8.1% (High, ref: 4.0-5.6%). Fasting Glucose: 9.4 mmol/L (High, ref: 3.9-5.6 mmol/L). Lipid Panel — Total Cholesterol: 5.9 mmol/L (Borderline High).",
        "conversation_history": [
            {"role": "user", "content": "ما معنى HbA1c 8.1؟"},
            {"role": "assistant", "content": "مستوى HbA1c 8.1% أعلى من المعدل الطبيعي (4.0-5.6%). يعكس هذا المستوى متوسط سكر الدم خلال الأشهر الثلاثة الماضية. يُرجى مناقشة النتيجة مع طبيبك."},
        ],
        "user_question": "Is my diabetes under control based on this result?",
        "assistant_response": "An HbA1c of 8.1% suggests that blood sugar levels have been above the target range over the past three months. For most adults with diabetes, the target is below 7.0%. This does not mean your condition cannot be managed — your doctor can review your treatment plan. Please discuss these results with your doctor for a full medical interpretation.",
        "triage_result_level": None,
        "interaction_language": "mixed",
        "question_category": "panel_specific_query",
        "report_panel": "HbA1c",
        "age_range": "46-55",
        "gender": "male",
        "nationality": "AE",
        "document_quality": "high",
        "patient_rating": 4,
        "guardrail_triggered": False,
        "clinician_validated": True,
        "clinician_rating": 4,
        "auto_quality_score": Decimal("0.88"),
        "dataset_version": "v1.0",
        "included_in_export": True,
        "export_batch_id": "a6545cc6-558c-4e1b-b440-88747762f065",
        "phi_scan_passed": True,
        "phi_scan_at": now,
        "created_at": now,
    },

    # 4. General mode — no document, English, medication query, guardrail NOT triggered
    {
        "id": "f0772c32-db7c-42f3-b27a-11a405651e7d",
        "source_session_id": "1dfd99cc-6fb2-4e0f-b9db-d95c7f23f1df",
        "source_message_id": "23ce8229-33b0-4c4c-bb10-6dc7115c5591",
        "source_report_type": "none",
        "session_mode": "general",
        "system_prompt": "You are a medical AI assistant. Answer general health questions with caution. Never prescribe medication or provide a diagnosis.",
        "report_context": None,
        "conversation_history": [],
        "user_question": "What is metformin usually prescribed for?",
        "assistant_response": "Metformin is a medication commonly used to manage type 2 diabetes. It works by reducing glucose production in the liver and improving insulin sensitivity. It is typically prescribed alongside lifestyle changes such as diet and exercise. Only a doctor can determine whether metformin is appropriate for your situation. Please discuss this with your doctor for a full medical interpretation.",
        "triage_result_level": None,
        "interaction_language": "en",
        "question_category": "medication_query",
        "report_panel": None,
        "age_range": "36-45",
        "gender": "female",
        "nationality": "SA",
        "document_quality": None,
        "patient_rating": 5,
        "guardrail_triggered": False,
        "clinician_validated": True,
        "clinician_rating": 5,
        "auto_quality_score": Decimal("0.92"),
        "dataset_version": "v1.0",
        "included_in_export": True,
        "export_batch_id": "50ca0ac5-a6ad-45a4-b399-3283be98d329",
        "phi_scan_passed": True,
        "phi_scan_at": now,
        "created_at": now,
    },

    # 5. Document mode — Lipid Panel, medium quality scan, phi_scan not yet run, not export-ready
    {
        "id": "2105a5af-01c1-471f-a6fb-da9f54dca4a3",
        "source_session_id": "383dee92-b6cb-4937-a826-776091f7e973",
        "source_message_id": "1d7176b7-d254-4e98-aa3f-b698a01fbebb",
        "source_report_type": "lipid_panel",
        "session_mode": "document",
        "system_prompt": "You are a medical AI assistant. Summarise lab results in plain language. Always end with a doctor consultation disclaimer. Never provide a diagnosis.",
        "report_context": "Lipid Panel — Total Cholesterol: 6.4 mmol/L (High). LDL: 4.2 mmol/L (High). HDL: 0.9 mmol/L (Low). Triglycerides: 2.8 mmol/L (Borderline High).",
        "conversation_history": [
            {"role": "user", "content": "Are my cholesterol levels dangerous?"},
            {"role": "assistant", "content": "Your total cholesterol and LDL are above the recommended range, and your HDL (the protective cholesterol) is lower than ideal. Together these may increase cardiovascular risk. Please discuss with your doctor."},
        ],
        "user_question": "What lifestyle changes can help lower LDL?",
        "assistant_response": "Common approaches to lowering LDL include reducing saturated fat intake, increasing soluble fibre, engaging in regular aerobic exercise, and maintaining a healthy weight. However, the right plan depends on your overall health picture. Please discuss these results with your doctor for a full medical interpretation.",
        "triage_result_level": None,
        "interaction_language": "en",
        "question_category": "lab_explanation",
        "report_panel": "Lipid Panel",
        "age_range": "56-65",
        "gender": "male",
        "nationality": "SA",
        "document_quality": "medium",
        "patient_rating": None,       # Not yet rated
        "guardrail_triggered": False,
        "clinician_validated": False,
        "clinician_rating": None,
        "auto_quality_score": Decimal("0.74"),  # Below 0.85 threshold — needs clinician validation before export
        "dataset_version": "v1.0",
        "included_in_export": False,
        "export_batch_id": None,
        "phi_scan_passed": False,     # PHI scan not yet run — nightly job pending
        "phi_scan_at": None,
        "created_at": now,
    },
]




# Assume these user_ids are pre-seeded in the USERS table
user_id_1 = "604c02aa-b8f3-4c9c-b500-40bd75eec8c1"  
user_id_2 = "043262a7-c7c5-4db0-bd64-77a664535f5c"  


extension_hooks = [
    # 1. Telemedicine integration — active, user has a linked provider and preferred time slot
    {
        "id": "9f440c59-a3a0-4863-8901-b72b1dd63966",
        "user_id": user_id_1,
        "hook_name": "telemedicine_enabled",
        "hook_value": {
            "provider": "seha",                        # Telemedicine provider slug
            "provider_display_name": "Seha Virtual Care",
            "redirect_url": "https://seha.ae/consult",
            "preferred_language": "ar",
            "preferred_slot": "morning",               # morning | afternoon | evening
            "auto_escalate_red_triage": True           # Auto-book on red triage result
        },
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    },

    # 2. WhatsApp follow-up — active, sends check-in 48hr after yellow/red triage
    {
        "id": "c428536d-bf9f-47d3-8ad7-5254eac86ed7",
        "user_id": user_id_1,
        "hook_name": "whatsapp_followup_enabled",
        "hook_value": {
            "whatsapp_number": "+966500000000",        # Stored hashed in production — plain here for seed only
            "followup_delay_hours": 48,
            "trigger_on": ["yellow", "red"],           # Triage result levels that trigger the message
            "message_language": "ar",
            "opt_out_token": "abc123xyz"               # Single-use opt-out link token
        },
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    },

    # 3. Payment gateway — configured but NOT yet active (pending billing setup)
    {
        "id": "4a16e77d-3142-4f7f-83eb-c3ac9043ba2c",
        "user_id": user_id_2,
        "hook_name": "payment_gateway_url",
        "hook_value": {
            "gateway": "moyasar",
            "gateway_display_name": "Moyasar",
            "publishable_key": "pk_test_placeholder",  # Test key — replace before activation
            "currency": "SAR",
            "billable_features": ["triage_session", "document_upload"],
            "free_tier_limit": {
                "triage_sessions": 1,
                "document_uploads": 0
            }
        },
        "is_active": False,                            # Configured but inactive — pending CTO activation sign-off
        "created_at": now,
        "updated_at": now,
    },

    # 4. Physician escalation webhook — fires when a red triage result is generated
    {
        "id": "af4c055c-9f0c-4d16-b46e-04e7e58350af",
        "user_id": user_id_2,
        "hook_name": "physician_escalation_webhook",
        "hook_value": {
            "webhook_url": "https://internal.clinic-system.sa/api/escalate",
            "auth_header": "X-Webhook-Secret",
            "secret_ref": "projects/med-ai/secrets/clinic_webhook_secret/versions/latest",  # Secret Manager ref
            "trigger_on": ["red"],
            "include_fields": ["session_id", "urgency_score", "symptoms_reported", "result_summary"],
            "timeout_seconds": 10,
            "retry_attempts": 3
        },
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    },

    # 5. Pub/Sub migration flag — signals event_dispatcher to route events to Pub/Sub instead of in-process handlers
   
]




# Pre-seeded report_ids matching existing REPORTS rows
report_id_cbc = "9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6"
report_id_full_checkup ="df7b626b-0ea5-425a-940e-44fb037e88a6"

def fake_vector(seed: int) -> list[float]:
    """Generates a reproducible fake 768-dim unit-ish vector for seeding."""
    random.seed(seed)
    return [round(random.uniform(-0.05, 0.05), 6) for _ in range(768)]

embeddings = [
    # 1. CBC single-panel report — only one panel, chunk 0 (opening reference ranges block)
    {
        "id":"06338c08-664f-48e8-98c1-40b86f2b5289",
        "report_id": report_id_cbc,
        "chunk_text_enc": "enc::CBC_CHUNK_0::Hemoglobin 9.2 g/dL [Low]. WBC 11.8 x10³/µL [High]. Platelets 145 x10³/µL [Normal]. Reference ranges: Hb 13.5-17.5, WBC 4.5-11.0, Plt 150-400.",
        "embedding_vector": fake_vector(seed=1),
        "chunk_index": 0,
        "section_name": "CBC",
        "token_count": 387,
    },

    # 2. CBC single-panel report — chunk 1 (continuation: differential counts block)
    {
        "id":"6973200b-002c-4c30-9f28-35e9ec523ba8",
        "report_id": report_id_cbc,
        "chunk_text_enc": "enc::CBC_CHUNK_1::Neutrophils 78% [High, ref 40-70%]. Lymphocytes 15% [Low, ref 20-40%]. Monocytes 5% [Normal]. Eosinophils 1% [Normal]. Basophils 1% [Normal].",
        "embedding_vector": fake_vector(seed=2),
        "chunk_index": 1,
        "section_name": "CBC",
        "token_count": 312,
    },

    # 3. Full checkup — CBC panel chunk (multi-panel report, round-robin coverage starts here)
    {
        "id": "0c8c5151-425a-40af-acd0-d64de0040b02",
        "report_id": report_id_full_checkup,
        "chunk_text_enc": "enc::FULL_CHECKUP_CBC::CBC Panel. Hemoglobin: 11.4 g/dL [Low]. MCV: 72 fL [Low, ref 80-100]. MCH: 24 pg [Low, ref 27-33]. Ferritin: 8 µg/L [Low, ref 12-300]. Consistent with microcytic anaemia pattern.",
        "embedding_vector": fake_vector(seed=3),
        "chunk_index": 0,
        "section_name": "CBC",
        "token_count": 401,
    },

    # 4. Full checkup — Lipid Panel chunk (different section_name, same report — enables round-robin retrieval)
    {
        "id": "c09b7307-16ab-4166-b48a-8ecc75018c98",
        "report_id": report_id_full_checkup,
        "chunk_text_enc": "enc::FULL_CHECKUP_LIPID::Lipid Panel. Total Cholesterol: 6.4 mmol/L [High, ref <5.2]. LDL: 4.2 mmol/L [High, ref <3.4]. HDL: 0.9 mmol/L [Low, ref >1.0]. Triglycerides: 2.8 mmol/L [Borderline High, ref <1.7]. Non-HDL Cholesterol: 5.5 mmol/L [High].",
        "embedding_vector": fake_vector(seed=4),
        "chunk_index": 1,
        "section_name": "Lipid Panel",
        "token_count": 398,
    },

    # 5. Full checkup — TFTs chunk (third distinct panel, short panel padded with metadata context per spec)
    {
        "id": "6019a9cb-cb2a-4ad6-aa27-676c11bc2ab2",
        "report_id": report_id_full_checkup,
        "chunk_text_enc": "enc::FULL_CHECKUP_TFT::Thyroid Function Panel. TSH: 0.28 mIU/L [Low, ref 0.40-4.00]. Free T4: 18.2 pmol/L [Normal, ref 12.0-22.0]. Free T3: 5.1 pmol/L [Normal, ref 3.1-6.8]. [Section context: Thyroid Function Panel — single-page section, MENA population ref ranges applied.]",
        "embedding_vector": fake_vector(seed=5),
        "chunk_index": 2,
        "section_name": "TFTs",
        "token_count": 318,  # Short panel — under 400 tokens, padded with section metadata per chunking spec
    },
]

now = datetime.now(timezone.utc)

# Pre-seeded IDs matching existing CHAT_MESSAGES and USERS (role=doctor) rows
message_id_1 = "28fd1664-1c46-4353-9b38-e14291ab4f59"
message_id_2 = "636a35a4-7548-4720-afe7-6590b9524eff"
message_id_3 = "caf6858e-f52b-4371-a31a-00b8112698d1"


doctor_id_1 = "ff4975b9-2b05-4625-b9bc-e614af62e323"  # Senior physician reviewer

clinician_reviews = [
    # 1. Excellent response — high scores across all dimensions, safe to train on
    {
        "id": "adef58c6-7a61-4cf1-8f95-91791699efaa",
        "message_id": message_id_1,
        "reviewer_id": doctor_id_1,
        "accuracy_rating": 5,
        "safety_rating": 5,
        "completeness_rating": 5,
        "contains_error": False,
        "error_description": None,
        "suggested_correction": None,
        "is_safe_to_train_on": True,
        "reviewed_at": now,
        "review_duration_sec": 142,         # Thorough review — well above 30s threshold
    },

    # 2. Acceptable response with minor completeness gap — safe to train on, no error
    {
        "id": "45177fee-fdf2-433d-988c-2f1c8e7d71c2",
        "message_id": message_id_2,
        "reviewer_id": doctor_id_1,
        "accuracy_rating": 4,
        "safety_rating": 5,
        "completeness_rating": 3,           # Missing mention of fasting requirement for lipid retest
        "contains_error": False,
        "error_description": None,
        "suggested_correction": "Response should mention that a fasting lipid retest is typically required before clinical decisions are made on borderline results.",
        "is_safe_to_train_on": True,        # Safe despite gap — correction logged for prompt tuning
        "reviewed_at": now,
        "review_duration_sec": 98,
    },

    # 3. Factual error detected — wrong HbA1c target cited, NOT safe to train on
    {
        "id":"96c670b8-1a3a-4c3a-9929-1ac1b378f9ea",
        "message_id": message_id_3,
        "reviewer_id": doctor_id_1,
        "accuracy_rating": 2,
        "safety_rating": 3,
        "completeness_rating": 3,
        "contains_error": True,
        "error_description": "The response stated the HbA1c target for diabetic patients is below 6.0%. The correct general target for most adults with type 2 diabetes is below 7.0% (ADA guideline). Citing 6.0% could cause unnecessary patient anxiety.",
        "suggested_correction": "Replace '6.0%' with '7.0%' and note that individual targets vary — some patients may have a higher target set by their doctor depending on age and comorbidities.",
        "is_safe_to_train_on": False,       # Factual error disqualifies from training pipeline
        "reviewed_at": now,
        "review_duration_sec": 187,         # Long review — clinician cross-referenced guidelines
    },

    # 4. Unsafe response — AI response implied a likely diagnosis, safety guardrail should have caught this
    
    # 5. Rushed review — flagged for quality, is_safe_to_train_on left False pending re-review
    
]






now = datetime.now(timezone.utc)

# Pre-seeded IDs matching existing USERS and REPORTS rows
user_id_1 = "604c02aa-b8f3-4c9c-b500-40bd75eec8c1"  
user_id_2 = "043262a7-c7c5-4db0-bd64-77a664535f5c"  
report_id_cbc = "9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6"
report_id_full_checkup ="df7b626b-0ea5-425a-940e-44fb037e88a6"

chat_sessions = [
    # 1. Document mode — registered user, CBC report, Arabic, active session
    {
        "id": "4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae",
        "user_id": user_id_1,
        "report_id": report_id_cbc,
        "mode": "document",
        "title": "تحليل CBC - يناير 2025",           # Auto-generated from first user message, truncated to 60 chars
        "language": "ar",
        "is_guest": False,
        "guest_token": None,
        "triage_status": None,                        # Not a triage session — triage fields all NULL
        "triage_result": None,
        "triage_completed_at": None,
        "created_at": now,
        "last_message_at": now,
    },

    # 2. Triage mode — registered user, completed yellow result, English
    {
        "id": "e2385da2-08c4-4b7e-af76-97b947567d09",
        "user_id": user_id_2,
        "report_id": None,                            # Triage mode never has a report_id
        "mode": "triage",
        "title": "Symptom check — headache and nausea",
        "language": "en",
        "is_guest": False,
        "guest_token": None,
        "triage_status": "completed",
        "triage_result": "yellow",
        "triage_completed_at": now,
        "created_at": now,
        "last_message_at": now,
    },

    # 3. Guest triage session — first free session, Arabic, in progress
    {
        "id": "92b927dc-115b-41a1-a0aa-0abf81528e5c",
        "user_id": None,                              # NULL — guest session, no account
        "report_id": None,
        "mode": "triage",
        "title": None,                                # NULL — title only set after first message completes
        "language": "ar",
        "is_guest": True,
        "guest_token": f"guest:{"bb2dc801-b094-471d-85f0-4733956925df"}",       # Bearer guest:{uuid} format per auth spec
        "triage_status": "in_progress",
        "triage_result": None,                        # Not yet completed
        "triage_completed_at": None,
        "created_at": now,
        "last_message_at": now,
    },

    # 4. Document mode — full checkup report, English, abandoned mid-session (report deleted — report_id SET NULL)
    {
        "id": "7f9950a5-8f1d-4c79-967e-e356355deac0",
        "user_id": user_id_2,
        "report_id": None,                            # SET NULL — parent report was deleted by user (PDPL erasure)
        "mode": "document",
        "title": "Full checkup review — March 2025",
        "language": "en",
        "is_guest": False,
        "guest_token": None,
        "triage_status": None,
        "triage_result": None,
        "triage_completed_at": None,
        "created_at": now,
        "last_message_at": now,
    },

    # 5. General mode — registered user, no report, completed red triage escalation follow-up chat
    {
        "id": "e794391b-accd-4d36-915a-6140c93daffe",
        "user_id": user_id_1,
        "report_id": None,                            # General mode — no document context
        "mode": "general",
        "title": "سؤال عن أدوية ضغط الدم",            # "Question about blood pressure medication"
        "language": "ar",
        "is_guest": False,
        "guest_token": None,
        "triage_status": None,                        # General mode — triage fields NULL
        "triage_result": None,
        "triage_completed_at": None,
        "created_at": now,
        "last_message_at": now,
    },
]



# Reference session_ids from previous dummy data
session_id_1 = "4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae"  # document mode session
session_id_2 = "e2385da2-08c4-4b7e-af76-97b947567d09"  # triage mode session

dummy_chat_messages = [
    # 1. User message — document mode, Arabic question about CBC
    {
        "id": "28fd1664-1c46-4353-9b38-e14291ab4f59",
        "session_id": session_id_1,
        "role": "user",
        "content_enc": "AES256:enc:...ما معنى ارتفاع خلايا الدم البيضاء؟...",
        "retrieved_chunk_ids": None,    # user messages have no chunks
        "finish_reason": None,          # only assistant messages have finish_reason
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "patient_rating": None,
        "patient_rating_at": None,
        "user_feedback_flag": None,
        "guardrail_triggered": False,
        "guardrail_reason": None,
        "fallback_used": False,
        "response_language": None,      # user message has no response language
        "question_language": "ar",
        "question_category": "lab_explanation",
        "ft_eligible": None,            # computed nightly
        "ft_excluded_reason": None,
        "created_at": datetime(2025, 1, 10, 9, 30, 0, tzinfo=timezone.utc),
    },

    # 2. Assistant message — document mode, Arabic response,
    #    RAG chunks used, patient rated 5 stars
    {
        "id": "636a35a4-7548-4720-afe7-6590b9524eff",
        "session_id": session_id_1,
        "role": "assistant",
        "content_enc": "AES256:enc:...ارتفاع خلايا الدم البيضاء يشير إلى...",
        "retrieved_chunk_ids": ["a29bc5a5-af1b-469e-941a-22931f49a8df", "c71f80c8-8731-4cc1-a9e0-81ec478ff795", "63e32535-308f-4046-a138-75873da8677a"],
        "finish_reason": "STOP",
        "prompt_tokens": 1600,
        "completion_tokens": 320,
        "patient_rating": 5,
        "patient_rating_at": datetime(2025, 1, 10, 9, 32, 0, tzinfo=timezone.utc),
        "user_feedback_flag": "helpful",
        "guardrail_triggered": False,
        "guardrail_reason": None,
        "fallback_used": False,
        "response_language": "ar",
        "question_language": "ar",
        "question_category": "lab_explanation",
        "ft_eligible": True,            # high rating, no guardrail
        "ft_excluded_reason": None,
        "created_at": datetime(2025, 1, 10, 9, 31, 0, tzinfo=timezone.utc),
    },

    # 3. Assistant message — guardrail fired,
    #    cardiac urgency override, fallback used


    # 4. Triage mode — user message describing symptoms
    {
        "id": "caf6858e-f52b-4371-a31a-00b8112698d1",
        "session_id": session_id_2,
        "role": "user",
        "content_enc": "AES256:enc:...I have chest pain and shortness of breath...",
        "retrieved_chunk_ids": None,    # triage has no RAG
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
        "ft_eligible": None,            # computed nightly
        "ft_excluded_reason": None,
        "created_at": datetime(2025, 2, 14, 11, 0, 0, tzinfo=timezone.utc),
    },

    # 5. Assistant message — wrong flag from patient,
    #    low rating, ft excluded
    {
        "id": "45d2de49-527e-430c-852e-7adcdcea2e3f",
        "session_id": session_id_1,
        "role": "assistant",
        "content_enc": "AES256:enc:...your HbA1c level suggests...",
        "retrieved_chunk_ids": ["a709a7e2-c00f-46a3-b726-d81f5fa6b63f", "8afd8739-bb4b-4cf3-82ba-71cfd36c48d1"],
        "finish_reason": "STOP",
        "prompt_tokens": 1400,
        "completion_tokens": 280,
        "patient_rating": 2,            # low rating
        "patient_rating_at": datetime(2025, 4, 10, 10, 5, 0, tzinfo=timezone.utc),
        "user_feedback_flag": "wrong",  # patient flagged as wrong
        "guardrail_triggered": False,
        "guardrail_reason": None,
        "fallback_used": False,
        "response_language": "en",
        "question_language": "en",
        "question_category": "lab_explanation",
        "ft_eligible": False,           # low rating = not eligible
        "ft_excluded_reason": "patient_rating_below_threshold",
        "created_at": datetime(2025, 4, 10, 10, 4, 0, tzinfo=timezone.utc),
    },
]

print("1 users --------")
print(dummy_users)
print("2 guest --------")
print(dummy_guest_sessions)
print("3 chat message--------")
print(dummy_chat_messages)
print("4 chat_sessions --------")
print(chat_sessions)
print("5 reports --------")
print(dummy_reports)
print("6 demo --------")
print(dummy_patient_demographics)
print("7 triage --------")
print(dummy_triage_results)
print("8 llm --------")
print(dummy_llm_traces)
print("9 lab --------")
print(dummy_lab_values)
print("10 tuning --------")
print(fine_tuning_examples)
print("11 extension --------")
print(extension_hooks)
print("12 clicnical --------")
print(clinician_reviews)




# final format


# 1 users --------
[
    {
        "id": "604c02aa-b8f3-4c9c-b500-40bd75eec8c1",
        "name": "Ahmed Al-Rashidi",
        "email_enc": "AES256:enc:ahmed.alrashidi@gmail.com",
        "phone_enc": "AES256:enc:+966501234567",
        "dob_enc": "AES256:enc:1990-05-15",
        "preferred_language": "ar",
        "role": "patient",
        "firebase_uid": "firebase_uid_001",
        "created_at": datetime.datetime(2025, 1, 10, 8, 0),
        "consent_given_at": datetime.datetime(2025, 1, 10, 8, 5),
        "research_consent": True,
        "triage_count": 2,
    },
    {
        "id": "043262a7-c7c5-4db0-bd64-77a664535f5c",
        "name": "Sarah Mitchell",
        "email_enc": "AES256:enc:sarah.mitchell@gmail.com",
        "phone_enc": "AES256:enc:+971501234567",
        "dob_enc": "AES256:enc:1985-09-22",
        "preferred_language": "en",
        "role": "patient",
        "firebase_uid": "firebase_uid_002",
        "created_at": datetime.datetime(2025, 2, 14, 10, 30),
        "consent_given_at": datetime.datetime(2025, 2, 14, 10, 35),
        "research_consent": False,
        "triage_count": 1,
    },
    {
        "id": "ff4975b9-2b05-4625-b9bc-e614af62e323",
        "name": "Dr. Khalid Al-Otaibi",
        "email_enc": "AES256:enc:khalid.otaibi@hospital.sa",
        "phone_enc": "AES256:enc:+966509876543",
        "dob_enc": None,
        "preferred_language": "ar",
        "role": "doctor",
        "firebase_uid": "firebase_uid_003",
        "created_at": datetime.datetime(2025, 1, 5, 9, 0),
        "consent_given_at": datetime.datetime(2025, 1, 5, 9, 10),
        "research_consent": True,
        "triage_count": 0,
    },
    {
        "id": "677f7b41-19fc-4d5f-8d4f-d65c716dfcae",
        "name": "Fatima Al-Zahra",
        "email_enc": "AES256:enc:fatima.zahra@gmail.com",
        "phone_enc": None,
        "dob_enc": None,
        "preferred_language": "ar",
        "role": "patient",
        "firebase_uid": "firebase_uid_004",
        "created_at": datetime.datetime(2025, 3, 1, 14, 0),
        "consent_given_at": None,
        "research_consent": False,
        "triage_count": 0,
    },
    {
        "id": "9c4ed973-c0a2-4eab-9cd3-93b3ca8d8828",
        "name": "Admin User",
        "email_enc": "AES256:enc:admin@platform.com",
        "phone_enc": None,
        "dob_enc": None,
        "preferred_language": "en",
        "role": "admin",
        "firebase_uid": "firebase_uid_005",
        "created_at": datetime.datetime(2025, 1, 1, 0, 0),
        "consent_given_at": datetime.datetime(2025, 1, 1, 0, 1),
        "research_consent": False,
        "triage_count": 0,
    },
]
# 2 guest --------
[
    {
        "id": "5f43455a-cffb-486f-9977-81d58a060fb6",
        "guest_token": "guest_token_001",
        "tos_accepted": True,
        "tos_accepted_at": datetime.datetime(
            2025, 1, 10, 8, 0, tzinfo=datetime.timezone.utc
        ),
        "research_consent": False,
        "age_range": "26-35",
        "gender": "male",
        "nationality": "SA",
        "claimed_user_id": None,
        "created_at": datetime.datetime(
            2025, 1, 10, 8, 0, tzinfo=datetime.timezone.utc
        ),
        "triage_count": 0,
        "expires_at": datetime.datetime(
            2025, 1, 11, 8, 0, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "7063a7d8-947b-4320-bc1f-24006d8c327f",
        "guest_token": "guest_token_002",
        "tos_accepted": True,
        "tos_accepted_at": datetime.datetime(
            2025, 2, 14, 10, 0, tzinfo=datetime.timezone.utc
        ),
        "research_consent": True,
        "age_range": "36-45",
        "gender": "female",
        "nationality": "AE",
        "claimed_user_id": None,
        "created_at": datetime.datetime(
            2025, 2, 14, 10, 0, tzinfo=datetime.timezone.utc
        ),
        "triage_count": 1,
        "expires_at": datetime.datetime(
            2025, 2, 15, 10, 0, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "6a89299e-4554-4451-9bad-105506e0339c",
        "guest_token": "guest_token_003",
        "tos_accepted": True,
        "tos_accepted_at": datetime.datetime(
            2025, 3, 1, 9, 0, tzinfo=datetime.timezone.utc
        ),
        "research_consent": True,
        "age_range": "18-25",
        "gender": "female",
        "nationality": "SA",
        "claimed_user_id": "043262a7-c7c5-4db0-bd64-77a664535f5c",
        "created_at": datetime.datetime(2025, 3, 1, 9, 0, tzinfo=datetime.timezone.utc),
        "triage_count": 1,
        "expires_at": datetime.datetime(2025, 3, 2, 9, 0, tzinfo=datetime.timezone.utc),
    },
    {
        "id": "b8d540e6-a340-4e8d-8345-5d25f63104a6",
        "guest_token": "guest_token_004",
        "tos_accepted": True,
        "tos_accepted_at": datetime.datetime(
            2025, 1, 1, 6, 0, tzinfo=datetime.timezone.utc
        ),
        "research_consent": False,
        "age_range": "46-55",
        "gender": "male",
        "nationality": "KW",
        "claimed_user_id": None,
        "created_at": datetime.datetime(2025, 1, 1, 6, 0, tzinfo=datetime.timezone.utc),
        "triage_count": 0,
        "expires_at": datetime.datetime(2025, 1, 2, 6, 0, tzinfo=datetime.timezone.utc),
    },
    {
        "id": "946f7183-7da6-4ba6-8281-6566fcdfe8ab",
        "guest_token": "guest_token_005",
        "tos_accepted": False,
        "tos_accepted_at": None,
        "research_consent": False,
        "age_range": "56-65",
        "gender": "prefer_not_to_say",
        "nationality": None,
        "claimed_user_id": None,
        "created_at": datetime.datetime(
            2025, 4, 10, 12, 0, tzinfo=datetime.timezone.utc
        ),
        "triage_count": 0,
        "expires_at": datetime.datetime(
            2025, 4, 11, 12, 0, tzinfo=datetime.timezone.utc
        ),
    },
]
# 3 chat message--------
[
    {
        "id": "28fd1664-1c46-4353-9b38-e14291ab4f59",
        "session_id": "4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae",
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
        "created_at": datetime.datetime(
            2025, 1, 10, 9, 30, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "636a35a4-7548-4720-afe7-6590b9524eff",
        "session_id": "4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae",
        "role": "assistant",
        "content_enc": "AES256:enc:...ارتفاع خلايا الدم البيضاء يشير إلى...",
        "retrieved_chunk_ids": [
            "a29bc5a5-af1b-469e-941a-22931f49a8df",
            "c71f80c8-8731-4cc1-a9e0-81ec478ff795",
            "63e32535-308f-4046-a138-75873da8677a",
        ],
        "finish_reason": "STOP",
        "prompt_tokens": 1600,
        "completion_tokens": 320,
        "patient_rating": 5,
        "patient_rating_at": datetime.datetime(
            2025, 1, 10, 9, 32, tzinfo=datetime.timezone.utc
        ),
        "user_feedback_flag": "helpful",
        "guardrail_triggered": False,
        "guardrail_reason": None,
        "fallback_used": False,
        "response_language": "ar",
        "question_language": "ar",
        "question_category": "lab_explanation",
        "ft_eligible": True,
        "ft_excluded_reason": None,
        "created_at": datetime.datetime(
            2025, 1, 10, 9, 31, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "caf6858e-f52b-4371-a31a-00b8112698d1",
        "session_id": "e2385da2-08c4-4b7e-af76-97b947567d09",
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
        "created_at": datetime.datetime(
            2025, 2, 14, 11, 0, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "45d2de49-527e-430c-852e-7adcdcea2e3f",
        "session_id": "4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae",
        "role": "assistant",
        "content_enc": "AES256:enc:...your HbA1c level suggests...",
        "retrieved_chunk_ids": [
            "a709a7e2-c00f-46a3-b726-d81f5fa6b63f",
            "8afd8739-bb4b-4cf3-82ba-71cfd36c48d1",
        ],
        "finish_reason": "STOP",
        "prompt_tokens": 1400,
        "completion_tokens": 280,
        "patient_rating": 2,
        "patient_rating_at": datetime.datetime(
            2025, 4, 10, 10, 5, tzinfo=datetime.timezone.utc
        ),
        "user_feedback_flag": "wrong",
        "guardrail_triggered": False,
        "guardrail_reason": None,
        "fallback_used": False,
        "response_language": "en",
        "question_language": "en",
        "question_category": "lab_explanation",
        "ft_eligible": False,
        "ft_excluded_reason": "patient_rating_below_threshold",
        "created_at": datetime.datetime(
            2025, 4, 10, 10, 4, tzinfo=datetime.timezone.utc
        ),
    },
]
# 4 chat_sessions --------
[
    {
        "id": "4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae",
        "user_id": "604c02aa-b8f3-4c9c-b500-40bd75eec8c1",
        "report_id": "9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6",
        "mode": "document",
        "title": "تحليل CBC - يناير 2025",
        "language": "ar",
        "is_guest": False,
        "guest_token": None,
        "triage_status": None,
        "triage_result": None,
        "triage_completed_at": None,
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557722, tzinfo=datetime.timezone.utc
        ),
        "last_message_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557722, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "e2385da2-08c4-4b7e-af76-97b947567d09",
        "user_id": "043262a7-c7c5-4db0-bd64-77a664535f5c",
        "report_id": None,
        "mode": "triage",
        "title": "Symptom check — headache and nausea",
        "language": "en",
        "is_guest": False,
        "guest_token": None,
        "triage_status": "completed",
        "triage_result": "yellow",
        "triage_completed_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557722, tzinfo=datetime.timezone.utc
        ),
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557722, tzinfo=datetime.timezone.utc
        ),
        "last_message_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557722, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "92b927dc-115b-41a1-a0aa-0abf81528e5c",
        "user_id": None,
        "report_id": None,
        "mode": "triage",
        "title": None,
        "language": "ar",
        "is_guest": True,
        "guest_token": "guest:bb2dc801-b094-471d-85f0-4733956925df",
        "triage_status": "in_progress",
        "triage_result": None,
        "triage_completed_at": None,
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557722, tzinfo=datetime.timezone.utc
        ),
        "last_message_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557722, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "7f9950a5-8f1d-4c79-967e-e356355deac0",
        "user_id": "043262a7-c7c5-4db0-bd64-77a664535f5c",
        "report_id": None,
        "mode": "document",
        "title": "Full checkup review — March 2025",
        "language": "en",
        "is_guest": False,
        "guest_token": None,
        "triage_status": None,
        "triage_result": None,
        "triage_completed_at": None,
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557722, tzinfo=datetime.timezone.utc
        ),
        "last_message_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557722, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "e794391b-accd-4d36-915a-6140c93daffe",
        "user_id": "604c02aa-b8f3-4c9c-b500-40bd75eec8c1",
        "report_id": None,
        "mode": "general",
        "title": "سؤال عن أدوية ضغط الدم",
        "language": "ar",
        "is_guest": False,
        "guest_token": None,
        "triage_status": None,
        "triage_result": None,
        "triage_completed_at": None,
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557722, tzinfo=datetime.timezone.utc
        ),
        "last_message_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557722, tzinfo=datetime.timezone.utc
        ),
    },
]
# 5 reports --------
[
    {
        "id": "9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6",
        "user_id": "604c02aa-b8f3-4c9c-b500-40bd75eec8c1",
        "file_url": "gs://med-ai-bucket/604c02aa-b8f3-4c9c-b500-40bd75eec8c1/cbc_report_001.pdf",
        "display_name": "CBC January 2025",
        "ocr_text_enc": "AES256:enc:...cbc_ocr_text...",
        "summary_enc": "AES256:enc:...cbc_summary...",
        "report_type": "cbc",
        "report_subtype": "cbc_with_differential",
        "detected_panels": ["CBC"],
        "panel_count": 1,
        "cardiac_urgency_flag": False,
        "detected_language": "ar",
        "is_bilingual": False,
        "report_language_mix": {"ar": 1.0, "en": 0.0},
        "status": "ready",
        "ocr_avg_confidence": 0.95,
        "ocr_min_confidence": 0.91,
        "document_quality": "high",
        "low_confidence_blocks": [],
        "uploaded_at": datetime.datetime(
            2025, 1, 10, 9, 0, tzinfo=datetime.timezone.utc
        ),
        "retention_expires_at": datetime.datetime(
            2027, 1, 10, 9, 0, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "df7b626b-0ea5-425a-940e-44fb037e88a6",
        "user_id": "604c02aa-b8f3-4c9c-b500-40bd75eec8c1",
        "file_url": "gs://med-ai-bucket/604c02aa-b8f3-4c9c-b500-40bd75eec8c1/full_checkup_001.pdf",
        "display_name": "Full Body Checkup March 2025",
        "ocr_text_enc": "AES256:enc:...full_checkup_ocr_text...",
        "summary_enc": "AES256:enc:...full_checkup_summary...",
        "report_type": "full_checkup",
        "report_subtype": None,
        "detected_panels": ["CBC", "Lipid Panel", "LFTs", "TFTs", "Cardiac Enzymes"],
        "panel_count": 5,
        "cardiac_urgency_flag": True,
        "detected_language": "bilingual",
        "is_bilingual": True,
        "report_language_mix": {"ar": 0.65, "en": 0.35},
        "status": "ready",
        "ocr_avg_confidence": 0.88,
        "ocr_min_confidence": 0.76,
        "document_quality": "medium",
        "low_confidence_blocks": [
            {"block_id": "b001", "text": "...", "confidence": 0.74},
            {"block_id": "b002", "text": "...", "confidence": 0.71},
        ],
        "uploaded_at": datetime.datetime(
            2025, 3, 1, 10, 0, tzinfo=datetime.timezone.utc
        ),
        "retention_expires_at": datetime.datetime(
            2027, 3, 1, 10, 0, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "50318f00-371b-482c-8c8d-1ab7e0f440df",
        "user_id": "043262a7-c7c5-4db0-bd64-77a664535f5c",
        "file_url": "gs://med-ai-bucket/043262a7-c7c5-4db0-bd64-77a664535f5c/xray_001.jpg",
        "display_name": "Chest X-Ray February 2025",
        "ocr_text_enc": None,
        "summary_enc": None,
        "report_type": "imaging_report",
        "report_subtype": None,
        "detected_panels": None,
        "panel_count": 1,
        "cardiac_urgency_flag": False,
        "detected_language": None,
        "is_bilingual": False,
        "report_language_mix": None,
        "status": "image_only",
        "ocr_avg_confidence": None,
        "ocr_min_confidence": None,
        "document_quality": None,
        "low_confidence_blocks": None,
        "uploaded_at": datetime.datetime(
            2025, 2, 14, 11, 0, tzinfo=datetime.timezone.utc
        ),
        "retention_expires_at": datetime.datetime(
            2027, 2, 14, 11, 0, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "f1ae82e6-c118-4de0-bd1b-97adb88eddf2",
        "user_id": "043262a7-c7c5-4db0-bd64-77a664535f5c",
        "file_url": "gs://med-ai-bucket/043262a7-c7c5-4db0-bd64-77a664535f5c/lipid_scan_001.pdf",
        "display_name": "Lipid Panel April 2025",
        "ocr_text_enc": None,
        "summary_enc": None,
        "report_type": "lipid_panel",
        "report_subtype": None,
        "detected_panels": None,
        "panel_count": 1,
        "cardiac_urgency_flag": False,
        "detected_language": None,
        "is_bilingual": False,
        "report_language_mix": None,
        "status": "ocr_failed",
        "ocr_avg_confidence": 0.6,
        "ocr_min_confidence": 0.45,
        "document_quality": "low",
        "low_confidence_blocks": [
            {"block_id": "b001", "text": "...", "confidence": 0.55},
            {"block_id": "b002", "text": "...", "confidence": 0.45},
        ],
        "uploaded_at": datetime.datetime(
            2025, 4, 5, 8, 0, tzinfo=datetime.timezone.utc
        ),
        "retention_expires_at": datetime.datetime(
            2027, 4, 5, 8, 0, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "260bbbfe-2b9c-4d9a-82a2-29134ba2f98c",
        "user_id": "604c02aa-b8f3-4c9c-b500-40bd75eec8c1",
        "file_url": "gs://med-ai-bucket/604c02aa-b8f3-4c9c-b500-40bd75eec8c1/diabetes_001.pdf",
        "display_name": "HbA1c Diabetes Panel May 2025",
        "ocr_text_enc": None,
        "summary_enc": None,
        "report_type": "diabetes_panel",
        "report_subtype": None,
        "detected_panels": None,
        "panel_count": 1,
        "cardiac_urgency_flag": False,
        "detected_language": "en",
        "is_bilingual": False,
        "report_language_mix": {"ar": 0.0, "en": 1.0},
        "status": "uploaded",
        "ocr_avg_confidence": None,
        "ocr_min_confidence": None,
        "document_quality": None,
        "low_confidence_blocks": None,
        "uploaded_at": datetime.datetime(
            2025, 5, 1, 7, 0, tzinfo=datetime.timezone.utc
        ),
        "retention_expires_at": datetime.datetime(
            2027, 5, 1, 7, 0, tzinfo=datetime.timezone.utc
        ),
    },
]
# 6 demo --------
[
    {
        "id": "48d53614-852d-4d30-8e07-4f5931e65341",
        "user_id": "604c02aa-b8f3-4c9c-b500-40bd75eec8c1",
        "age_range": "26-35",
        "gender": "male",
        "nationality": "SA",
        "region": "riyadh",
        "health_literacy": "medium",
        "chronic_conditions": ["diabetes", "hypertension"],
        "consent_for_research": True,
        "consent_given_at": datetime.datetime(
            2025, 1, 10, 8, 5, tzinfo=datetime.timezone.utc
        ),
        "created_at": datetime.datetime(
            2025, 1, 10, 8, 5, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "ad7848b1-c6c7-44d7-9e72-488ed1763e5e",
        "user_id": "043262a7-c7c5-4db0-bd64-77a664535f5c",
        "age_range": "36-45",
        "gender": "female",
        "nationality": "AE",
        "region": "dubai",
        "health_literacy": "high",
        "chronic_conditions": [],
        "consent_for_research": False,
        "consent_given_at": None,
        "created_at": datetime.datetime(
            2025, 2, 14, 10, 35, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "3d98909b-abd6-4b0c-9a26-1b5bf7ecd455",
        "user_id": "ff4975b9-2b05-4625-b9bc-e614af62e323",
        "age_range": "46-55",
        "gender": "male",
        "nationality": "SA",
        "region": "jeddah",
        "health_literacy": "high",
        "chronic_conditions": [],
        "consent_for_research": True,
        "consent_given_at": datetime.datetime(
            2025, 1, 5, 9, 10, tzinfo=datetime.timezone.utc
        ),
        "created_at": datetime.datetime(
            2025, 1, 5, 9, 10, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "33fde3f8-76db-4018-a40c-0d83154c895f",
        "user_id": "677f7b41-19fc-4d5f-8d4f-d65c716dfcae",
        "age_range": "56-65",
        "gender": "prefer_not_to_say",
        "nationality": "SA",
        "region": "eastern_province",
        "health_literacy": "low",
        "chronic_conditions": ["diabetes", "hypertension", "thyroid"],
        "consent_for_research": False,
        "consent_given_at": None,
        "created_at": datetime.datetime(
            2025, 3, 1, 14, 0, tzinfo=datetime.timezone.utc
        ),
    },
]
# 7 triage --------
[
    {
        "id": "472f5b9f-cbcc-4062-8c4c-3a05227c529c",
        "session_id": "4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae",
        "user_id": "604c02aa-b8f3-4c9c-b500-40bd75eec8c1",
        "result_level": "green",
        "urgency_score": 2,
        "result_summary_enc": "AES256:enc:...mild_symptoms_summary...",
        "result_recommendation_enc": "AES256:enc:...rest_and_hydration...",
        "symptoms_reported_enc": "AES256:enc:...headache_fatigue...",
        "result_language": "ar",
        "generated_at": datetime.datetime(
            2025, 1, 10, 9, 30, tzinfo=datetime.timezone.utc
        ),
        "viewed_at": datetime.datetime(
            2025, 1, 10, 9, 31, tzinfo=datetime.timezone.utc
        ),
        "patient_acted": "monitored_at_home",
    },
    {
        "id": "ebbad186-7815-45e4-a6d0-2878f1aaf1d7",
        "session_id": "e2385da2-08c4-4b7e-af76-97b947567d09",
        "user_id": "043262a7-c7c5-4db0-bd64-77a664535f5c",
        "result_level": "yellow",
        "urgency_score": 5,
        "result_summary_enc": "AES256:enc:...moderate_symptoms_summary...",
        "result_recommendation_enc": "AES256:enc:...visit_doctor_within_48hrs...",
        "symptoms_reported_enc": "AES256:enc:...chest_discomfort_shortness_of_breath...",
        "result_language": "en",
        "generated_at": datetime.datetime(
            2025, 2, 14, 11, 0, tzinfo=datetime.timezone.utc
        ),
        "viewed_at": datetime.datetime(
            2025, 2, 14, 11, 2, tzinfo=datetime.timezone.utc
        ),
        "patient_acted": "sought_care",
    },
    {
        "id": "df42b479-49c4-43dc-b781-b02f8597afe7",
        "session_id": "e794391b-accd-4d36-915a-6140c93daffe",
        "user_id": "604c02aa-b8f3-4c9c-b500-40bd75eec8c1",
        "result_level": "red",
        "urgency_score": 9,
        "result_summary_enc": "AES256:enc:...severe_symptoms_summary...",
        "result_recommendation_enc": "AES256:enc:...seek_emergency_care_immediately...",
        "symptoms_reported_enc": "AES256:enc:...chest_pain_sweating_arm_pain...",
        "result_language": "ar",
        "generated_at": datetime.datetime(
            2025, 3, 1, 14, 0, tzinfo=datetime.timezone.utc
        ),
        "viewed_at": datetime.datetime(2025, 3, 1, 14, 1, tzinfo=datetime.timezone.utc),
        "patient_acted": "ignored",
    },
]
# 8 llm --------
[
    {
        "id": "978420fc-67ac-4c61-bcd3-b24f8035a3ee",
        "session_id": "4cfc0ea8-b740-4eb8-b225-70dfd8bd6cae",
        "message_id": "28fd1664-1c46-4353-9b38-e14291ab4f59",
        "report_id": "9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6",
        "call_type": "chat",
        "assembled_prompt_enc": "AES256:enc:...zone1+zone2+zone3+zone4...",
        "raw_response_enc": "AES256:enc:...gemini_raw_response...",
        "guardrail_trigger_text_enc": None,
        "error_message_enc": None,
        "guardrail_fired": False,
        "guardrail_check": None,
        "retrieved_chunk_ids": [
            "2f0de9e2-2c3a-4f85-9d1f-9baf0946360e",
            "c019ae54-4fd4-42be-a704-2d6ded509711",
            "2dc152ec-f82f-49c7-ae70-a350e1fc894c",
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
        "temperature": 0.1,
        "error_code": None,
        "ocr_duration_ms": None,
        "embedding_duration_ms": 120,
        "retrieval_duration_ms": 85,
        "llm_duration_ms": 2100,
        "total_duration_ms": 2350,
        "created_at": datetime.datetime(
            2025, 1, 10, 9, 30, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "f53ba1b3-78eb-4de2-aef3-76a51d6d1e8f",
        "session_id": "e794391b-accd-4d36-915a-6140c93daffe",
        "message_id": "caf6858e-f52b-4371-a31a-00b8112698d1",
        "report_id": None,
        "call_type": "triage_completion",
        "assembled_prompt_enc": "AES256:enc:...triage_full_conversation_history...",
        "raw_response_enc": "AES256:enc:...triage_result_json...",
        "guardrail_trigger_text_enc": None,
        "error_message_enc": None,
        "guardrail_fired": False,
        "guardrail_check": None,
        "retrieved_chunk_ids": None,
        "cosine_scores": None,
        "panel_coverage": None,
        "zone1_tokens": 450,
        "zone2_tokens": 0,
        "zone3_tokens": 1200,
        "zone4_tokens": 0,
        "total_prompt_tokens": 1650,
        "completion_tokens": 180,
        "finish_reason": "STOP",
        "model_version": "gemini-1.5-pro",
        "temperature": 0.0,
        "error_code": None,
        "ocr_duration_ms": None,
        "embedding_duration_ms": None,
        "retrieval_duration_ms": None,
        "llm_duration_ms": 1800,
        "total_duration_ms": 1900,
        "created_at": datetime.datetime(
            2025, 2, 14, 11, 0, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "787f8804-c5f8-41a6-9590-ce820b5f48f0",
        "session_id": "e2385da2-08c4-4b7e-af76-97b947567d09",
        "message_id": None,
        "report_id": "df7b626b-0ea5-425a-940e-44fb037e88a6",
        "call_type": "summary",
        "assembled_prompt_enc": "AES256:enc:...full_checkup_summary_prompt...",
        "raw_response_enc": "AES256:enc:...full_checkup_summary_response...",
        "guardrail_trigger_text_enc": "AES256:enc:...cardiac_enzyme_text_that_triggered...",
        "error_message_enc": None,
        "guardrail_fired": True,
        "guardrail_check": "cardiac_urgency_override",
        "retrieved_chunk_ids": [
            "9e6893f2-734d-4ebf-bef4-7274420599ed",
            "a43ea41d-6ab9-4329-84ea-c0ba92c2df11",
            "91dd30d8-d15a-4cee-84d2-fd60a43bd21f",
            "733594f0-6725-4148-9bbe-f5cde896ee97",
        ],
        "cosine_scores": [0.95, 0.91, 0.89, 0.86, 0.82],
        "panel_coverage": {"CBC": 2, "Lipid Panel": 1, "Cardiac Enzymes": 2},
        "zone1_tokens": 450,
        "zone2_tokens": 1200,
        "zone3_tokens": 0,
        "zone4_tokens": 80,
        "total_prompt_tokens": 1730,
        "completion_tokens": 420,
        "finish_reason": "STOP",
        "model_version": "gemini-1.5-pro",
        "temperature": 0.1,
        "error_code": None,
        "ocr_duration_ms": 3200,
        "embedding_duration_ms": 250,
        "retrieval_duration_ms": 110,
        "llm_duration_ms": 3800,
        "total_duration_ms": 7400,
        "created_at": datetime.datetime(
            2025, 3, 1, 14, 0, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "31bc7458-a2ca-4727-8eeb-138c49385c1e",
        "session_id": None,
        "message_id": None,
        "report_id": "9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6",
        "call_type": "embedding",
        "assembled_prompt_enc": "AES256:enc:...chunk_text_batch...",
        "raw_response_enc": None,
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
        "total_prompt_tokens": 1200,
        "completion_tokens": 0,
        "finish_reason": "STOP",
        "model_version": "gemini-1.5-pro",
        "temperature": 0.0,
        "error_code": None,
        "ocr_duration_ms": 2800,
        "embedding_duration_ms": 340,
        "retrieval_duration_ms": None,
        "llm_duration_ms": 340,
        "total_duration_ms": 3200,
        "created_at": datetime.datetime(2025, 4, 5, 8, 0, tzinfo=datetime.timezone.utc),
    },
    {
        "id": "e705b6e0-cce0-467d-850f-62e77f14f8a4",
        "session_id": "e2385da2-08c4-4b7e-af76-97b947567d09",
        "message_id": "636a35a4-7548-4720-afe7-6590b9524eff",
        "report_id": "9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6",
        "call_type": "chat",
        "assembled_prompt_enc": "AES256:enc:...failed_call_prompt...",
        "raw_response_enc": None,
        "guardrail_trigger_text_enc": None,
        "error_message_enc": "AES256:enc:...vertex_ai_503_error_message...",
        "guardrail_fired": False,
        "guardrail_check": None,
        "retrieved_chunk_ids": [
            "c8f71c85-7004-4355-bbcd-0ebd3c0ffc49",
            "6c18ddea-3b54-49ee-9eb7-161f19c3692b",
        ],
        "cosine_scores": [0.9, 0.87],
        "panel_coverage": {"CBC": 2},
        "zone1_tokens": 450,
        "zone2_tokens": 600,
        "zone3_tokens": 200,
        "zone4_tokens": 45,
        "total_prompt_tokens": 1295,
        "completion_tokens": 0,
        "finish_reason": "ERROR",
        "model_version": "gemini-1.5-pro",
        "temperature": 0.1,
        "error_code": "VERTEX_AI_503",
        "ocr_duration_ms": None,
        "embedding_duration_ms": 115,
        "retrieval_duration_ms": 90,
        "llm_duration_ms": 5000,
        "total_duration_ms": 5250,
        "created_at": datetime.datetime(
            2025, 4, 10, 10, 0, tzinfo=datetime.timezone.utc
        ),
    },
]
# 9 lab --------
[
    {
        "id": "6bc2aeec-f662-4421-952d-e7a7d5e0522b",
        "report_id": "9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6",
        "panel_name": "CBC",
        "test_category": "haematology",
        "test_name": "الهيموغلوبين",
        "value": Decimal("13.5"),
        "unit": "g/dL",
        "normal_range_low": Decimal("12.0"),
        "normal_range_high": Decimal("16.0"),
        "flag": "normal",
        "extracted_language": "ar",
    },
    {
        "id": "c84986df-4ea9-42c3-b504-3171f5f62826",
        "report_id": "9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6",
        "panel_name": "CBC",
        "test_category": "haematology",
        "test_name": "White Blood Cell Count",
        "value": Decimal("11.8"),
        "unit": "10^3/uL",
        "normal_range_low": Decimal("4.5"),
        "normal_range_high": Decimal("11.0"),
        "flag": "high",
        "extracted_language": "en",
    },
    {
        "id": "6a0fb206-1e05-4868-98f3-deefac50fe41",
        "report_id": "df7b626b-0ea5-425a-940e-44fb037e88a6",
        "panel_name": "Cardiac Enzymes",
        "test_category": "cardiac_enzymes",
        "test_name": "Troponin I",
        "value": Decimal("2.85"),
        "unit": "ng/mL",
        "normal_range_low": Decimal("0.00"),
        "normal_range_high": Decimal("0.04"),
        "flag": "critical",
        "extracted_language": "en",
    },
    {
        "id": "0d5c8a1c-107f-422e-9b3c-e7f70bae0032",
        "report_id": "df7b626b-0ea5-425a-940e-44fb037e88a6",
        "panel_name": "Lipid Panel",
        "test_category": "biochemistry",
        "test_name": "LDL Cholesterol",
        "value": Decimal("3.25"),
        "unit": "mmol/L",
        "normal_range_low": Decimal("0.00"),
        "normal_range_high": Decimal("3.00"),
        "flag": "borderline_high",
        "extracted_language": "en",
    },
    {
        "id": "66e65c79-d66d-4ff0-9e6a-85e18821b1f3",
        "report_id": "df7b626b-0ea5-425a-940e-44fb037e88a6",
        "panel_name": "TFTs",
        "test_category": "endocrinology",
        "test_name": "TSH",
        "value": Decimal("0.28"),
        "unit": "mIU/L",
        "normal_range_low": Decimal("0.40"),
        "normal_range_high": Decimal("4.00"),
        "flag": "low",
        "extracted_language": "en",
    },
]
# 10 tuning --------
[
    {
        "id": "bb203870-4cfc-4afa-8220-16d49088a441",
        "source_session_id": "2bb77f2d-341f-44b2-aab2-d51f5643bf83",
        "source_message_id": "11e30dde-8ec7-4135-b55b-51a72149fcd5",
        "source_report_type": "cbc",
        "session_mode": "document",
        "system_prompt": "You are a medical AI assistant. Summarise lab results in plain language. Always end with a doctor consultation disclaimer. Never provide a diagnosis.",
        "report_context": "CBC Report — Male, 34. Hemoglobin: 9.2 g/dL (Low). WBC: 11.8 x10³/µL (High). Platelets: 145 x10³/µL (Normal).",
        "conversation_history": [
            {"role": "user", "content": "What does my blood test show?"},
            {
                "role": "assistant",
                "content": "Your report shows a lower than normal hemoglobin level and a slightly elevated white blood cell count. This may suggest anaemia alongside a possible infection or inflammation. Please discuss with your doctor.",
            },
        ],
        "user_question": "Should I be worried about my hemoglobin being low?",
        "assistant_response": "A hemoglobin of 9.2 g/dL is below the normal range for adult males (13.5-17.5 g/dL), which indicates mild to moderate anaemia. This can cause fatigue and shortness of breath. Your doctor may investigate the underlying cause. Please discuss these results with your doctor for a full medical interpretation.",
        "triage_result_level": None,
        "interaction_language": "en",
        "question_category": "lab_explanation",
        "report_panel": "CBC",
        "age_range": "26-35",
        "gender": "male",
        "nationality": "SA",
        "document_quality": "high",
        "patient_rating": 5,
        "guardrail_triggered": False,
        "clinician_validated": True,
        "clinician_rating": 5,
        "auto_quality_score": Decimal("0.94"),
        "dataset_version": "v1.0",
        "included_in_export": True,
        "export_batch_id": "d0deeeb3-d784-4414-9a2f-70b1f5f8edce",
        "phi_scan_passed": True,
        "phi_scan_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "8b52fb50-b50a-4909-ab70-6f436abce437",
        "source_session_id": "2bc992f8-0c97-4e51-9f20-1da1d2918af4",
        "source_message_id": "9c4cda96-5969-4841-b4fa-521b2149f46e",
        "source_report_type": "none",
        "session_mode": "triage",
        "system_prompt": "أنت مساعد طبي ذكاء اصطناعي. اطرح أسئلة منظمة حول الأعراض. لا تقدم تشخيصاً طبياً أبداً.",
        "report_context": None,
        "conversation_history": [
            {"role": "user", "content": "أعاني من صداع شديد منذ يومين مع غثيان"},
            {
                "role": "assistant",
                "content": "هل الصداع في منطقة معينة من الرأس؟ وهل تعاني من حساسية للضوء أو الصوت؟",
            },
            {
                "role": "user",
                "content": "نعم، في الجانب الأيسر فقط، ونعم أشعر بحساسية من الضوء",
            },
        ],
        "user_question": "ما الذي يسبب هذا الصداع؟",
        "assistant_response": "بناءً على ما وصفته — صداع شديد في جانب واحد مع غثيان وحساسية للضوء — قد تكون هذه أعراض الشقيقة (الصداع النصفي). يُنصح بمراجعة الطبيب لتقييم حالتك. يُرجى مناقشة هذه الأعراض مع طبيبك للحصول على تفسير طبي كامل.",
        "triage_result_level": "yellow",
        "interaction_language": "ar",
        "question_category": "symptom_triage",
        "report_panel": None,
        "age_range": "26-35",
        "gender": "female",
        "nationality": "SA",
        "document_quality": None,
        "patient_rating": 4,
        "guardrail_triggered": False,
        "clinician_validated": False,
        "clinician_rating": None,
        "auto_quality_score": Decimal("0.81"),
        "dataset_version": "v1.0",
        "included_in_export": False,
        "export_batch_id": None,
        "phi_scan_passed": True,
        "phi_scan_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "b491fbf4-5834-421e-ac53-9f8267d8c385",
        "source_session_id": "83e61dc6-09ff-4a51-b897-c11b18fa1c72",
        "source_message_id": "d495e711-1374-4d32-b4f9-a992d894c31a",
        "source_report_type": "full_checkup",
        "session_mode": "document",
        "system_prompt": "You are a medical AI assistant. Respond in the same language as the patient's question. Summarise lab results by panel. Never provide a diagnosis.",
        "report_context": "HbA1c Panel — HbA1c: 8.1% (High, ref: 4.0-5.6%). Fasting Glucose: 9.4 mmol/L (High, ref: 3.9-5.6 mmol/L). Lipid Panel — Total Cholesterol: 5.9 mmol/L (Borderline High).",
        "conversation_history": [
            {"role": "user", "content": "ما معنى HbA1c 8.1؟"},
            {
                "role": "assistant",
                "content": "مستوى HbA1c 8.1% أعلى من المعدل الطبيعي (4.0-5.6%). يعكس هذا المستوى متوسط سكر الدم خلال الأشهر الثلاثة الماضية. يُرجى مناقشة النتيجة مع طبيبك.",
            },
        ],
        "user_question": "Is my diabetes under control based on this result?",
        "assistant_response": "An HbA1c of 8.1% suggests that blood sugar levels have been above the target range over the past three months. For most adults with diabetes, the target is below 7.0%. This does not mean your condition cannot be managed — your doctor can review your treatment plan. Please discuss these results with your doctor for a full medical interpretation.",
        "triage_result_level": None,
        "interaction_language": "mixed",
        "question_category": "panel_specific_query",
        "report_panel": "HbA1c",
        "age_range": "46-55",
        "gender": "male",
        "nationality": "AE",
        "document_quality": "high",
        "patient_rating": 4,
        "guardrail_triggered": False,
        "clinician_validated": True,
        "clinician_rating": 4,
        "auto_quality_score": Decimal("0.88"),
        "dataset_version": "v1.0",
        "included_in_export": True,
        "export_batch_id": "a6545cc6-558c-4e1b-b440-88747762f065",
        "phi_scan_passed": True,
        "phi_scan_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "f0772c32-db7c-42f3-b27a-11a405651e7d",
        "source_session_id": "1dfd99cc-6fb2-4e0f-b9db-d95c7f23f1df",
        "source_message_id": "23ce8229-33b0-4c4c-bb10-6dc7115c5591",
        "source_report_type": "none",
        "session_mode": "general",
        "system_prompt": "You are a medical AI assistant. Answer general health questions with caution. Never prescribe medication or provide a diagnosis.",
        "report_context": None,
        "conversation_history": [],
        "user_question": "What is metformin usually prescribed for?",
        "assistant_response": "Metformin is a medication commonly used to manage type 2 diabetes. It works by reducing glucose production in the liver and improving insulin sensitivity. It is typically prescribed alongside lifestyle changes such as diet and exercise. Only a doctor can determine whether metformin is appropriate for your situation. Please discuss this with your doctor for a full medical interpretation.",
        "triage_result_level": None,
        "interaction_language": "en",
        "question_category": "medication_query",
        "report_panel": None,
        "age_range": "36-45",
        "gender": "female",
        "nationality": "SA",
        "document_quality": None,
        "patient_rating": 5,
        "guardrail_triggered": False,
        "clinician_validated": True,
        "clinician_rating": 5,
        "auto_quality_score": Decimal("0.92"),
        "dataset_version": "v1.0",
        "included_in_export": True,
        "export_batch_id": "50ca0ac5-a6ad-45a4-b399-3283be98d329",
        "phi_scan_passed": True,
        "phi_scan_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "2105a5af-01c1-471f-a6fb-da9f54dca4a3",
        "source_session_id": "383dee92-b6cb-4937-a826-776091f7e973",
        "source_message_id": "1d7176b7-d254-4e98-aa3f-b698a01fbebb",
        "source_report_type": "lipid_panel",
        "session_mode": "document",
        "system_prompt": "You are a medical AI assistant. Summarise lab results in plain language. Always end with a doctor consultation disclaimer. Never provide a diagnosis.",
        "report_context": "Lipid Panel — Total Cholesterol: 6.4 mmol/L (High). LDL: 4.2 mmol/L (High). HDL: 0.9 mmol/L (Low). Triglycerides: 2.8 mmol/L (Borderline High).",
        "conversation_history": [
            {"role": "user", "content": "Are my cholesterol levels dangerous?"},
            {
                "role": "assistant",
                "content": "Your total cholesterol and LDL are above the recommended range, and your HDL (the protective cholesterol) is lower than ideal. Together these may increase cardiovascular risk. Please discuss with your doctor.",
            },
        ],
        "user_question": "What lifestyle changes can help lower LDL?",
        "assistant_response": "Common approaches to lowering LDL include reducing saturated fat intake, increasing soluble fibre, engaging in regular aerobic exercise, and maintaining a healthy weight. However, the right plan depends on your overall health picture. Please discuss these results with your doctor for a full medical interpretation.",
        "triage_result_level": None,
        "interaction_language": "en",
        "question_category": "lab_explanation",
        "report_panel": "Lipid Panel",
        "age_range": "56-65",
        "gender": "male",
        "nationality": "SA",
        "document_quality": "medium",
        "patient_rating": None,
        "guardrail_triggered": False,
        "clinician_validated": False,
        "clinician_rating": None,
        "auto_quality_score": Decimal("0.74"),
        "dataset_version": "v1.0",
        "included_in_export": False,
        "export_batch_id": None,
        "phi_scan_passed": False,
        "phi_scan_at": None,
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
    },
]
# 11 extension --------
[
    {
        "id": "9f440c59-a3a0-4863-8901-b72b1dd63966",
        "user_id": "604c02aa-b8f3-4c9c-b500-40bd75eec8c1",
        "hook_name": "telemedicine_enabled",
        "hook_value": {
            "provider": "seha",
            "provider_display_name": "Seha Virtual Care",
            "redirect_url": "https://seha.ae/consult",
            "preferred_language": "ar",
            "preferred_slot": "morning",
            "auto_escalate_red_triage": True,
        },
        "is_active": True,
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
        "updated_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "c428536d-bf9f-47d3-8ad7-5254eac86ed7",
        "user_id": "604c02aa-b8f3-4c9c-b500-40bd75eec8c1",
        "hook_name": "whatsapp_followup_enabled",
        "hook_value": {
            "whatsapp_number": "+966500000000",
            "followup_delay_hours": 48,
            "trigger_on": ["yellow", "red"],
            "message_language": "ar",
            "opt_out_token": "abc123xyz",
        },
        "is_active": True,
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
        "updated_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "4a16e77d-3142-4f7f-83eb-c3ac9043ba2c",
        "user_id": "043262a7-c7c5-4db0-bd64-77a664535f5c",
        "hook_name": "payment_gateway_url",
        "hook_value": {
            "gateway": "moyasar",
            "gateway_display_name": "Moyasar",
            "publishable_key": "pk_test_placeholder",
            "currency": "SAR",
            "billable_features": ["triage_session", "document_upload"],
            "free_tier_limit": {"triage_sessions": 1, "document_uploads": 0},
        },
        "is_active": False,
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
        "updated_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
    },
    {
        "id": "af4c055c-9f0c-4d16-b46e-04e7e58350af",
        "user_id": "043262a7-c7c5-4db0-bd64-77a664535f5c",
        "hook_name": "physician_escalation_webhook",
        "hook_value": {
            "webhook_url": "https://internal.clinic-system.sa/api/escalate",
            "auth_header": "X-Webhook-Secret",
            "secret_ref": "projects/med-ai/secrets/clinic_webhook_secret/versions/latest",
            "trigger_on": ["red"],
            "include_fields": [
                "session_id",
                "urgency_score",
                "symptoms_reported",
                "result_summary",
            ],
            "timeout_seconds": 10,
            "retry_attempts": 3,
        },
        "is_active": True,
        "created_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
        "updated_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 554972, tzinfo=datetime.timezone.utc
        ),
    },
]
# 12 clicnical --------
[
    {
        "id": "adef58c6-7a61-4cf1-8f95-91791699efaa",
        "message_id": "28fd1664-1c46-4353-9b38-e14291ab4f59",
        "reviewer_id": "ff4975b9-2b05-4625-b9bc-e614af62e323",
        "accuracy_rating": 5,
        "safety_rating": 5,
        "completeness_rating": 5,
        "contains_error": False,
        "error_description": None,
        "suggested_correction": None,
        "is_safe_to_train_on": True,
        "reviewed_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557717, tzinfo=datetime.timezone.utc
        ),
        "review_duration_sec": 142,
    },
    {
        "id": "45177fee-fdf2-433d-988c-2f1c8e7d71c2",
        "message_id": "636a35a4-7548-4720-afe7-6590b9524eff",
        "reviewer_id": "ff4975b9-2b05-4625-b9bc-e614af62e323",
        "accuracy_rating": 4,
        "safety_rating": 5,
        "completeness_rating": 3,
        "contains_error": False,
        "error_description": None,
        "suggested_correction": "Response should mention that a fasting lipid retest is typically required before clinical decisions are made on borderline results.",
        "is_safe_to_train_on": True,
        "reviewed_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557717, tzinfo=datetime.timezone.utc
        ),
        "review_duration_sec": 98,
    },
    {
        "id": "96c670b8-1a3a-4c3a-9929-1ac1b378f9ea",
        "message_id": "caf6858e-f52b-4371-a31a-00b8112698d1",
        "reviewer_id": "ff4975b9-2b05-4625-b9bc-e614af62e323",
        "accuracy_rating": 2,
        "safety_rating": 3,
        "completeness_rating": 3,
        "contains_error": True,
        "error_description": "The response stated the HbA1c target for diabetic patients is below 6.0%. The correct general target for most adults with type 2 diabetes is below 7.0% (ADA guideline). Citing 6.0% could cause unnecessary patient anxiety.",
        "suggested_correction": "Replace '6.0%' with '7.0%' and note that individual targets vary — some patients may have a higher target set by their doctor depending on age and comorbidities.",
        "is_safe_to_train_on": False,
        "reviewed_at": datetime.datetime(
            2026, 5, 1, 6, 28, 30, 557717, tzinfo=datetime.timezone.utc
        ),
        "review_duration_sec": 187,
    },
]
