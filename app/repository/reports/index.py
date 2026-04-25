import datetime
from datetime import timedelta, timezone, datetime
from typing import Any
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from helpers.audit import set_audit_state
from helpers.error_management import msg
from models.reports import Report
from utils.cloud import StorageManager


class ReportRepo:
    def __init__(self, db: Session):
        self.db = db

    def report_list(self, reports) -> list[dict[str, Any]]:
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

    def save_document_data_to_table(
        self, file_url, user_id, display_name, report_type, mime_type
    ):
        if (
            mime_type == "image/jpg"
            or mime_type == "image/png"
            or mime_type == "image/jpeg"
        ):
            status = "image_only"
        else:
            status = "uploaded"
        uploaded_at = datetime.now(timezone.utc)
        expires_at = uploaded_at + timedelta(days=365)

        # Use keyword arguments here:
        report_data = Report(
            user_id=user_id,
            file_url=file_url,
            display_name=display_name,
            report_type=report_type,
            status=status,
            uploaded_at=uploaded_at,  # Check if your model uses 'created_at' or ''
            retention_expires_at=expires_at,
        )

        self.db.add(report_data)
        try:
            self.db.commit()
        except:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail={
                    "message_ar": msg("errors", "db_failed", "ar"),
                    "message_en": msg("errors", "db_failed", "en"),
                },
            )
        self.db.refresh(report_data)
        return report_data

    def get_list_of_all_reports(
        self, request: Request, user_id
    ) -> list[dict[str, Any]]:
        try:
            all_reports = self.db.query(Report).filter(Report.user_id == user_id).all()

            set_audit_state(
                request,
                action="READ",
                resource_type="report",
                outcome="SUCCESS",
                resource_id=user_id,
            )
            return self.report_list(all_reports)
        except Exception as e:
            print(e)

            set_audit_state(
                request,
                action="READ",
                resource_type="report",
                outcome="FAILURE",
                resource_id=user_id,
            )
            raise HTTPException(
                status_code=500,
                detail={
                    "message_ar": msg("errors", "db_failed", "ar"),
                    "message_en": msg("errors", "db_failed", "en"),
                },
            )

    def get_report_by_id(self, report_id, user_id):
        try:
            return (
                self.db.query(Report)
                .filter(Report.id == report_id, Report.user_id == user_id)
                .first()
            )
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail={
                    "message_ar": msg("errors", "db_failed", "ar"),
                    "message_en": msg("errors", "db_failed", "en"),
                },
            )

    def delete_report_by_id(
        self, request: Request, report_id, user_id
    ) -> dict[str, bool]:
        try:
            storage = StorageManager()

            # 1. Check exists first
            report_obj = (
                self.db.query(Report)
                .filter(Report.id == report_id, Report.user_id == user_id)
                .first()
            )

            if not report_obj:
                set_audit_state(
                    request,
                    action="DELETE",
                    resource_type="report",
                    outcome="FAILURE",
                    resource_id=report_id,
                )
                raise HTTPException(
                    status_code=404,
                    detail={
                        "message_ar": msg("errors", "report_not_found", "ar"),
                        "message_en": msg("errors", "report_not_found", "en"),
                    },
                )

            # 2. Delete from storage first
            try:
                storage.delete_file(report=report_obj)
            except Exception as e:

                set_audit_state(
                    request,
                    action="DELETE",
                    resource_type="report",
                    outcome="FAILURE",
                    resource_id=report_id,
                )
                raise HTTPException(
                    status_code=500,
                    detail={
                        "message_ar": msg("errors", "storage_failed", "ar"),
                        "message_en": msg("errors", "storage_failed", "en"),
                    },
                )

            # 3. Then delete from DB
            self.db.delete(report_obj)
            self.db.commit()

            set_audit_state(
                request,
                action="DELETE",
                resource_type="report",
                outcome="SUCCESS",
                resource_id=report_id,
            )
            return {"deleted": True}

        except HTTPException:
            raise

        except Exception as e:

            self.db.rollback()

            set_audit_state(
                request,
                action="DELETE",
                resource_type="report",
                outcome="FAILURE",
                resource_id=report_id,
            )
            raise HTTPException(
                status_code=500,
                detail={
                    "message_ar": msg("errors", "db_failed", "ar"),
                    "message_en": msg("errors", "db_failed", "en"),
                },
            )
