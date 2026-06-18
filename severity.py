def classify_severity(score):

    if score < 0.30:
        return "LOW"

    elif score < 0.50:
        return "MEDIUM"

    elif score < 0.70:
        return "HIGH"

    else:
        return "CRITICAL"