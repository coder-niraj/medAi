from datetime import datetime, timedelta, timezone
from typing import Any
import uuid

from helpers.audit_context import set_audit_state
from helpers.msg import msg
from repository.reports.index import ReportRepo
from fastapi import File, HTTPException, Request, status
from utils.firebase import verify_token
from DTOs.reportSchema import ReportDocumentResponse, ReportSchema, ReportUrlRepsonse
from services.storage_service import StorageManager


class ReportServices:

    def __init__(self, report_repo: ReportRepo, storage: StorageManager):
        self.report_repo = report_repo
        self.storage = storage

    def is_Image(self, mime_type):
        if (
            mime_type == "image/jpg"
            or mime_type == "image/png"
            or mime_type == "image/jpeg"
        ):
            return True
        else:
            return False

    def get_url_24_hours(self, request: Request, report_id, user_id):
        report_data = self.report_repo.get_report_by_id(report_id, user_id)
        request.state.user_id = user_id
        if not report_data:

            set_audit_state(
                request,
                action="READ",
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
        report_name = report_data.file_url.rsplit("/", 1)[-1]
        file_obj = self.storage.get_short_lived_url(blob_name=report_name)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

        set_audit_state(
            request,
            action="READ",
            resource_type="report",
            outcome="SUCCESS",
            resource_id=report_id,
        )
        return ReportUrlRepsonse(
            file_url=file_obj.get("url"),
            content_type=file_obj.get("content_type"),
            display_name=report_data.display_name,
            expires_at=expires_at,
            is_image_only=self.is_Image(mime_type=file_obj.get("content_type")),
        )

    def save_file(
        self, file_bytes, display_name, report_type, user_id, mime_type
    ) -> ReportDocumentResponse:
        extension_map = {
            "application/pdf": ".pdf",
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/png": ".png",
        }
        ext = extension_map.get(mime_type, "")
        file_name = f"{uuid.uuid4()}{ext}"
        file_url = self.storage.upload_file(file_bytes, file_name, mime_type)
        report_data = self.report_repo.save_document_data_to_table(
            file_url, user_id, display_name, report_type, mime_type
        )
        if self.is_Image(mime_type):
            return ReportDocumentResponse(
                report_id=report_data.id,
                status="image_only",
                Message_ar=msg("errors", "image_only", "ar"),
                Message_en=msg("errors", "image_only", "en"),
            )
        else:
            return ReportDocumentResponse(report_id=report_data.id, status="uploaded")

    def get_list_reports(self, request: Request, user_id) -> list[dict[str, Any]]:
        request.state.user_id = user_id
        return self.report_repo.get_list_of_all_reports(request, user_id)

    def delete_report(self, request: Request, report_id, user_id) -> dict[str, bool]:
        request.state.user_id = user_id
        return self.report_repo.delete_report_by_id(request, report_id, user_id)
