from pydantic import BaseModel


class CopilotMessage(BaseModel):
    customer_id: int
    message: str
    language: str = "en"


class CopilotResponse(BaseModel):
    customer_id: int
    message: str
    language: str

    intent: str
    recommendation: str | None = None

    confidence: float
    sources: list[str] = []
    actions: list[str] = []