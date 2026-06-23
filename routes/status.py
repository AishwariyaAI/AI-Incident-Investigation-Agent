# routes/status.py

from fastapi import APIRouter
from database.db import SessionLocal
from database.models import Incident

router = APIRouter()

@router.patch("/incident/{id}/ack")
def ack(id: int):

    db = SessionLocal()

    incident = db.query(Incident).filter(
        Incident.id == id
    ).first()

    if not incident:
        return {"error": "Incident not found"}

    incident.status = "ACK"

    db.commit()
    db.close()

    return {"message": "ACKNOWLEDGED"}


@router.patch("/incident/{id}/resolve")
def resolve(id: int):

    db = SessionLocal()

    incident = db.query(Incident).filter(
        Incident.id == id
    ).first()

    if not incident:
        return {"error": "Incident not found"}

    incident.status = "RESOLVED"

    db.commit()
    db.close()

    return {"message": "RESOLVED"}