from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, status
from api.reports.index import ReportsController
from middlewares.idempotency import check_header_idempotency
from db.session import get_DB
from middlewares.consent_gate import consent_gate
from DTOs.reportSchema import ReportDelete, ReportType
from middlewares.rate_limiter import limiter

router = APIRouter(prefix="/reports")


def get_auth_controller(db: Session = Depends(get_DB)):
    return ReportsController(db)


def get_user_id_from_token(request: Request) -> str:
    return request.state.user_id


@router.get("/", status_code=status.HTTP_200_OK)
async def list_reports(
    request: Request,
    token_data: dict = Depends(consent_gate),
    controller: ReportsController = Depends(get_auth_controller),
):
    return await controller.get_all_reports(request, user_data=token_data)


@limiter.limit("5/day", key_func=get_user_id_from_token)
@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_report(
    request: Request,
    cached_response=Depends(check_header_idempotency),
    file: UploadFile = File(...),
    report_type: ReportType = Form(...),
    display_name: str = Form(...),
    token_data: dict = Depends(consent_gate),
    controller: ReportsController = Depends(get_auth_controller),
):
    if cached_response:
        return cached_response
    else:
        return await controller.upload_doc_report(
            request, file, report_type, display_name, token_data
        )


@router.get("/{report_id}/summary", status_code=status.HTTP_200_OK)
def get_report_summery():
    ReportsController.ai_generated_summary_report()


@router.get("/{report_id}/file", status_code=status.HTTP_200_OK)
def get_limited_time_url(
    request: Request,
    report_id: str,
    token_data: dict = Depends(consent_gate),
    controller: ReportsController = Depends(get_auth_controller),
):
    return controller.short_lived_urls_in_app_doc_viewer(
        request, report_id, token_data.get("id")
    )


@router.delete("/{report_id}", status_code=status.HTTP_200_OK)
async def delete_file(
    request: Request,
    report_id: str,
    token_data: dict = Depends(consent_gate),
    controller: ReportsController = Depends(get_auth_controller),
):
    return await controller.delete_report(request, report_id, token_data.get("id"))
