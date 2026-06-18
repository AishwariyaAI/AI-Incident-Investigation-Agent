from fastapi import FastAPI
from routes import health, detect

app = FastAPI(
    title="AI Incident Investigation Agent",
    version="1.0.0",
    description="Production-grade AI monitoring system"
)

# register routes
app.include_router(health.router)
app.include_router(detect.router)