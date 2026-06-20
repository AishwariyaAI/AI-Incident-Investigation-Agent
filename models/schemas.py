from pydantic import BaseModel


class SensorInput(BaseModel):
    sensor_values: list[float]


class StatusUpdate(BaseModel):
    status: str