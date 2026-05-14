from fastapi import APIRouter, Depends, Request
from api.triage.index import TriageController
from DTOs.triageSchema import TriageClaim
from db.session import get_DB
from middlewares.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/triage")


def get_auth_controller(db: Session = Depends(get_DB)):
    return TriageController(db)


# router.post("/complete/{session_id}")(TriageController.triage_result)
@router.post("/claim")
def claim(
    request: Request,
    body: TriageClaim,
    token_data: dict = Depends(get_current_user),
    controller: TriageController = Depends(get_auth_controller),
):
    return controller.triage_guest_token_claim(request, token_data, body)


# router.get("/results/{triage_result_id}")(TriageController.specific_triage_result)
# router.get("/results")(TriageController.all_triage_results)
# router.patch("/sessions/{session_id}/messages/{message_id}/feedback")(
#     TriageController.rating_flag
# )
