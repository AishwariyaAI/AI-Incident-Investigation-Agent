from fastapi import APIRouter, Depends
from utils.security import get_current_user
from services.sensor_predictor import predict_sensor
from models.schemas import SensorInput

from database.db import SessionLocal
from database.models import Incident

router = APIRouter()


# ==========================================
# SEVERITY MAPPING
# ==========================================
def map_severity(prediction, confidence):

    if prediction == 2:
        return "CRITICAL 🔴"

    elif prediction == 1:
        return "HIGH 🟠"

    elif confidence > 0.85:
        return "MEDIUM 🟡"

    else:
        return "LOW 🟢"


# ==========================================
# ROOT CAUSE ANALYSIS
# ==========================================
def get_root_cause(severity):

    if "CRITICAL" in severity:
        return "High turbine pressure detected"

    elif "HIGH" in severity:
        return "Abnormal vibration detected"

    elif "MEDIUM" in severity:
        return "Sensor drift detected"

    else:
        return "System operating normally"


# ==========================================
# DETECT INCIDENT
# ==========================================
@router.post("/detect")
def detect(
    data: SensorInput,
    user=Depends(get_current_user)
):

    prediction, confidence, anomaly_score = predict_sensor(
        data.sensor_values
    )

    print("Prediction:", prediction)
    print("Confidence:", confidence)
    print("Anomaly Score:", anomaly_score)

    severity = map_severity(
        prediction,
        confidence
    )

    root_cause = get_root_cause(
        severity
    )

    db = SessionLocal()

    incident = Incident(
        engine_id=getattr(data, "engine_id", 1),
        cycle=getattr(data, "cycle", 1),
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

    db.close()

    return {
        "user": user,
        "incident_id": incident_id,
        "prediction": int(prediction),
        "confidence": float(confidence),
        "anomaly_score": float(anomaly_score),
        "severity": severity,
        "root_cause": root_cause,
        "status": "OPEN",
        "alert": f"{severity} INCIDENT DETECTED"
    }