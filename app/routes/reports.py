from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from api.reports.index import ReportsController
from db.session import get_DB
from middlewares.index import get_current_user_gateway
from schemas.reportSchema import ReportDelete, ReportType

router = APIRouter(prefix="/reports")


def get_auth_controller(db: Session = Depends(get_DB)):
    return ReportsController(db)


@router.get("/")
async def list_reports(
    request: Request,
    token_data: dict = Depends(get_current_user_gateway),
    controller: ReportsController = Depends(get_auth_controller),
):
    return await controller.get_all_reports(request, user_data=token_data)


@router.post("/upload")
async def upload_report(
    request: Request,
    file: UploadFile = File(...),
    report_type: ReportType = Form(...),
    display_name: str = Form(...),
    token_data: dict = Depends(get_current_user_gateway),
    controller: ReportsController = Depends(get_auth_controller),
):
    return await controller.upload_doc_report(
        request, file, report_type, display_name, token_data
    )


@router.get("/{report_id}/summary")
def get_report_summery():
    ReportsController.ai_generated_summary_report()


@router.get("/{report_id}/file")
def get_limited_time_url(
    request: Request,
    report_id: str,
    token_data: dict = Depends(get_current_user_gateway),
    controller: ReportsController = Depends(get_auth_controller),
):
    return controller.short_lived_urls_in_app_doc_viewer(
        request, report_id, token_data.get("id")
    )


@router.delete("/{report_id}")
async def delete_file(
    request: Request,
    report_id: str,
    token_data: dict = Depends(get_current_user_gateway),
    controller: ReportsController = Depends(get_auth_controller),
):
    return await controller.delete_report(request, report_id, token_data.get("id"))
