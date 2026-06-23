def get_root_cause(
    severity,
    confidence,
    anomaly_score
):

    prompt = f"""
Prediction={severity}
Confidence={confidence}
Anomaly Score={anomaly_score}

Explain probable root cause.
"""

    if severity == "CRITICAL":

        return (
            "Severe degradation detected. "
            "High vibration and temperature "
            "indicate possible engine failure."
        )

    elif severity == "HIGH":

        return (
            "Sensor drift detected. "
            "Possible maintenance required."
        )

    return (
        "Engine operating normally."
    )