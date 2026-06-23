def ai_root_cause(prediction):

    if prediction == 2:

        return """
Engine Failure Predicted

Likely Cause:
High turbine temperature

Recommendation:
Inspect cooling system immediately.
"""

    elif prediction == 1:

        return """
Engine Risk Detected

Likely Cause:
Abnormal vibration trend

Recommendation:
Schedule maintenance.
"""

    return """
Engine Healthy

Likely Cause:
No anomaly detected

Recommendation:
Continue monitoring.
"""