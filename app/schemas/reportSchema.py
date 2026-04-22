import array
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date, datetime


class ReportType(str, Enum):
    CBC = "cbc"
    DIABETES = "diabetes_panel"
    LIPID = "lipid_panel"
    VITAMINS = "vitamins_minerals"
    THYROID = "thyroid"
    LFT = "lft"
    KFT = "kft"
    URINALYSIS = "urinalysis"
    CARDIAC = "cardiac_enzymes"
    HORMONES = "hormones"
    TUMOUR = "tumour_markers"
    FULL_CHECKUP = "full_checkup"
    PRESCRIPTION = "prescription"
    IMAGING = "imaging_report"
    OTHER = "other"


class ReportSchema(BaseModel):
    id: Optional[UUID]
    user_id: UUID
    file_url: str
    display_name: str
    report_type: ReportType
    retention_expires_at: Optional[str]
    uploaded_at: Optional[str]
    is_bilingual: Optional[str]
    cardiac_urgency_flag: Optional[str]
    panel_count: Optional[str]
    status: Optional[str]


class ReportResponse(BaseModel):
    id: UUID
    file_url: str
    display_name: str
    report_type: str
    uploaded_at: str
    is_bilingual: str
    cardiac_urgency_flag: str
    detected_panels: str
    panel_count: str
    status: str
    document_quality: str
    abnormal_count: str


class ReportDocumentResponse(BaseModel):
    report_id: UUID
    status: str


class ReportImageResponse(BaseModel):
    report_id: UUID
    status: str
    message: str = (
        "Image stored. Please also upload the written report from your radiologist for AI explanation."
    )


class ReportDelete(BaseModel):
    report_id: UUID


def report_list(reports):
    return [
        {
            "id": str(report.id),
            "display_name": report.display_name,
            "report_type": report.report_type,
            "report_subtype": report.report_subtype,
            "panel_count": report.panel_count,
            "detected_panels": report.detected_panels,
            "document_quality": report.document_quality,
            # "abnormal_count": report.abnormal_count,
            "cardiac_urgency_flag": report.cardiac_urgency_flag,
            "is_bilingual": report.is_bilingual,
            "status": report.status,
            "uploaded_at": (
                report.uploaded_at.isoformat() if report.uploaded_at else None
            ),
        }
        for report in reports
    ]
