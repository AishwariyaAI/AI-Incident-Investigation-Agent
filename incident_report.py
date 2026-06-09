from severity import get_severity
from root_cause import root_cause_analysis


def generate_incident_report(
    sensor_score,
    image_score,
    log_score
):

    fused_score = (
        sensor_score +
        image_score +
        log_score
    ) / 3

    severity = get_severity(
        fused_score
    )

    root_cause = root_cause_analysis(
        sensor_score,
        image_score,
        log_score
    )

    report = {
        "severity": severity,
        "root_cause": root_cause["root_cause"],
        "sensor_score": sensor_score,
        "image_score": image_score,
        "log_score": log_score,
        "fused_score": fused_score
    }

    return report
