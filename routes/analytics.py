from fastapi import APIRouter
from database.db import SessionLocal
from database.models import Incident

router = APIRouter()

# =========================
# ANOMALY TREND
# =========================
@router.get("/anomaly-trend")
def anomaly_trend():
    db = SessionLocal()

    data = db.query(Incident).order_by(Incident.id).all()

    trend = [
        {
            "cycle": d.cycle,
            "anomaly_score": float(d.anomaly_score)
        }
        for d in data[-50:]
    ]

    db.close()
    return trend


# =========================
# SEVERITY PIE
# =========================
@router.get("/severity-pie")
def severity_pie():
    db = SessionLocal()

    incidents = db.query(Incident).all()

    result = {
        "LOW 🟢": 0,
        "MEDIUM 🟡": 0,
        "HIGH 🟠": 0,
        "CRITICAL 🔴": 0
    }

    for i in incidents:
        if "LOW" in i.severity:
            result["LOW 🟢"] += 1
        elif "MEDIUM" in i.severity:
            result["MEDIUM 🟡"] += 1
        elif "HIGH" in i.severity:
            result["HIGH 🟠"] += 1
        elif "CRITICAL" in i.severity:
            result["CRITICAL 🔴"] += 1

    db.close()
    return result

@router.get("/incident-lifecycle")
def incident_lifecycle():

    db = SessionLocal()

    incidents = db.query(Incident).all()

    result = {
        "OPEN": 0,
        "ACK": 0,
        "RESOLVED": 0
    }

    for incident in incidents:

        status = incident.status

        if status in result:
            result[status] += 1

    db.close()

    return result

@router.get("/incident-timeline")
def incident_timeline():

    db = SessionLocal()

    incidents = (
        db.query(Incident)
        .order_by(Incident.id.desc())
        .limit(20)
        .all()
    )

    result = []

    for i in incidents:

        result.append({
            "incident_id": i.id,
            "status": i.status,
            "severity": i.severity,
            "timestamp": str(i.timestamp)
        })

    db.close()

    return result

    