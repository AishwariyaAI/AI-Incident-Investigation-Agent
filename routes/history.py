from fastapi import APIRouter
from schemas.incident import StatusUpdate
from database.crud import get_incidents, update_incident_status

router = APIRouter()


@router.get("/incidents")
def read_incidents():
    return get_incidents()


@router.patch("/incidents/{incident_id}")
def update_status(incident_id: int, data: StatusUpdate):

    updated = update_incident_status(
        incident_id,
        data.status
    )

    if not updated:
        return {"error": "Incident not found"}

    return {
        "message": "Status updated",
        "id": updated.id,
        "status": updated.status
    }