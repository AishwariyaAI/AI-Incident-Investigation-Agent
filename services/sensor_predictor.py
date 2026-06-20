import joblib
import numpy as np

model = joblib.load("ml/model.pkl")
scaler = joblib.load("ml/scaler.pkl")


def predict_sensor(sensor_values):
    X = np.array(sensor_values).reshape(1, -1)

    X_scaled = scaler.transform(X)

    prediction = model.predict(X_scaled)[0]

    probabilities = model.predict_proba(X_scaled)[0]

    confidence = float(max(probabilities))
    anomaly_score = float(probabilities[prediction])

    return prediction, confidence, anomaly_score