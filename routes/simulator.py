from fastapi import APIRouter
import random

router = APIRouter()


@router.get("/simulate")
def simulate():

    sensor_values = [
        random.uniform(0, 100)
        for _ in range(24)
    ]

    return {
        "engine_id": 1,
        "cycle": 100,
        "sensor_values": sensor_values
    }