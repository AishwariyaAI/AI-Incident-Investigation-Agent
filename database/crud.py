from database.db import SessionLocal
from database.models import Incident

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_incident(
    score,
    confidence,
    prediction,
    severity,
    status="OPEN"
):

    db = SessionLocal()

    incident = Incident(
        score=score,
        confidence=confidence,
        prediction=prediction,
        severity=severity,
        status=status
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    db.close()

    return incident

def get_incidents(db):

    incidents = db.query(
        Incident
    ).all()

    result = []

    for i in incidents:

        result.append({
            "id": i.id,
            "engine_id": i.engine_id,
            "cycle": i.cycle,
            "prediction": i.prediction,
            "confidence": i.confidence,
            "anomaly_score": i.anomaly_score,
            "severity": i.severity,
            "status": i.status,
            "timestamp": str(i.timestamp)
        })

    return result

        
        
def update_incident_status(
    incident_id,
    status
):

    db = SessionLocal()

    incident = db.query(
        Incident
    ).filter(
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