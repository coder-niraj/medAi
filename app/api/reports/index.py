from fastapi import Depends, HTTPException, status
from httpx import get

from utils.cloud import StorageManager
from db.session import get_DB
from repository.reports.index import ReportRepo
from services.reports.index import ReportServices
from sqlalchemy.orm import Session


class ReportsController:

    def __init__(self, db: Session = Depends(get_DB)):
        self.report_repo = ReportRepo(db)
        self.report_storage = StorageManager()
        self.report_Service = ReportServices(self.report_repo, self.report_storage)

    async def get_all_reports(self, user_data):
        return self.report_Service.get_list_reports(user_data.get("id"))

    async def upload_doc_report(
        self, file, report_type, display_name, user_data: dict, mime_type
    ):
        user_type = user_data.get("type")
        triage_count = user_data.get("triage_count", 0)
        user_id = user_data.get("id")
        if not user_data.get("consent_given_at"):
            raise HTTPException(403, "consent_required")
        try:
            MAX_SIZE = 10 * 1024 * 1024
            content = await file.read(MAX_SIZE + 1)
            if len(content) > MAX_SIZE:
                raise HTTPException(400, "invalid_file_type | file_too_large")
            content_type = file.content_type
            file_url = self.report_Service.save_file(
                content, display_name, report_type, user_id, content_type, mime_type
            )
            return file_url
        except Exception as e:
            raise HTTPException(500, "Failed to save report to storage.")

    def ai_generated_summary_report(self):
        return "ai report"

    def short_lived_urls_in_app_doc_viewer(self):
        return "urls"

    async def delete_report(self, report_id, user_id):
        return self.report_Service.delete_report(report_id, user_id)
