from fastapi import APIRouter, Depends

from utils.security import get_current_user

from services.sensor_predictor import predict_sensor
from services.notifier import generate_alert
from services.root_cause_ai import ai_root_cause
from services.alerts import add_alert

from models.schemas import SensorInput

from database.db import SessionLocal
from database.models import Incident

router = APIRouter()


def map_severity(prediction, confidence):

    if prediction == 2:
        return "CRITICAL 🔴"

    elif prediction == 1:
        return "HIGH 🟠"

    else:
        return "LOW 🟢"


def get_root_cause(prediction, sensor_values):

    sensor_7 = sensor_values[7]
    sensor_11 = sensor_values[11]

    if sensor_11 > 80:
        return "High vibration detected"

    elif sensor_7 > 80:
        return "Temperature spike detected"

    elif prediction == 2:
        return "Possible engine degradation"

    else:
        return "System operating normally"


@router.post("/detect")
def detect(
    data: SensorInput,
    user=Depends(get_current_user)
):

    prediction, confidence, anomaly_score = predict_sensor(
        data.sensor_values
    )

    severity = map_severity(
        prediction,
        confidence
    )

    root_cause = get_root_cause(
        prediction,
        data.sensor_values
    )

    alert = generate_alert(
        severity
    )
    print("ALERT GENERATED:", alert)

    add_alert(alert)

    print("ALERT ADDED")

    add_alert(alert)
    print("ALERT ADDED")
    ai_report = ai_root_cause(
        prediction
    )

    db = SessionLocal()

    incident = Incident(
        engine_id=data.engine_id,
        cycle=data.cycle,
        prediction=int(prediction),
        confidence=float(confidence),
        anomaly_score=float(anomaly_score),
        severity=severity,
        status="OPEN"
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    incident_id = incident.id

    report = f"""
Incident ID: {incident_id}

Severity: {severity}

Root Cause:
{root_cause}

Recommendation:
Inspect turbine bearings
"""

    db.close()

    return {
        "incident_id": incident_id,
        "prediction": int(prediction),
        "confidence": float(confidence),
        "anomaly_score": float(anomaly_score),
        "severity": severity,
        "root_cause": root_cause,
        "status": "OPEN",
        "alert": alert,
        "ai_report": ai_report,
        "report": report
    }