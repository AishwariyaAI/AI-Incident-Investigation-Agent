from groq import Groq
import os
from dotenv import load_dotenv

# -----------------------
# LOAD ENV VARIABLES
# -----------------------
load_dotenv()

# -----------------------
# INIT GROQ CLIENT
# -----------------------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------
# ROOT CAUSE ANALYZER
# -----------------------
def analyze_root_cause(sensor_values):

    causes = []

    if sensor_values[11] > 9040:
        causes.append(
            "High turbine pressure"
        )

    if sensor_values[16] > 8120:
        causes.append(
            "Compressor efficiency degradation"
        )

    if sensor_values[4] > 642:
        causes.append(
            "Engine temperature abnormal"
        )

    if not causes:
        causes.append(
            "No significant anomaly detected"
        )

    return causes