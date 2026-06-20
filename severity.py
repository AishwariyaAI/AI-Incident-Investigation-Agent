def classify_severity(confidence):

    if confidence < 0.25:
        return "LOW"

    elif confidence < 0.50:
        return "MEDIUM"

    elif confidence < 0.75:
        return "HIGH"

    else:
        return "CRITICAL"