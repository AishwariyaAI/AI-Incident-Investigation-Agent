def generate_alert(severity: str):
    if severity == "CRITICAL":
        return "🚨 CRITICAL INCIDENT DETECTED"
    elif severity == "HIGH":
        return "⚠️ HIGH RISK INCIDENT"
    elif severity == "MEDIUM":
        return "⚡ MEDIUM ALERT"
    else:
        return "✅ Normal Activity"