import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# NASA train data
df = pd.read_csv(
    "data/train_FD001.txt",
    sep=r"\s+",
    header=None
)

df = df.dropna(axis=1)

# NASA sensors
X = df.iloc[:, 2:26]

# Simple anomaly label
threshold = X.mean(axis=1)

y = (threshold > threshold.median()).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

print(
    "Accuracy:",
    model.score(X_test, y_test)
)

joblib.dump(
    model,
    "models/sensor_model.pkl"
)

print("Model Saved")