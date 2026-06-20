from database.db import Base
from sqlalchemy import Column, Integer, Float, String

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    engine_id = Column(Integer)
    cycle = Column(Integer)

    prediction = Column(Integer)
    confidence = Column(Float)
    anomaly_score = Column(Float)

    severity = Column(String)
    status = Column(String)