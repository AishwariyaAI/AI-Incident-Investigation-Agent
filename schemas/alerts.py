def generate_alert(severity):
    if severity == "CRITICAL":
        return "🚨 CRITICAL INCIDENT DETECTED"
    elif severity == "HIGH":
        return "⚠ HIGH RISK ALERT"
    return "OK"