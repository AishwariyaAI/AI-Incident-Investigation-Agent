# 🚨 AI Incident Investigation Agent

AI-powered Predictive Maintenance and Incident Investigation Platform built using FastAPI, Machine Learning, and NASA FD001 engine sensor data.

## 📌 Project Overview

The AI Incident Investigation Agent is an intelligent monitoring system that analyzes NASA engine sensor data, detects anomalies, predicts potential failures, classifies incident severity, performs root cause analysis, and generates AI-powered investigation reports.

The system helps engineering teams identify failures before they occur and supports proactive maintenance decisions.

---
🔑 DEMO LOGIN CREDENTIALS

Username: admin

Password: admin123

⚠️ Required to access the live dashboard.

Quick Access
1.Open the Dashboard link
2.Enter the demo credentials above
3.Explore incidents, analytics, and root cause analysis

## 🚀 Live Deployment

### Dashboard


### API Documentation (Swagger)

https://ai-incident-investigation-agent.onrender.com/docs

### Health Endpoint

https://ai-incident-investigation-agent.onrender.com/api/v1/health

---

## 🛠 Tech Stack

### Backend

* FastAPI
* Uvicorn
* Python 3.12

### Machine Learning

* Scikit-Learn
* Joblib
* NASA FD001 Dataset

### Database

* SQLite
* SQLAlchemy

### Authentication

* JWT Authentication
* Python-Jose
* Passlib

### Visualization

* Streamlit
* Plotly

### Deployment

* Docker
* GitHub
* Render

---

## 🏗 System Architecture

NASA FD001 Dataset
↓
Sensor Data Processing
↓
Machine Learning Model
↓
Anomaly Detection
↓
Severity Classification
↓
Root Cause Analysis
↓
AI Investigation Report
↓
FastAPI REST APIs
↓
Streamlit Dashboard

---

## ✨ Features

### Incident Detection

* Real-time anomaly detection
* Engine health monitoring
* Failure prediction

### AI Investigation

* Root cause analysis
* AI-generated investigation reports
* Incident summaries

### Incident Management

* Open incidents
* Acknowledge incidents
* Resolve incidents

### Analytics

* Severity distribution
* Incident lifecycle tracking
* Engine health monitoring
* Anomaly trends

### Security

* JWT Authentication
* Protected API endpoints

---

## 📂 Project Structure

AI-Incident-Investigation-Agent/

├── api.py

├── dashboard.py

├── database/

├── routes/

├── services/

├── schemas/

├── ml/

│   ├── model.pkl

│   ├── scaler.pkl

│   └── train.py

├── Dockerfile

├── requirements.txt

└── README.md

---

## 📸 Screenshots

### Swagger Documentation


<img width="1920" height="1080" alt="Screenshot (331)" src="https://github.com/user-attachments/assets/084fd947-5474-43a9-83cd-e87877f05ad4" />
<img width="1920" height="1080" alt="Screenshot (332)" src="https://github.com/user-attachments/assets/a5b8beaa-69d4-4e04-83e8-b15eaeca9297" />


### Incident Dashboard

<img width="1920" height="1080" alt="Screenshot (333)" src="https://github.com/user-attachments/assets/673e39f1-af3b-4484-9287-3d17594cfdf6" />
<img width="1920" height="1080" alt="Screenshot (334)" src="https://github.com/user-attachments/assets/6a031789-76f8-4506-8958-f071e6f50329" />


### Detection Results

<img width="1920" height="1080" alt="Screenshot (335)" src="https://github.com/user-attachments/assets/992941ac-f06c-4960-9331-387b083bcf62" />
<img width="1920" height="1080" alt="Screenshot (336)" src="https://github.com/user-attachments/assets/b3fb2722-323b-4c19-a6fe-88591706dcff" />
<img width="1920" height="1080" alt="Screenshot (337)" src="https://github.com/user-attachments/assets/083dae2b-6495-45d9-af6e-ee32e353ec77" />
<img width="1920" height="1080" alt="Screenshot (338)" src="https://github.com/user-attachments/assets/f64ebeaa-4f50-47a4-96e8-a57d7c849501" />
<img width="1920" height="1080" alt="Screenshot (339)" src="https://github.com/user-attachments/assets/d6149a01-39fa-46b5-a8cd-12ee6ef05a5f" />
<img width="1920" height="1080" alt="Screenshot (336)" src="https://github.com/user-attachments/assets/35308b80-6cf0-4b3b-9833-77b2a6164bcf" />
<img width="1920" height="1080" alt="Screenshot (339)" src="https://github.com/user-attachments/assets/5a7c87dd-e862-4a4d-b458-f8cbcf093d59" />
<img width="1920" height="1080" alt="Screenshot (334)" src="https://github.com/user-attachments/assets/f674e618-37ca-410c-a111-6fb6f4b1171d" />



---
## 📊 Dataset

Dataset Used:

NASA Turbofan Engine Degradation Simulation Dataset (FD001)

Used for predictive maintenance and engine failure prediction.

---

## 🔐 Authentication

Login Endpoint:

POST /api/v1/login

Protected APIs:

* /api/v1/detect
* /api/v1/incidents
* /api/v1/report

JWT Bearer Authentication is required.

---

## 🧪 Example Detection Request

```json
{
  "engine_id": 1,
  "cycle": 50,
  "sensor_values": [
    518.67,
    641.82,
    1589.70,
    1400.60,
    14.62,
    21.61
  ]
}
```

---

## 📈 Future Enhancements

* PostgreSQL integration
* Real-time WebSocket alerts
* Cloud-native monitoring
* LLM-powered investigation assistant
* Advanced predictive maintenance models
* Multi-engine fleet monitoring

---

## 👩‍💻 Author

Aishwariya A

AI/ML Engineer | Generative AI Enthusiast | Full Stack AI Developer

GitHub:
https://github.com/AishwariyaAI

Email:
[aishwariyaalwar@gmail.com](mailto:aishwariyaalwar@gmail.com)
