from fastapi import APIRouter

from schemas.status import StatusUpdate

from database.crud import (
    update_incident_status
)

router = APIRouter()


@router.patch(
    "/incidents/{incident_id}"
)
def update_status(
    incident_id: int,
    data: StatusUpdate
):

    incident = update_incident_status(
        incident_id,
        data.status
    )

    if not incident:

        return {
            "error": "Incident not found"
        }

    return {
        "message": "Status updated",
        "id": incident.id,
        "status": incident.status
    }