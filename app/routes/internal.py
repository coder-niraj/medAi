from fastapi import APIRouter

from api.internal.index import InternalController
router = APIRouter(prefix="/internal")

router.delete("/traces/{message_id}")(InternalController.llm_traces)
router.post("/ft-pipeline/run")(InternalController.trigger_night_pipeline)
router.get("/ft-pipeline/stats")(InternalController.check_pipeline_health)
