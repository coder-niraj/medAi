from fastapi import APIRouter

from api.internal.index import InternalController
from services.seeding.index import run_all_seeds
from tasks.ft_curation_job import run
from tasks.cleanup_job import run as guest_run
from services.seeding.index import run_all_seeds

router = APIRouter(prefix="/internal")

# router.delete("/traces/{message_id}")(InternalController.llm_traces)


@router.post("/ft-pipeline/run")
def run_all():
    run_all_seeds()
    run()
    guest_run()


# router.get("/ft-pipeline/stats")(InternalController.check_pipeline_health)
