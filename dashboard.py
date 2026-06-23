import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh



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

            st.write("Login Response:")
            st.write(data)

            if "access_token" in data:

                st.session_state.token = data["access_token"]

                st.success("Login Successful")

                st.rerun()

            else:
                st.error("Invalid Login")

        except Exception as e:
            st.error(str(e))

    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.token = None
    st.rerun()

headers = {
    "Authorization":
    f"Bearer {st.session_state.token}"
}
st_autorefresh(
    interval=30000,
    key="live_refresh"
)
# ==========================================
# HEADER
# ==========================================

st.title("🚨 AI Incident Monitoring Center")
st.subheader("🛰 NASA Sensor + AI Incident Detection System")
st.markdown("## 🔔 Live Alerts")

alerts = requests.get(
    f"{API_URL}/alerts"
).json()

for alert in alerts:
    st.error(alert)

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



SENSOR_START = 2
SENSOR_END = 26

# ==========================================
# NASA ENGINE DATA
# ==========================================

st.markdown("## 🔧 NASA Engine Data")
live_mode = st.checkbox(
    "🔴 Live Monitoring Mode"
)

if live_mode:

    sensor = requests.get(
        f"{API_URL}/simulate"
    ).json()

    engine_id = sensor["engine_id"]
    cycle = sensor["cycle"]
    sensor_values = sensor["sensor_values"]

else:

    row_id = st.number_input(
        "Select Engine Row",
        min_value=0,
        max_value=len(df)-1,
        value=0
    )

    row = df.iloc[row_id]

    engine_id = int(row.iloc[0])
    cycle = int(row.iloc[1])

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
st.write("Sensor Count:", len(sensor_values))

if "last_result" not in st.session_state:
    st.session_state.last_result = None
run = st.button("🚀 Run Incident Detection")

if run:

    try:

        payload = {
            "engine_id": engine_id,
            "cycle": cycle,
            "sensor_values": sensor_values
        }

        response = requests.post(
            f"{API_URL}/detect",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        result = response.json()

        st.session_state.last_result = result

    except Exception as e:
        st.error(f"Detection Error: {e}")

# ==========================================
# SHOW LAST RESULT
# ==========================================

if st.session_state.last_result:

    result = st.session_state.last_result

    st.success("✅ Detection Complete")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Prediction",
        result.get("prediction", "N/A")
    )

    col2.metric(
        "Confidence",
        f"{result.get('confidence',0)*100:.2f}%"
    )

    col3.metric(
        "Severity",
        result.get("severity", "N/A")
    )

    col4.metric(
        "Anomaly Score",
        round(result.get("anomaly_score", 0), 4)
    )

    severity = result.get("severity", "")

    st.markdown("## 📊 Detection Results")

    if "CRITICAL" in severity:
        st.error("🚨 ENGINE FAILURE PREDICTED")

    elif "HIGH" in severity:
        st.warning("⚠️ HIGH RISK ENGINE")

    elif "MEDIUM" in severity:
        st.info("🟡 MEDIUM RISK ENGINE")

    else:
        st.success("🟢 ENGINE HEALTHY")

    st.markdown("### 📈 Anomaly Score Gauge")

    score = min(
        max(
            float(result.get("anomaly_score", 0)),
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

    st.markdown("### 🔍 Root Cause Analysis")

    st.info(
        result.get(
            "root_cause",
            "No root cause available"
        )
    )

    st.markdown("### 🤖 AI Investigation Report")

    st.info(
        result.get(
            "ai_report",
            "No report available"
        )
    )

    st.markdown("### 📄 Incident Summary")

    st.json({
        "incident_id":
        result.get("incident_id", 0),

        "prediction":
        result.get("prediction"),

        "severity":
        result.get("severity"),

        "anomaly_score":
        result.get("anomaly_score"),

        "confidence":
        result.get("confidence")
    })

    st.markdown("### 🔔 Alert Status")

    if "CRITICAL" in severity:
        st.error("🚨 CRITICAL INCIDENT DETECTED")

    elif "HIGH" in severity:
        st.warning("⚠️ HIGH RISK DETECTED")

    elif "MEDIUM" in severity:
        st.info("🟡 MEDIUM RISK DETECTED")

    else:
        st.success("🟢 LOW RISK")

    st.markdown("---")



st.markdown("---")
st.markdown(
    "## 📊 Incident History + Lifecycle"
)
incidents = requests.get(
    f"{API_URL}/incidents"
).json()

incidents_df = pd.DataFrame(incidents)

severity_filter = st.selectbox(
    "Filter Severity",
    ["ALL", "LOW", "MEDIUM", "HIGH", "CRITICAL"],
    key="severity_filter"
)

search_id = st.text_input(
    "Search Incident ID",
    key="search_id"
)

if severity_filter != "ALL":
    incidents_df = incidents_df[
        incidents_df["severity"].str.contains(
            severity_filter,
            na=False
        )
    ]

if search_id:

    try:
        incidents_df = incidents_df[
            incidents_df["id"] == int(search_id)
        ]
    except:
        st.warning("Enter numeric Incident ID")
st.dataframe(
    incidents_df,
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

st.markdown("## 🔄 Incident Lifecycle")

lifecycle = requests.get(
    f"{API_URL}/incident-lifecycle"
).json()

col1, col2, col3 = st.columns(3)

col1.metric("OPEN", lifecycle["OPEN"])
col2.metric("ACK", lifecycle["ACK"])
col3.metric("RESOLVED", lifecycle["RESOLVED"])
st.markdown("### ⏱ Incident Timeline")

timeline = requests.get(
    f"{API_URL}/incident-timeline"
).json()

if timeline:

    st.dataframe(
        pd.DataFrame(timeline),
        use_container_width=True
    )

incidents = requests.get(
    f"{API_URL}/incidents"
).json()

incidents_df = pd.DataFrame(incidents)

total = len(incidents_df)

open_incidents = len(
    incidents_df[
        incidents_df["status"] == "OPEN"
    ]
)

resolved_count = len(
    incidents_df[
        incidents_df["status"] == "RESOLVED"
    ]
)

critical_count = len(
    incidents_df[
        incidents_df["severity"]
        .str.contains("CRITICAL", na=False)
    ]
)

st.markdown("## 📊 System Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Incidents",
    total
)

c2.metric(
    "Critical",
    critical_count
)

c3.metric(
    "Open",
    open_incidents
)

c4.metric(
    "Resolved",
    resolved_count
)

failure_rate = (
    critical_count
    / max(len(incidents_df), 1)
) * 100

st.metric(
    "Failure Rate %",
    round(failure_rate, 2)
)

st.markdown("## 🚂 Engine Health")

health = requests.get(
    f"{API_URL}/engine-health-map"
).json()
health_df = pd.DataFrame(health)


st.dataframe(
    pd.DataFrame(health),
    use_container_width=True
)




report = requests.get(
    f"{API_URL}/report"
)

st.download_button(
    "⬇ Download Incident Report",
    report.content,
    file_name="incident_report.csv",
    mime="text/csv"
)

incident_id = st.number_input(
    "Incident ID",
    min_value=1,
    step=1,
    value=1
)


if st.button("🟠 Acknowledge Incident"):

    response = requests.patch(
        f"{API_URL}/incident/{incident_id}/ack"
    )

    if response.status_code == 200:
        st.success("Incident Acknowledged")
    else:
        st.error(response.text)

if st.button("✅ Resolve Incident"):

    response = requests.patch(
        f"{API_URL}/incident/{incident_id}/resolve"
    )

    if response.status_code == 200:
        st.success("Incident Resolved")
    else:
        st.error(response.text)