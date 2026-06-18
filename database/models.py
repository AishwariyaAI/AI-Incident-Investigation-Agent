from sqlalchemy import Column, Integer, Float, String, DateTime
from database.db import Base
import datetime

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    score = Column(Float)

    prediction = Column(Integer)

    severity = Column(String)

    status = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )