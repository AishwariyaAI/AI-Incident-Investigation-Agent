import requests

API_URL = "http://127.0.0.1:8001/detect"

def get_predictions():

    payload = {
        "sensor_scores":[0.3,0.8,0.9],
        "image_scores":[0.2,0.7,0.1],
        "log_scores":[0.4,0.6,0.3]
    }

    response = requests.post(
        API_URL,
        json=payload
    )

    return response.json()