def generate_alert(severity):

    if "CRITICAL" in severity:
        return "🚨 Critical Failure Predicted"

    elif "HIGH" in severity:
        return "⚠️ High Risk Engine"

    else:
        return "✅ Engine Healthy"