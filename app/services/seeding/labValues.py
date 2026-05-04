import uuid
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.lab import LabValue

dummy_lab_values = [
    # 1. CBC — Hemoglobin, Arabic test name, normal
    {
        "id": uuid.UUID("6bc2aeec-f662-4421-952d-e7a7d5e0522b"),
        "report_id": uuid.UUID("9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6"),  # CBC report
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
    # 2. CBC — White Blood Cell Count, high flag
    {
        "id": uuid.UUID("c84986df-4ea9-42c3-b504-3171f5f62826"),
        "report_id": uuid.UUID("9fdba70b-e8f9-48a9-9e99-fd2e7e3715f6"),  # CBC report
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
        "id": uuid.UUID("6a0fb206-1e05-4868-98f3-deefac50fe41"),
        "report_id": uuid.UUID("df7b626b-0ea5-425a-940e-44fb037e88a6"),  # full checkup report
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
        "id": uuid.UUID("0d5c8a1c-107f-422e-9b3c-e7f70bae0032"),
        "report_id": uuid.UUID("df7b626b-0ea5-425a-940e-44fb037e88a6"),  # full checkup report
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
    # 5. TFTs — TSH, low flag, bilingual report
    {
        "id": uuid.UUID("66e65c79-d66d-4ff0-9e6a-85e18821b1f3"),
        "report_id": uuid.UUID("df7b626b-0ea5-425a-940e-44fb037e88a6"),  # full checkup report
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



def seed_lab_values(db: Session):
    print("➡️ Seeding triage results...")

    for data in dummy_lab_values:
        db.merge(LabValue(**data))  # safe re-run

    db.flush()  # no commit here
    db.commit() 

    print(f"✅ Seeded {len(dummy_lab_values)} lab values")