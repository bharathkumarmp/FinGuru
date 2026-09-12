from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class FraudAnalysisRequest(BaseModel):
    customer_id: int
    transaction_amount: Decimal
    merchant: str | None = None
    location: str | None = None
    device_id: str | None = None
    beneficiary: str | None = None


class FraudAnalysisResponse(BaseModel):
    customer_id: int
    fraud_score: float
    risk_level: str
    is_suspicious: bool

    anomaly_score: float
    rule_score: float
    identity_risk_score: float

    reasons: list[str]
    recommended_action: str


class FraudEventResponse(BaseModel):
    id: int
    customer_id: int
    transaction_id: int | None
    fraud_score: float
    risk_level: str
    status: str
    reason: str
    created_at: datetime

    class Config:
        from_attributes = True