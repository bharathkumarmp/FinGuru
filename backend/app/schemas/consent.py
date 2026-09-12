from datetime import datetime

from pydantic import BaseModel


class ConsentCreate(BaseModel):
    purpose: str
    granted: bool


class ConsentResponse(BaseModel):
    id: int
    customer_id: int
    purpose: str
    granted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True