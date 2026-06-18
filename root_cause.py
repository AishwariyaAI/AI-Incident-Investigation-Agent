def analyze_root_cause(sensor_values):

    if max(sensor_values) > 9000:
        return ["High turbine pressure detected"]

    if sensor_values[0] < 520:
        return ["Low inlet pressure anomaly"]

    return ["No significant root cause detected"]