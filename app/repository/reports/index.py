import datetime
from datetime import timedelta, timezone, datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.reportSchema import report_list
from models.reports import Report
from utils.cloud import StorageManager


class ReportRepo:
    def __init__(self, db: Session):
        self.db = db

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
        self.db.commit()
        self.db.refresh(report_data)
        return report_data

    def get_list_of_all_reports(self, user_id):
        try:
            all_reports = self.db.query(Report).filter(Report.user_id == user_id).all()
            return report_list(all_reports)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Database transaction failed")

    def get_report_by_id():
        print("report by id")

    def delete_report_by_id(self, report_id, user_id):
        try:
            storage = StorageManager()
            report_obj = self.db.query(Report).filter(Report.id == report_id).first()
            storage.delete_file(report=report_obj)
            self.db.query(Report).filter(Report.id == report_obj.id).delete()
            return "deleted"
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Database transaction failed")
