from datetime import datetime

from pydantic import BaseModel


class IncidentResponse(BaseModel):
    id: int
    incident_type: str
    severity: str
    customer_id: int | None
    title: str
    description: str
    status: str

    detected_at: datetime
    resolved_at: datetime | None = None

    recommended_action: str | None = None

    class Config:
        from_attributes = True