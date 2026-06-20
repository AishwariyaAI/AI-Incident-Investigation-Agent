from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.analytics import router as analytics_router
from database.db import Base, engine
from database import models

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
    websocket
)

# REGISTER ROUTES
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(detect.router, prefix="/api/v1", tags=["Detection"])
app.include_router(history.router, prefix="/api/v1", tags=["History"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
app.include_router(websocket.router, prefix="/api/v1", tags=["Realtime"])

# ROOT
@app.get("/")
def root():
    return {
        "message": "AI Incident Investigation Agent running 🚀",
        "docs": "/docs"
    }