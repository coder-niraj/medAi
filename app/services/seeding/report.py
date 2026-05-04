import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from decimal import Decimal

from models.reports import Report

dummy_reports = [
    {
        "id": uuid.UUID("9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6"),
        "user_id": uuid.UUID("604c02aa-b8f3-4c9c-b500-40bd75eec8c1"),  # Ahmed Al-Rashidi
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
        "ocr_avg_confidence": Decimal("0.9500"),
        "ocr_min_confidence": Decimal("0.9100"),
        "document_quality": "high",
        "low_confidence_blocks": [],
        "uploaded_at": datetime(2025, 1, 10, 9, 0, tzinfo=timezone.utc),
        "retention_expires_at": datetime(2027, 1, 10, 9, 0, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("df7b626b-0ea5-425a-940e-44fb037e88a6"),
        "user_id": uuid.UUID("604c02aa-b8f3-4c9c-b500-40bd75eec8c1"),  # Ahmed Al-Rashidi
        "file_url": "gs://med-ai-bucket/604c02aa-b8f3-4c9c-b500-40bd75eec8c1/full_checkup_001.pdf",
        "display_name": "Full Body Checkup March 2025",
        "ocr_text_enc": "AES256:enc:...full_checkup_ocr_text...",
        "summary_enc": "AES256:enc:...full_checkup_summary...",
        "report_type": "full_checkup",
        "report_subtype": None,
        "detected_panels": ["CBC", "Lipid Panel", "LFTs", "TFTs", "Cardiac Enzymes"],
        "panel_count": 5,
        "cardiac_urgency_flag": True,   # cardiac enzymes critical
        "detected_language": "bilingual",
        "is_bilingual": True,
        "report_language_mix": {"ar": 0.65, "en": 0.35},
        "status": "ready",
        "ocr_avg_confidence": Decimal("0.8800"),
        "ocr_min_confidence": Decimal("0.7600"),
        "document_quality": "medium",
        "low_confidence_blocks": [
            {"block_id": "b001", "text": "...", "confidence": 0.74},
            {"block_id": "b002", "text": "...", "confidence": 0.71},
        ],
        "uploaded_at": datetime(2025, 3, 1, 10, 0, tzinfo=timezone.utc),
        "retention_expires_at": datetime(2027, 3, 1, 10, 0, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("50318f00-371b-482c-8c8d-1ab7e0f440df"),
        "user_id": uuid.UUID("043262a7-c7c5-4db0-bd64-77a664535f5c"),  # Sarah Mitchell
        "file_url": "gs://med-ai-bucket/043262a7-c7c5-4db0-bd64-77a664535f5c/xray_001.jpg",
        "display_name": "Chest X-Ray February 2025",
        "ocr_text_enc": None,           # image_only — no OCR
        "summary_enc": None,
        "report_type": "imaging_report",
        "report_subtype": None,
        "detected_panels": None,
        "panel_count": 1,
        "cardiac_urgency_flag": False,
        "detected_language": None,
        "is_bilingual": False,
        "report_language_mix": None,
        "status": "image_only",         # OCR pipeline NOT initiated
        "ocr_avg_confidence": None,
        "ocr_min_confidence": None,
        "document_quality": None,
        "low_confidence_blocks": None,
        "uploaded_at": datetime(2025, 2, 14, 11, 0, tzinfo=timezone.utc),
        "retention_expires_at": datetime(2027, 2, 14, 11, 0, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("f1ae82e6-c118-4de0-bd1b-97adb88eddf2"),
        "user_id": uuid.UUID("043262a7-c7c5-4db0-bd64-77a664535f5c"),  # Sarah Mitchell
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
        "status": "ocr_failed",         # pipeline stopped
        "ocr_avg_confidence": Decimal("0.6000"),
        "ocr_min_confidence": Decimal("0.4500"),
        "document_quality": "low",
        "low_confidence_blocks": [
            {"block_id": "b001", "text": "...", "confidence": 0.55},
            {"block_id": "b002", "text": "...", "confidence": 0.45},
        ],
        "uploaded_at": datetime(2025, 4, 5, 8, 0, tzinfo=timezone.utc),
        "retention_expires_at": datetime(2027, 4, 5, 8, 0, tzinfo=timezone.utc),
    },
    {
        "id": uuid.UUID("260bbbfe-2b9c-4d9a-82a2-29134ba2f98c"),
        "user_id": uuid.UUID("604c02aa-b8f3-4c9c-b500-40bd75eec8c1"),  # Ahmed Al-Rashidi
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
        "status": "uploaded",           # pipeline not started yet
        "ocr_avg_confidence": None,
        "ocr_min_confidence": None,
        "document_quality": None,
        "low_confidence_blocks": None,
        "uploaded_at": datetime(2025, 5, 1, 7, 0, tzinfo=timezone.utc),
        "retention_expires_at": datetime(2027, 5, 1, 7, 0, tzinfo=timezone.utc),
    },
]


def seed_reports(db: Session):
    print("➡️ Seeding triage results...")

    for data in dummy_reports:
        db.merge(Report(**data))  # safe re-run

    db.flush()  # no commit here
    db.commit() 

    print(f"✅ Seeded {len(dummy_reports)} triage results")