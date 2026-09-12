from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None
    date_of_birth: date | None = None
    city: str | None = None
    occupation: str | None = None
    monthly_income: Decimal = Decimal("0")


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int
    customer_code: str
    created_at: datetime

    class Config:
        from_attributes = True


class Customer360Response(BaseModel):
    customer: CustomerResponse
    total_balance: Decimal
    monthly_income: Decimal
    monthly_spending: Decimal
    savings_rate: float
    emi_ratio: float
    financial_health_score: float
    financial_stress_score: float
    risk_level: str
    segment: str