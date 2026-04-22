import uuid

from repository.reports.index import ReportRepo
from fastapi import File, HTTPException, status
from utils.firebase import verify_token
from schemas.reportSchema import ReportSchema
from utils.cloud import StorageManager


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

    def save_file(
        self, file_bytes, display_name, report_type, user_id, content_type, mime_type
    ):
        extension_map = {
            "application/pdf": ".pdf",
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/png": ".png",
        }
        ext = extension_map.get(mime_type, "")
        file_name = f"{uuid.uuid4()}{ext}"
        file_url = self.storage.upload_file(file_bytes, file_name, content_type)
        report_data = self.report_repo.save_document_data_to_table(
            file_url, user_id, display_name, report_type, mime_type
        )
        if self.is_Image(mime_type):
            return {
                "report_id": report_data.id,
                "status": "image_only",
                "message": "Image stored. Please also upload the written report from your radiologist for AI explanation.",
            }
        else:
            return {"report_id": report_data.id, "status": "uploaded"}

    def get_list_reports(self, user_id):
        return self.report_repo.get_list_of_all_reports(user_id)

    def delete_report(self, report_id, user_id):
        return self.report_repo.delete_report_by_id(report_id, user_id)
