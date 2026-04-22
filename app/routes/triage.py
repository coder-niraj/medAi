from fastapi import APIRouter
from api.triage.index import TriageController

router = APIRouter(prefix="/triage")

router.post("/complete/{session_id}")(TriageController.triage_result)
router.post("/claim")(TriageController.triage_token_claim)
router.get("/results/{triage_result_id}")(TriageController.specific_triage_result)
router.get("/results")(TriageController.all_triage_results)
router.patch("/sessions/{session_id}/messages/{message_id}/feedback")(TriageController.rating_flag)
