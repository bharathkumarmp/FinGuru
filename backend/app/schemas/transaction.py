from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    customer_id: int
    account_id: int | None = None
    transaction_type: str
    amount: Decimal
    merchant: str | None = None
    category: str | None = None
    location: str | None = None
    device_id: str | None = None
    beneficiary: str | None = None
    description: str | None = None


class TransactionResponse(BaseModel):
    id: int
    customer_id: int
    account_id: int | None
    transaction_type: str
    amount: Decimal
    merchant: str | None
    category: str | None
    location: str | None
    device_id: str | None
    beneficiary: str | None
    description: str | None
    timestamp: datetime

    class Config:
        from_attributes = True


class TransactionAnalysisResponse(BaseModel):
    transaction_id: int
    fraud_score: float
    risk_level: str
    is_suspicious: bool
    reasons: list[str]