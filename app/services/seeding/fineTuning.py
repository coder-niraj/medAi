import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from decimal import Decimal
from models.fineTuning import FineTuningExample

dummy_fine_tuning_examples = [
    # 1. Document mode — CBC, English, clinician validated,
    #    included in export, phi scan passed
    {
        "id": uuid.UUID("bb203870-4cfc-4afa-8220-16d49088a441"),
        "source_session_id": uuid.UUID("2bb77f2d-341f-44b2-aab2-d51f5643bf83"),
        "source_message_id": uuid.UUID("11e30dde-8ec7-4135-b55b-51a72149fcd5"),
        "source_report_type": "cbc",
        "session_mode": "document",
        "system_prompt": "You are a medical AI assistant. Summarise lab results in plain language. Always end with a doctor consultation disclaimer. Never provide a diagnosis.",
        "report_context": "CBC Report — Male, 34. Hemoglobin: 9.2 g/dL (Low). WBC: 11.8 x10³/µL (High). Platelets: 145 x10³/µL (Normal).",
        "conversation_history": [
            {
                "role": "user",
                "content": "What does my blood test show?",
            },
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
        "export_batch_id": uuid.UUID("d0deeeb3-d784-4414-9a2f-70b1f5f8edce"),
        "phi_scan_passed": True,
        "phi_scan_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
    },

    # 2. Triage mode — Arabic, yellow result,
    #    not clinician validated yet, not exported
    {
        "id": uuid.UUID("8b52fb50-b50a-4909-ab70-6f436abce437"),
        "source_session_id": uuid.UUID("2bc992f8-0c97-4e51-9f20-1da1d2918af4"),
        "source_message_id": uuid.UUID("9c4cda96-5969-4841-b4fa-521b2149f46e"),
        "source_report_type": "none",
        "session_mode": "triage",
        "system_prompt": "أنت مساعد طبي ذكاء اصطناعي. اطرح أسئلة منظمة حول الأعراض. لا تقدم تشخيصاً طبياً أبداً.",
        "report_context": None,         # triage has no report context
        "conversation_history": [
            {
                "role": "user",
                "content": "أعاني من صداع شديد منذ يومين مع غثيان",
            },
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
        "report_panel": None,           # triage has no panel
        "age_range": "26-35",
        "gender": "female",
        "nationality": "SA",
        "document_quality": None,       # triage has no document quality
        "patient_rating": 4,
        "guardrail_triggered": False,
        "clinician_validated": False,   # pending clinician review
        "clinician_rating": None,
        "auto_quality_score": Decimal("0.81"),
        "dataset_version": "v1.0",
        "included_in_export": False,    # not exported yet
        "export_batch_id": None,
        "phi_scan_passed": True,
        "phi_scan_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
    },

    # 3. Document mode — full checkup, mixed language AR/EN,
    #    HbA1c panel, clinician validated, included in export
    {
        "id": uuid.UUID("b491fbf4-5834-421e-ac53-9f8267d8c385"),
        "source_session_id": uuid.UUID("83e61dc6-09ff-4a51-b897-c11b18fa1c72"),
        "source_message_id": uuid.UUID("d495e711-1374-4d32-b4f9-a992d894c31a"),
        "source_report_type": "full_checkup",
        "session_mode": "document",
        "system_prompt": "You are a medical AI assistant. Respond in the same language as the patient's question. Summarise lab results by panel. Never provide a diagnosis.",
        "report_context": "HbA1c Panel — HbA1c: 8.1% (High, ref: 4.0-5.6%). Fasting Glucose: 9.4 mmol/L (High, ref: 3.9-5.6 mmol/L). Lipid Panel — Total Cholesterol: 5.9 mmol/L (Borderline High).",
        "conversation_history": [
            {
                "role": "user",
                "content": "ما معنى HbA1c 8.1؟",
            },
            {
                "role": "assistant",
                "content": "مستوى HbA1c 8.1% أعلى من المعدل الطبيعي (4.0-5.6%). يعكس هذا المستوى متوسط سكر الدم خلال الأشهر الثلاثة الماضية. يُرجى مناقشة النتيجة مع طبيبك.",
            },
        ],
        "user_question": "Is my diabetes under control based on this result?",
        "assistant_response": "An HbA1c of 8.1% suggests that blood sugar levels have been above the target range over the past three months. For most adults with diabetes, the target is below 7.0%. This does not mean your condition cannot be managed — your doctor can review your treatment plan. Please discuss these results with your doctor for a full medical interpretation.",
        "triage_result_level": None,
        "interaction_language": "mixed",  # AR question then EN follow-up
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
        "export_batch_id": uuid.UUID("a6545cc6-558c-4e1b-b440-88747762f065"),
        "phi_scan_passed": True,
        "phi_scan_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
    },

    # 4. General mode — medication query, English,
    #    no report context, clinician validated, exported
    {
        "id": uuid.UUID("f0772c32-db7c-42f3-b27a-11a405651e7d"),
        "source_session_id": uuid.UUID("1dfd99cc-6fb2-4e0f-b9db-d95c7f23f1df"),
        "source_message_id": uuid.UUID("23ce8229-33b0-4c4c-bb10-6dc7115c5591"),
        "source_report_type": "none",
        "session_mode": "general",
        "system_prompt": "You are a medical AI assistant. Answer general health questions with caution. Never prescribe medication or provide a diagnosis.",
        "report_context": None,         # general mode has no report
        "conversation_history": [],     # no prior turns
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
        "export_batch_id": uuid.UUID("50ca0ac5-a6ad-45a4-b399-3283be98d329"),
        "phi_scan_passed": True,
        "phi_scan_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
    },

    # 5. Document mode — lipid panel, phi_scan_passed = FALSE
    #    blocked from export — critical safety gate test
    {
        "id": uuid.UUID("2105a5af-01c1-471f-a6fb-da9f54dca4a3"),
        "source_session_id": uuid.UUID("383dee92-b6cb-4937-a826-776091f7e973"),
        "source_message_id": uuid.UUID("1d7176b7-d254-4e98-aa3f-b698a01fbebb"),
        "source_report_type": "lipid_panel",
        "session_mode": "document",
        "system_prompt": "You are a medical AI assistant. Summarise lab results in plain language. Always end with a doctor consultation disclaimer. Never provide a diagnosis.",
        "report_context": "Lipid Panel — Total Cholesterol: 6.4 mmol/L (High). LDL: 4.2 mmol/L (High). HDL: 0.9 mmol/L (Low). Triglycerides: 2.8 mmol/L (Borderline High).",
        "conversation_history": [
            {
                "role": "user",
                "content": "Are my cholesterol levels dangerous?",
            },
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
        "patient_rating": None,         # no rating given
        "guardrail_triggered": False,
        "clinician_validated": False,
        "clinician_rating": None,
        "auto_quality_score": Decimal("0.74"),
        "dataset_version": "v1.0",
        "included_in_export": False,    # blocked — phi_scan_passed = FALSE
        "export_batch_id": None,
        "phi_scan_passed": False,       # PHI scan failed — cannot export
        "phi_scan_at": None,            # scan not completed
        "created_at": datetime(2026, 5, 1, 6, 28, 30, 554972, tzinfo=timezone.utc),
    },
]





def seed_fine_tuning_examples(db: Session):
    print("➡️ Seeding triage results...")

    for data in dummy_fine_tuning_examples:
        db.merge(FineTuningExample(**data))  # safe re-run

    db.flush()  # no commit here
    db.commit() 

    print(f"✅ Seeded {len(dummy_fine_tuning_examples)} fine tuning")