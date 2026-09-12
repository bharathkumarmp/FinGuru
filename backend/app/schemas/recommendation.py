from datetime import datetime
from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    id: int
    customer_id: int

    action: str
    title: str
    description: str

    score: float
    confidence: float

    need_score: float
    affordability_score: float
    suitability_score: float
    timing_score: float
    preference_score: float
    financial_health_score: float

    reasons: list[str]

    created_at: datetime

    class Config:
        from_attributes = True