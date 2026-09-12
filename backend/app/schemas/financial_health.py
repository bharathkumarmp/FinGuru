from datetime import datetime
from pydantic import BaseModel


class FinancialHealthResponse(BaseModel):
    customer_id: int

    score: float
    health_level: str

    income_score: float
    spending_score: float
    savings_score: float
    debt_score: float
    stability_score: float

    monthly_income: float
    monthly_spending: float
    savings_rate: float
    emi_ratio: float
    balance_volatility: float

    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]

    calculated_at: datetime | None = None