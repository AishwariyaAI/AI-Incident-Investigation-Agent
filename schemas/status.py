from pydantic import BaseModel

class StatusUpdate(BaseModel):
    status: str  # OPEN / RESOLVED / CLOSED