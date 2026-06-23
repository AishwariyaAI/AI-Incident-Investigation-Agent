from fastapi import APIRouter
from fastapi.responses import Response
import pandas as pd

router = APIRouter()

@router.get("/report")
def download_report():

    data = [
        {"engine": 1, "severity": "LOW"},
        {"engine": 2, "severity": "HIGH"},
        {"engine": 3, "severity": "CRITICAL"},
    ]

    df = pd.DataFrame(data)

    csv_data = df.to_csv(index=False)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=incident_report.csv"
        }
    )