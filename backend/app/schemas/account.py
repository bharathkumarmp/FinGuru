from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class AccountCreate(BaseModel):
    customer_id: int
    account_number: str
    account_type: str
    balance: Decimal = Decimal("0")
    currency: str = "INR"


class AccountResponse(BaseModel):
    id: int
    customer_id: int
    account_number: str
    account_type: str
    balance: Decimal
    currency: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True