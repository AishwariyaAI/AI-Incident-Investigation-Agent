def fuse_scores(sensor_scores, image_scores, log_scores):

    fused = []

    max_len = max(len(sensor_scores), len(image_scores), len(log_scores))

    for i in range(max_len):

        s = sensor_scores[i] if i < len(sensor_scores) else 0
        im = image_scores[i] if i < len(image_scores) else 0
        l = log_scores[i] if i < len(log_scores) else 0

        score = (0.4 * s) + (0.3 * im) + (0.3 * l)

        fused.append(score)

    return fused