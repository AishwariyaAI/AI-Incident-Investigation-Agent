import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# CONFIG
# ==================================================
st.set_page_config(
    page_title="AI Incident Monitoring Center",
    layout="wide"
)

API_URL = "http://127.0.0.1:8001/api/v1"

# ==================================================
# SESSION INIT
# ==================================================
if "token" not in st.session_state:
    st.session_state.token = None

# ==================================================
# LOGIN SYSTEM
# ==================================================
if not st.session_state.token:

    st.title("🔐 AI Incident Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        try:
            res = requests.post(
                f"{API_URL}/login",
                json={"username": username, "password": password}
            )

            data = res.json()

            if "access_token" in data:
                st.session_state.token = data["access_token"]
                st.success("Login successful")
                st.rerun()
            else:
                st.error(data.get("error", "Invalid login"))

        except Exception as e:
            st.error(f"Backend error: {e}")

    st.stop()


# ==================================================
# HEADER
# ==================================================
st.title("🚨 AI Incident Monitoring Center")
st.caption("NASA Sensor + AI Incident Detection System")

headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}

# ==================================================
# LOAD DATASET (FIXED NASA INDEXING)
# ==================================================
try:
    df = pd.read_csv("data/test_FD001.txt", sep=r"\s+", header=None)
    df = df.dropna().reset_index(drop=True)

    SENSOR_START = 2
    SENSOR_END = 26

except Exception as e:
    st.error(f"Dataset error: {e}")
    st.stop()

# ==================================================
# ENGINE SELECTION
# ==================================================
st.subheader("NASA Engine Data")

row_id = st.number_input("Select Engine Row", 0, len(df) - 1, 0)

row = df.iloc[row_id]

engine_id = int(row.iloc[0])
cycle = int(row.iloc[1])

sensor_values = row.iloc[SENSOR_START:SENSOR_END].astype(float).tolist()

col1, col2 = st.columns(2)
col1.metric("Engine ID", engine_id)
col2.metric("Cycle", cycle)

st.subheader("Sensor Values")
st.json(sensor_values)

# ==================================================
# RUN DETECTION
# ==================================================
if st.button("🚀 Run Incident Detection"):

    try:
        res = requests.post(
            f"{API_URL}/detect",
            json={"sensor_values": sensor_values},
            headers=headers
        )

        result = res.json()

        st.success("Detection Complete")

        # SAFE KEYS (backend mismatch fix)
        score = result.get("sensor_score") or result.get("score") or 0
        prediction = result.get("prediction", 0)
        severity = result.get("severity", "LOW")

        # ==================================================
        # METRICS
        # ==================================================
        c1, c2, c3 = st.columns(3)

        c1.metric("Anomaly Score", round(float(score), 4))
        c2.metric("Prediction", prediction)
        c3.metric("Severity", severity)

        # ==================================================
        # GAUGE (SAFE NORMALIZATION)
        # ==================================================
        st.subheader("Anomaly Score Gauge")

        safe_score = float(score)

        # clamp extreme values (IMPORTANT FIX)
        if safe_score > 1:
            safe_score = 1.0
        if safe_score < 0:
            safe_score = 0.0

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=safe_score,
                gauge={
                    "axis": {"range": [0, 1]},
                    "bar": {"color": "red"}
                }
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        # ==================================================
        # SEVERITY
        # ==================================================
        st.subheader("Severity Status")

        if severity == "CRITICAL":
            st.error(severity)
        elif severity == "HIGH":
            st.warning(severity)
        elif severity == "MEDIUM":
            st.info(severity)
        else:
            st.success(severity)

        # ==================================================
        # ROOT CAUSE
        # ==================================================
        st.subheader("Root Cause Analysis")

        root_causes = result.get("root_causes", [])

        if root_causes:
            for cause in root_causes:
                st.warning(cause)
        else:
            st.info("No root cause detected")

        # ==================================================
        # INCIDENT REPORT
        # ==================================================
        st.subheader("Incident Report")
        st.json(result.get("incident_report", {}))

        # ==================================================
        # ALERT
        # ==================================================
        st.subheader("Alert")
        st.info(result.get("alert", "No alert"))

    except Exception as e:
        st.error(f"Detection failed: {e}")

# ==================================================
# INCIDENT HISTORY + LIFECYCLE (FIXED VISUALS)
# ==================================================
st.divider()
st.subheader("📊 Incident History + Lifecycle")

try:
    res = requests.get(f"{API_URL}/incidents", headers=headers)
    data = res.json()

    if isinstance(data, list) and len(data) > 0:

        history = pd.DataFrame(data)

        history["status"] = history["status"].astype(str)

        # ==============================
        # STATUS BADGES
        # ==============================
        def badge(x):
            if x == "OPEN":
                return "🔴 OPEN"
            elif x == "ACK":
                return "🟠 ACK"
            elif x == "RESOLVED":
                return "🟢 RESOLVED"
            return x

        history["status_ui"] = history["status"].apply(badge)

        st.dataframe(history[["id", "score", "severity", "status_ui"]])

        # ==============================
        # PIE CHART
        # ==============================
        if "severity" in history.columns:
            fig = px.pie(history, names="severity", title="Severity Distribution")
            st.plotly_chart(fig, use_container_width=True)

        # ==============================
        # TREND
        # ==============================
        if "score" in history.columns:
            fig = px.line(history, x="id", y="score", title="Anomaly Score Trend")
            st.plotly_chart(fig, use_container_width=True)

        # ==============================
        # LIFECYCLE COUNTS
        # ==============================
        st.subheader("🔧 Incident Lifecycle Summary")

        open_count = len(history[history["status"] == "OPEN"])
        ack_count = len(history[history["status"] == "ACK"])
        resolved_count = len(history[history["status"] == "RESOLVED"])

        c1, c2, c3 = st.columns(3)

        c1.metric("🔴 OPEN", open_count)
        c2.metric("🟠 ACK", ack_count)
        c3.metric("🟢 RESOLVED", resolved_count)

    else:
        st.warning("No incident history found")

except Exception as e:
    st.warning(f"Could not load history: {e}")