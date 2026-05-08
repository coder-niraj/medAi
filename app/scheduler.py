from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta, timezone
from tasks.cleanup_job import run as clean_run
from tasks.doc_retention import run as doc_run
from tasks.ft_curation_job import run as finetune_run
from tasks.trace_retention_job import run as trace_run

scheduler = BlockingScheduler(timezone="UTC")

scheduler.add_job(
    clean_run,
    trigger="cron",
    hour="*/6",
    replace_existing=True,
    id="guest-cleanup",
)

scheduler.add_job(
    doc_run,
    trigger="cron",
    hour=3,
    minute=0,
    id="report-cleanup",
    replace_existing=True,
)

scheduler.add_job(
    finetune_run,
    trigger="cron",
    hour=2,
    minute=0,
    id="finetune-job",
    replace_existing=True,
)


scheduler.start()
