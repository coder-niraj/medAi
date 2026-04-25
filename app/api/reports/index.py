from typing import Any
from fastapi import HTTPException, Request
from helpers.audit import set_audit_state
from helpers.error_management import msg
from schemas.reportSchema import ReportDocumentResponse
from utils.cloud import StorageManager
from repository.reports.index import ReportRepo
from services.reports.index import ReportServices
from sqlalchemy.orm import Session
import magic


class ReportsController:

    def __init__(self, db: Session):
        self.report_repo = ReportRepo(db)
        self.report_storage = StorageManager()
        self.report_Service = ReportServices(self.report_repo, self.report_storage)

    async def get_all_reports(
        self, request: Request, user_data
    ) -> list[dict[str, Any]]:
        user_id = user_data.get("id")
        request.state.user_id = user_id
        return self.report_Service.get_list_reports(request, user_id)

    async def upload_doc_report(
        self,
        request: Request,
        file,
        report_type,
        display_name,
        user_data: dict,
    ) -> ReportDocumentResponse:
        user_id = user_data.get("id")
        request.state.user_id = user_id
        display_name = display_name.strip()[:100]
        try:
            MAX_SIZE = 10 * 1024 * 1024
            content = await file.read(MAX_SIZE + 1)
            if len(content) > MAX_SIZE:
                set_audit_state(
                    request,
                    action="UPLOAD",
                    resource_type="report",
                    outcome="FAILURE",
                    resource_id=None,
                )
                raise HTTPException(
                    400,
                    {
                        "message_ar": msg("errors", "file_too_large", "ar"),
                        "message_en": msg("errors", "file_too_large", "en"),
                    },
                )

            mime = magic.from_buffer(content, mime=True)
            allowed = ["application/pdf", "image/jpeg", "image/png"]

            if mime not in allowed:

                set_audit_state(
                    request,
                    action="UPLOAD",
                    resource_type="report",
                    outcome="FAILURE",
                    resource_id=None,
                )
                raise HTTPException(
                    400,
                    {
                        "message_ar": msg("errors", "invalid_file_type", "ar"),
                        "message_en": msg("errors", "invalid_file_type", "en"),
                    },
                )
            file_url = self.report_Service.save_file(
                content, display_name, report_type, user_id, mime
            )
            set_audit_state(
                request,
                action="UPLOAD",
                resource_type="report",
                outcome="SUCCESS",
                resource_id=file_url.report_id,
            )
            return file_url
        except HTTPException:
            raise
        except Exception as e:

            set_audit_state(
                request,
                action="UPLOAD",
                resource_type="report",
                outcome="FAILURE",
                resource_id=None,
            )
            raise HTTPException(
                500,
                {
                    "message_ar": msg("errors", "storage_failed", "ar"),
                    "message_en": msg("errors", "storage_failed", "en"),
                },
            )

    async def delete_report(
        self, request: Request, report_id, user_id
    ) -> dict[str, bool]:
        request.state.user_id = user_id
        return self.report_Service.delete_report(request, report_id, user_id)

    def ai_generated_summary_report(self):
        return "ai report"

    def short_lived_urls_in_app_doc_viewer(self, request: Request, report_id, user_id):
        request.state.user_id = user_id
        return self.report_Service.get_url_24_hours(request, report_id, user_id)
