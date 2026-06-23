from fastapi import APIRouter
from database.db import SessionLocal
from database.models import Incident

router = APIRouter()

@router.get("/engine-health-map")
def engine_health_map():

    db = SessionLocal()

    incidents = (
        db.query(Incident)
        .order_by(Incident.id.desc())
        .all()
    )

    latest_engines = {}
    result = []

    for i in incidents:

        # Skip if engine already processed
        if i.engine_id in latest_engines:
            continue

        latest_engines[i.engine_id] = True

        if "LOW" in str(i.severity):
            status = "Healthy"

        elif "MEDIUM" in str(i.severity):
            status = "Monitor"

        elif "HIGH" in str(i.severity):
            status = "High Risk"

        elif "CRITICAL" in str(i.severity):
            status = "Critical"

        else:
            status = "Unknown"

        result.append({
            "engine": i.engine_id,
            "severity": i.severity,
            "status": status
        })

    db.close()

    return result