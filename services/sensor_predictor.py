import joblib

model = joblib.load(
    "models/sensor_model.pkl"
)

def predict_sensor_score(sensor_values):

    score = model.decision_function(
        [sensor_values]
    )[0]

    normalized = 1 - (
        (score + 0.5) / 1.0
    )

    return round(
        max(0, min(1, normalized)),
        3
    )