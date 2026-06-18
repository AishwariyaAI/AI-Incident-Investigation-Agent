from fastapi import APIRouter, Depends

from schemas.request import InputData
from severity import classify_severity
from utils.alerts import generate_alert
from services.notifier import manager
from database.crud import create_incident
from utils.security import get_current_user
from root_cause import analyze_root_cause

router = APIRouter()


@router.post("/detect")
async def detect(
    data: InputData,
    user: str = Depends(get_current_user)
):

    # ===================================
    # REALISTIC NASA ANOMALY SCORE
    # ===================================

    sensors = data.sensor_values

    normalized = []

    for value in sensors:

        score = abs(value)

        if score > 1000:
            score = score / 10000

        elif score > 100:
            score = score / 1000

        else:
            score = score / 100

        normalized.append(score)

    sensor_score = sum(normalized) / len(normalized)

    if sensor_score > 1:
        sensor_score = 1.0

    # ===================================
    # PREDICTION
    # ===================================

    prediction = 1 if sensor_score > 0.55 else 0

    # ===================================
    # SEVERITY
    # ===================================

    severity = classify_severity(sensor_score)

    # ===================================
    # ROOT CAUSE
    # ===================================

    root_causes = analyze_root_cause(sensors)

    # ===================================
    # AUTO INCIDENT LIFECYCLE
    # ===================================

    if severity == "LOW":
        auto_status = "OPEN"

    elif severity == "MEDIUM":
        auto_status = "ACK"

    elif severity == "HIGH":
        auto_status = "RESOLVED"

    else:
        auto_status = "RESOLVED"

    # ===================================
    # SAVE INCIDENT
    # ===================================

    create_incident(
        score=sensor_score,
        prediction=prediction,
        severity=severity,
        status=auto_status
    )

    # ===================================
    # INCIDENT REPORT
    # ===================================

    report = {
        "incident_id": 0,
        "score": round(sensor_score, 4),
        "prediction": prediction,
        "severity": severity,
        "status": auto_status
    }

    # ===================================
    # ALERT
    # ===================================

    alert = generate_alert(severity)

    await manager.send_alert({
        "type": "INCIDENT_ALERT",
        "severity": severity,
        "message": alert
    })

    # ===================================
    # RESPONSE
    # ===================================

    return {
        "sensor_score": round(sensor_score, 4),
        "prediction": prediction,
        "severity": severity,
        "root_causes": root_causes,
        "incident_report": report,
        "alert": alert
    }