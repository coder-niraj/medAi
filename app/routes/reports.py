from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, UploadFile
from api.reports.index import ReportsController
from db.session import get_DB
from helpers.index import get_current_user_gateway
from schemas.reportSchema import ReportDelete, ReportType

router = APIRouter(prefix="/reports")


def get_auth_controller(db: Session = Depends(get_DB)):
    return ReportsController(db)


@router.get("/")
async def list_reports(
    token_data: dict = Depends(get_current_user_gateway),
    controller: ReportsController = Depends(get_auth_controller),
):
    return await controller.get_all_reports(user_data=token_data)


@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    report_type: ReportType = Form(...),
    display_name: str = Form(...),
    token_data: dict = Depends(get_current_user_gateway),
    controller: ReportsController = Depends(get_auth_controller),
):
    mime_type = file.content_type
    return await controller.upload_doc_report(
        file, report_type, display_name, token_data, mime_type
    )


@router.get("/{report_id}/summary")
def get_report_summery():
    ReportsController.ai_generated_summary_report()


@router.get("/{report_id}/file")
def get_limited_time_url():
    ReportsController.short_lived_urls_in_app_doc_viewer()


@router.delete("/{report_id}")
async def delete_file(
    report_id: str,
    token_data: dict = Depends(get_current_user_gateway),
    controller: ReportsController = Depends(get_auth_controller),
):
    return await controller.delete_report(report_id, token_data.get("id"))
