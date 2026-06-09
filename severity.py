def get_severity(score):

    if score >= 0.95:
        return "CRITICAL"

    elif score >= 0.85:
        return "HIGH"

    elif score >= 0.70:
        return "MEDIUM"

    return "LOW"