from pydantic import BaseModel
from typing import List

class SensorInput(BaseModel):
    engine_id: int
    cycle: int
    sensor_values: List[float]

class StatusUpdate(BaseModel):
    status: str