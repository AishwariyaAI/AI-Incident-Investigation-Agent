from database.db import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

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
    timestamp = Column(
    DateTime,
    default=datetime.utcnow
)