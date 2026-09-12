from datetime import datetime
from typing import Any

from pydantic import BaseModel


class EventCreate(BaseModel):
    event_type: str
    customer_id: int | None = None
    transaction_id: int | None = None
    payload: dict[str, Any] = {}
    timestamp: datetime | None = None


class EventResponse(BaseModel):
    event_id: str
    event_type: str
    customer_id: int | None
    transaction_id: int | None
    status: str
    timestamp: datetime