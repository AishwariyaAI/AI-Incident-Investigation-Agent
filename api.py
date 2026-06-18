from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Database
from database.db import engine
from database.models import Incident
from database.user_model import User

# Create tables
Incident.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)

# Routes
from routes import (
    health,
    detect,
    history,
    websocket,
    auth
)

app = FastAPI(
    title="AI Incident Investigation Agent",
    version="1.0.0",
    description="""
AI-powered system for:

- Anomaly Detection
- Severity Classification
- Incident Reporting
- Root Cause Analysis
- Real-time Monitoring System
- Authentication System
"""
)

# ----------------------------------
# CORS
# ----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------
# HEALTH
# ----------------------------------

app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["System Health"]
)

# ----------------------------------
# AUTHENTICATION
# ----------------------------------

app.include_router(
    auth.router,
    prefix="/api/v1",
    tags=["Authentication"]
)

# ----------------------------------
# DETECTION
# ----------------------------------

app.include_router(
    detect.router,
    prefix="/api/v1",
    tags=["Core Engine"]
)

# ----------------------------------
# INCIDENT HISTORY
# ----------------------------------

app.include_router(
    history.router,
    prefix="/api/v1",
    tags=["Incident History"]
)

# ----------------------------------
# WEBSOCKET
# ----------------------------------

app.include_router(
    websocket.router,
    prefix="/api/v1",
    tags=["Real-time Monitoring"]
)

# ----------------------------------
# ROOT
# ----------------------------------

@app.get("/", tags=["Root"])
def root():

    return {
        "message": "AI Incident Investigation Agent is running 🚀",
        "status": "active",
        "docs": "/docs"
    }