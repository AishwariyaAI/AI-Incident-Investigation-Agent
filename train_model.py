import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest

# NASA dataset
df = pd.read_csv(
    "data/train_FD001.txt",
    sep=r"\s+",
    header=None
)

df = df.dropna(axis=1, how="all")

# Sensor columns
X = df.iloc[:, 2:]

# Train anomaly model
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(X)

joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")