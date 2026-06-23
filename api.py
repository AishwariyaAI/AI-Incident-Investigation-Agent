from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.analytics import router as analytics_router
from database.db import Base, engine
from database import models
from routes import status
from routes import simulator
from database.models import Incident
from database.user_model import User
from routes import status
from routes.alerts import router as alerts_router
from routes.report import router as report_router
from routes import engine_health
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Incident Investigation Agent",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IMPORT ROUTES
from routes import (
    health,
    detect,
    analytics,
    history,
    auth,
    websocket,
    status,
    simulator,
    engine_health
    
)

# REGISTER ROUTES
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(detect.router, prefix="/api/v1", tags=["Detection"])
app.include_router(history.router, prefix="/api/v1", tags=["History"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
app.include_router(websocket.router, prefix="/api/v1", tags=["Realtime"])
app.include_router(
    status.router,
    prefix="/api/v1",
    tags=["Status"]
)
app.include_router(
    simulator.router,
    prefix="/api/v1",
    tags=["Simulation"]
)
app.include_router(
    engine_health.router,
    prefix="/api/v1",
    tags=["Engine Health"]
)

app.include_router(
    alerts_router,
    prefix="/api/v1",
    tags=["Alerts"]
)
app.include_router(
    report_router,
    prefix="/api/v1"
)
# ROOT
@app.get("/")
def root():
    return {
        "message": "AI Incident Investigation Agent running 🚀",
        "docs": "/docs"
    }