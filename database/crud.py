from database.db import SessionLocal
from database.models import Incident


# ----------------------------
# CREATE INCIDENT
# ----------------------------
def create_incident(score, prediction, severity, status="OPEN"):

    db = SessionLocal()

    incident = Incident(
        score=score,
        prediction=prediction,
        severity=severity,
        status=status
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    db.close()

    return incident


# ----------------------------
# GET ALL INCIDENTS
# ----------------------------
def get_incidents():

    db = SessionLocal()

    data = db.query(Incident).all()

    db.close()

    return data


# ----------------------------
# UPDATE STATUS (LIFECYCLE)
# ----------------------------
def update_incident_status(incident_id, status):

    db = SessionLocal()

    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        db.close()
        return None

    incident.status = status

    db.commit()
    db.refresh(incident)

    db.close()

    return incident