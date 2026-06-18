import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

# -----------------------
# TRAIN MODEL (FAKE DATA)
# -----------------------
def train_model():
    # normal + abnormal synthetic data
    X = np.array([
        [0.1], [0.2], [0.15], [0.3], [0.25],
        [0.8], [0.9], [0.85], [0.95]
    ])

    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit(X)

    joblib.dump(model, "anomaly_model.pkl")
    return model


# -----------------------
# LOAD MODEL
# -----------------------
def load_model():
    try:
        model = joblib.load("anomaly_model.pkl")
    except:
        model = train_model()
    return model


# -----------------------
# PREDICT
# -----------------------
def predict_scores(scores):
    model = load_model()

    data = np.array(scores).reshape(-1, 1)
    preds = model.predict(data)

    # convert:
    # -1 = anomaly, 1 = normal
    return [1 if p == -1 else 0 for p in preds]