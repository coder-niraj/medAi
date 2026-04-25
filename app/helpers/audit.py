from fastapi import Request


def set_audit_state(
    request: Request,
    action: str,
    resource_type: str,
    outcome: str,
    resource_id=None,
):
    request.state.resource_id = resource_id
    request.state.resource_type = resource_type
    request.state.action = action
    request.state.outcome = outcome
