from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Customer,
    CustomerFeatures,
    FinancialHealth,
    FinancialStress,
)
from app.llm.copilot import (
    build_customer_context,
    build_copilot_prompt,
    retrieve_copilot_context,
)
from app.llm.client import generate_llm_response


router = APIRouter(
    prefix="/copilot",
    tags=["AI Copilot"],
)


# ============================================================
# REQUEST / RESPONSE SCHEMAS
# ============================================================

class CopilotRequest(BaseModel):
    customer_id: int = Field(..., gt=0)
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )
    language: str = Field(
        default="English",
        max_length=50,
    )
    use_customer_context: bool = True


class CopilotResponse(BaseModel):
    success: bool
    customer_id: int
    question: str
    answer: str
    language: str
    sources: list
    customer_context_used: bool


# ============================================================
# CUSTOMER FINANCIAL CONTEXT
# ============================================================

def get_customer_financial_context(
    db: Session,
    customer_id: int,
) -> Optional[str]:

    features = (
        db.query(CustomerFeatures)
        .filter(
            CustomerFeatures.customer_id == customer_id
        )
        .first()
    )

    health = (
        db.query(FinancialHealth)
        .filter(
            FinancialHealth.customer_id == customer_id
        )
        .order_by(
            FinancialHealth.calculated_at.desc()
        )
        .first()
    )

    stress = (
        db.query(FinancialStress)
        .filter(
            FinancialStress.customer_id == customer_id
        )
        .order_by(
            FinancialStress.id.desc()
        )
        .first()
    )

    if not features:
        return None

    # --------------------------------------------------------
    # Financial Health
    # --------------------------------------------------------

    health_score = 0.0

    if health:
        health_score = float(
            health.score
        )

    # --------------------------------------------------------
    # Financial Stress
    # --------------------------------------------------------

    stress_score = 0.0

    if stress:

        if hasattr(
            stress,
            "stress_score",
        ):
            stress_score = float(
                stress.stress_score
            )

        elif hasattr(
            stress,
            "score",
        ):
            stress_score = float(
                stress.score
            )

    # --------------------------------------------------------
    # Financial State
    # --------------------------------------------------------

    monthly_income = float(
        features.avg_monthly_income
    )

    monthly_spending = float(
        features.avg_monthly_spending
    )

    monthly_surplus = (
        monthly_income
        - monthly_spending
    )

    return build_customer_context(
        monthly_income=monthly_income,
        monthly_spending=monthly_spending,
        monthly_surplus=monthly_surplus,
        savings_rate=float(
            features.savings_rate
        ),
        emi_ratio=float(
            features.emi_ratio
        ),
        financial_health=health_score,
        financial_stress=stress_score,
    )


# ============================================================
# COPILOT CHAT
# ============================================================

@router.post(
    "/chat",
    response_model=CopilotResponse,
)
def copilot_chat(
    request: CopilotRequest,
    db: Session = Depends(get_db),
):

    # ========================================================
    # 1. VERIFY CUSTOMER
    # ========================================================

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == request.customer_id
        )
        .first()
    )

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    # ========================================================
    # 2. RAG RETRIEVAL
    # ========================================================

    rag_data = retrieve_copilot_context(
        question=request.message,
        top_k=5,
    )

    knowledge_context = rag_data[
        "context"
    ]

    sources = rag_data[
        "sources"
    ]

    # ========================================================
    # 3. CUSTOMER FINANCIAL CONTEXT
    # ========================================================

    customer_context = None

    if request.use_customer_context:

        customer_context = (
            get_customer_financial_context(
                db=db,
                customer_id=request.customer_id,
            )
        )

    # ========================================================
    # 4. BUILD RAG + CUSTOMER PROMPT
    # ========================================================

    prompt = build_copilot_prompt(
        question=request.message,
        knowledge_context=knowledge_context,
        customer_context=customer_context,
    )

    # Add explicit language instruction.
    prompt = f"""
{prompt}

LANGUAGE REQUIREMENT
--------------------
Respond in {request.language}.

If the requested language is not English,
preserve financial terminology where useful,
but explain the concept naturally in the requested language.
""".strip()

    # ========================================================
    # 5. CALL REAL LLM
    # ========================================================

    try:

        answer = generate_llm_response(
            prompt=prompt,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"LLM generation failed: {exc}",
        )

    # ========================================================
    # 6. RETURN RESPONSE
    # ========================================================

    return {
        "success": True,
        "customer_id": request.customer_id,
        "question": request.message,
        "answer": answer,
        "language": request.language,
        "sources": sources,
        "customer_context_used": (
            customer_context is not None
        ),
    }   