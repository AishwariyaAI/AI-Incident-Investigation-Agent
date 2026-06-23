import numpy as np
import joblib

model = joblib.load("ml/model.pkl")
scaler = joblib.load("ml/scaler.pkl")


def predict_sensor(sensor_values):

    X = np.array(sensor_values).reshape(1, -1)

    print("Features Length:", len(sensor_values))

    X_scaled = scaler.transform(X)
    print("Features Length:", len(sensor_values))
    print("Scaler expects:", scaler.n_features_in_)

    prediction = model.predict(X_scaled)[0]

    confidence = max(
        model.predict_proba(X_scaled)[0]
    )

    anomaly_score = confidence

    return (
        int(prediction),
        float(confidence),
        float(anomaly_score)
    )