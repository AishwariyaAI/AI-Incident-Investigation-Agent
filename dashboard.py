import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="AI Incident Monitoring Center",
    layout="wide"
)

# ==========================================
# LOGIN
# ==========================================

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is None:

    st.title("🔐 AI Incident Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        try:

            res = requests.post(
                f"{API_URL}/login",
                json={
                    "username": username,
                    "password": password
                }
            )

            data = res.json()

            if "access_token" in data:

                st.session_state.token = data["access_token"]

                st.success("Login Successful")

                st.rerun()

            else:
                st.error("Invalid Login")

        except Exception as e:
            st.error(str(e))

    st.stop()

headers = {
    "Authorization":
    f"Bearer {st.session_state.token}"
}
# ==========================================
# HEADER
# ==========================================

st.title("🚨 AI Incident Monitoring Center")
st.subheader("🛰 NASA Sensor + AI Incident Detection System")

st.markdown("---")

# ==========================================
# DATASET SELECTOR
# ==========================================

dataset_choice = st.selectbox(
    "📂 Select Dataset",
    ["Test Dataset", "Training Dataset"]
)

if dataset_choice == "Test Dataset":
    path = "data/test_FD001.txt"
else:
    path = "ml/train_FD001.txt"

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    path,
    sep=r"\s+",
    header=None
)

df = df.dropna().reset_index(drop=True)

st.caption(
    f"Loaded: {dataset_choice} | Rows: {len(df)}"
)

# ==========================================
# NASA FD001 COLUMN MAPPING
# ==========================================

ENGINE_ID_COL = 0
CYCLE_COL = 1

SENSOR_START = 2
SENSOR_END = 26

# ==========================================
# NASA ENGINE DATA
# ==========================================

st.markdown("## 🔧 NASA Engine Data")

row_id = st.number_input(
    "Select Engine Row",
    min_value=0,
    max_value=len(df)-1,
    value=0
)

row = df.iloc[row_id]

engine_id = int(row.iloc[ENGINE_ID_COL])
cycle = int(row.iloc[CYCLE_COL])

sensor_values = (
    row.iloc[SENSOR_START:SENSOR_END]
    .astype(float)
    .tolist()
)

c1, c2 = st.columns(2)

c1.metric("Engine ID", engine_id)
c2.metric("Cycle", cycle)

st.markdown("### 📡 Sensor Values")

st.json(sensor_values)

run = st.button(
    "🚀 Run Incident Detection"
)
if run:

    try:

        res = requests.post(
            f"{API_URL}/detect",
            json={
                "engine_id": engine_id,
                "cycle": cycle,
                "sensor_values": sensor_values
            },
            headers=headers
        )

        if res.status_code != 200:
            st.error(res.text)
            st.stop()

        result = res.json()

        st.success("✅ Detection Complete")

        st.markdown("## 📊 Detection Results")

        a, b, c, d = st.columns(4)

        a.metric(
            "Anomaly Score",
            round(result["anomaly_score"], 4)
        )

        b.metric(
            "Prediction",
            result["prediction"]
        )

        c.metric(
            "Severity",
            result["severity"]
        )

        d.metric(
            "Confidence",
            f"{result['confidence']*100:.2f}%"
        )

        st.markdown("### 📈 Anomaly Score Gauge")

        score = min(
            max(
                float(result["anomaly_score"]),
                0
            ),
            1
        )

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                gauge={
                    "axis": {
                        "range": [0, 1]
                    }
                }
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("### 🚨 Severity Status")

        severity = result["severity"]

        if "CRITICAL" in severity:
            st.error(severity)

        elif "HIGH" in severity:
            st.warning(severity)

        elif "MEDIUM" in severity:
            st.info(severity)

        else:
            st.success(severity)

        st.markdown("### 🧠 Root Cause Analysis")

        st.warning(
            result.get(
                "root_cause",
                "No root cause available"
            )
        )

        st.markdown("### 📄 Incident Report")

        st.json({
            "incident_id":
            result.get("incident_id", 0),

            "score":
            result["anomaly_score"],

            "prediction":
            result["prediction"],

            "severity":
            result["severity"],

            "status":
            "OPEN"
        })

        st.markdown("### 🔔 Alert")

        if "CRITICAL" in severity:
            st.error(
                "🚨 CRITICAL INCIDENT DETECTED"
            )

        elif "HIGH" in severity:
            st.warning(
                "⚠️ HIGH RISK DETECTED"
            )

        elif "MEDIUM" in severity:
            st.info(
                "🟡 MEDIUM RISK DETECTED"
            )

        else:
            st.success(
                "🟢 LOW RISK"
            )

    except Exception as e:
        st.error(str(e))
        st.markdown("---")

st.markdown(
    "## 📊 Incident History + Lifecycle"
)

# ==========================================
# INCIDENT HISTORY
# ==========================================

st.markdown("### 📜 Incident History")

history = requests.get(
    f"{API_URL}/incidents"
).json()

if history:
    st.dataframe(
        pd.DataFrame(history),
        use_container_width=True
    )

# ==========================================
# SEVERITY PIE
# ==========================================

st.markdown(
    "### ⚖️ Severity Distribution"
)

pie = requests.get(
    f"{API_URL}/severity-pie"
).json()

if pie:

    df_pie = pd.DataFrame({
        "severity": list(pie.keys()),
        "count": list(pie.values())
    })

    fig = px.pie(
        df_pie,
        names="severity",
        values="count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# ANOMALY TREND
# ==========================================

st.markdown(
    "### 📈 Anomaly Trend"
)

trend = requests.get(
    f"{API_URL}/anomaly-trend"
).json()

if trend:

    df_trend = pd.DataFrame(trend)

    fig = px.line(
        df_trend,
        x="cycle",
        y="anomaly_score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# LIFECYCLE
# ==========================================

st.markdown(
    "### 🔧 Incident Lifecycle Summary"
)

life = requests.get(
    f"{API_URL}/incident-lifecycle"
).json()

if life:

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🔴 OPEN",
        life.get("OPEN", 0)
    )

    c2.metric(
        "🟠 ACK",
        life.get("ACK", 0)
    )

    c3.metric(
        "🟢 RESOLVED",
        life.get("RESOLVED", 0)
    )
