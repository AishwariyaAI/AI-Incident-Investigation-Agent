import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest

cols = (
    ["engine_id", "cycle"]
    + [f"op{i}" for i in range(1,4)]
    + [f"s{i}" for i in range(1,22)]
)

df = pd.read_csv(
    "data/train_FD001.txt",
    sep=r"\s+",
    header=None
)

df = df.iloc[:, :26]
df.columns = cols

X = df[[f"s{i}" for i in range(1,22)]]

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(X)

joblib.dump(
    model,
    "models/sensor_model.pkl"
)

print("Model Trained")