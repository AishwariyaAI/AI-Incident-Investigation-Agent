def root_cause_analysis(
    sensor_score,
    image_score,
    log_score
):

    scores = {
        "Sensor": sensor_score,
        "Image": image_score,
        "Log": log_score
    }

    dominant = max(
        scores,
        key=scores.get
    )

    return {
        "root_cause": dominant,
        "scores": scores
    }