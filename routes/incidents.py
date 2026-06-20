from fastapi import APIRouter
from database.db import SessionLocal
from database.models import Incident

router = APIRouter()

@router.get("/incidents")
def get_incidents():
    db = SessionLocal()
    data = db.query(Incident).all()
    db.close()
    return data