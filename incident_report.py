def generate_incident_report(incident_id, score, prediction, severity):

    return {
        "incident_id": incident_id,
        "score": score,
        "prediction": prediction,
        "severity": severity,
        "status": "OPEN"
    }