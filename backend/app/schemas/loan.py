from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class LoanCreate(BaseModel):
    customer_id: int
    loan_type: str
    principal_amount: Decimal
    interest_rate: float
    tenure_months: int


class LoanResponse(BaseModel):
    id: int
    customer_id: int
    loan_type: str
    principal_amount: Decimal
    interest_rate: float
    tenure_months: int
    monthly_emi: Decimal
    outstanding_amount: Decimal
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LoanSimulationRequest(BaseModel):
    customer_id: int
    loan_amount: Decimal = Field(gt=0)
    tenure_months: int = Field(gt=0)
    interest_rate: float = Field(gt=0)


class LoanSimulationResponse(BaseModel):
    customer_id: int

    loan_amount: Decimal
    tenure_months: int
    interest_rate: float
    monthly_emi: Decimal
    total_interest: Decimal
    total_payment: Decimal

    current_health_score: float
    projected_health_score: float

    current_monthly_surplus: Decimal
    projected_monthly_surplus: Decimal

    current_stress_score: float
    projected_stress_score: float

    affordability: str
    recommendation: str
    reasons: list[str]
    confidence: float