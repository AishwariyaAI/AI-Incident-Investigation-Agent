from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.crud import get_incidents, update_incident_status
from models.schemas import StatusUpdate

router = APIRouter()


# -------------------------
# DB Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# GET INCIDENTS
# -------------------------
@router.get("/incidents")
def read_incidents():

    db = SessionLocal()

    data = get_incidents(db)

    db.close()

    return data

