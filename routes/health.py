from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {
        "service": "AI Incident Investigation Agent",
        "status": "healthy",
        "version": "1.0.0"
    }