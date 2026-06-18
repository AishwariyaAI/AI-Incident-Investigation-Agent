from pydantic import BaseModel

class InputData(BaseModel):
    sensor_values: list[float]