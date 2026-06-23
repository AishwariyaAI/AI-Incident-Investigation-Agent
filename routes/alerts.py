from fastapi import APIRouter
from services.alerts import get_alerts

router = APIRouter()

@router.get("/alerts")
def alerts():

    return get_alerts()