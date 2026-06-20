import pandas as pd
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# ==========================================
# CONFIG
# ==========================================

DATA_PATH = "ml/train_FD001.txt"

COLUMNS = [
    "engine_id",
    "cycle",
    "op1",
    "op2",
    "op3"
] + [f"s{i}" for i in range(1, 22)]

# ==========================================
# LOAD NASA DATA
# ==========================================

print("Loading NASA FD001 dataset...")

df = pd.read_csv(
    DATA_PATH,
    sep=r"\s+",
    header=None
)

df.columns = COLUMNS

print("Rows:", len(df))

# ==========================================
# COMPUTE RUL
# ==========================================

max_cycle = (
    df.groupby("engine_id")["cycle"]
    .max()
    .reset_index()
)

max_cycle.columns = [
    "engine_id",
    "max_cycle"
]

df = df.merge(
    max_cycle,
    on="engine_id"
)

df["RUL"] = (
    df["max_cycle"]
    - df["cycle"]
)

# ==========================================
# LABEL CREATION
# ==========================================

def label_rul(rul):

    if rul <= 15:
        return 2      # CRITICAL

    elif rul <= 30:
        return 1      # HIGH

    else:
        return 0      # HEALTHY


df["label"] = df["RUL"].apply(label_rul)

print("\nLabel Distribution")
print(df["label"].value_counts())

print("\nLabel Percentage")
print(
    round(
        df["label"]
        .value_counts(normalize=True) * 100,
        2
    )
)

# ==========================================
# FEATURES
# ==========================================

feature_cols = [
    "op1",
    "op2",
    "op3"
] + [f"s{i}" for i in range(1, 22)]

X = df[feature_cols]
y = df["label"]

print("\nFeatures:", len(feature_cols))

# ==========================================
# SCALING
# ==========================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ==========================================
# RANDOM FOREST MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

print("\nTraining model...")

model.fit(
    X_scaled,
    y
)

# ==========================================
# TRAIN REPORT
# ==========================================

preds = model.predict(X_scaled)

print("\nClassification Report")
print(
    classification_report(
        y,
        preds
    )
)

print("\nModel Classes")
print(model.classes_)

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    "ml/model.pkl"
)

joblib.dump(
    scaler,
    "ml/scaler.pkl"
)

print("\nModel Saved")
print("ml/model.pkl")
print("ml/scaler.pkl")

# ==========================================
# SAMPLE CHECKS
# ==========================================

sample_rows = [
    0,
    100,
    500,
    1000
]

print("\nSample Predictions")

for r in sample_rows:

    if r < len(df):

        sample = X.iloc[r:r+1]

        sample_scaled = scaler.transform(sample)

        pred = model.predict(sample_scaled)[0]

        probs = model.predict_proba(sample_scaled)[0]

        print(
            f"Row={r}  "
            f"Prediction={pred}  "
            f"Confidence={max(probs):.4f}"
        )

        print("\nFailure Zone Predictions")

for r in [19000, 19500, 20000, 20500, 20600]:

    sample = X.iloc[r:r+1]

    sample_scaled = scaler.transform(sample)

    pred = model.predict(sample_scaled)[0]

    probs = model.predict_proba(sample_scaled)[0]

    print(
        f"Row={r} "
        f"Prediction={pred} "
        f"Confidence={max(probs):.4f}"
    )