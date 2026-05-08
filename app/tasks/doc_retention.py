from repository.reports.index import ReportRepo
from db.session import sessionLocal


def run():
    db = sessionLocal()
    report_repo = ReportRepo(db)
    print("Starting cleanup job...")
    old_reports = report_repo.get_2_year_old_reports(limit=500)
    success = 0
    failed = 0
    for report_obj in old_reports:
        try:
            report_repo.delete_report(report_obj)
            success += 1
        except Exception as e:
            failed += 1
            print(f"[FAILED] report_id={report_obj.id}, error={e}")
    print(f"✅ Success: {success}, ❌ Failed: {failed}")
    db.close()
