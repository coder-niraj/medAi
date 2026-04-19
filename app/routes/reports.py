from fastapi import APIRouter
from app.api.reports.index import ReportsController

router = APIRouter(prefix="/reports")

router.get("/")(ReportsController.get_all_reports)
router.post("/upload")(ReportsController.upload_doc_report)
router.get("/{report_id}/summary")(ReportsController.ai_generated_summary_report)
router.get("/{report_id}/file")(ReportsController.short_lived_urls_in_app_doc_viewer)
router.delete("/{report_id}")(ReportsController.delete_report)
