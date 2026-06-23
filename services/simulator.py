import pandas as pd
import random

df = pd.read_csv(
    "ml/train_FD001.txt",
    sep=r"\s+",
    header=None
)

def get_random_sensor():
    row = df.sample(1).iloc[0]

    return {
        "engine_id": int(row[0]),
        "cycle": int(row[1]),
        "sensor_values":
            row[2:26]
            .astype(float)
            .tolist()
    }