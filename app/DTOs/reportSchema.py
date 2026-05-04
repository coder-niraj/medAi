import array
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date, datetime

from helpers.msg import msg


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
    report_id: Optional[UUID] = None
    status: str
    Message_en: Optional[str] = None
    Message_ar: Optional[str] = None


class ReportUrlRepsonse(BaseModel):
    file_url: str
    expires_at: datetime
    content_type: Optional[str] = None
    display_name: str
    is_image_only: bool


class ReportImageResponse(BaseModel):
    report_id: UUID
    status: str
    message_ar: str = msg("errors", "image_only", "ar")
    message_en: str = msg("errors", "image_only", "en")


class ReportDelete(BaseModel):
    report_id: UUID
