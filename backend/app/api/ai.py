from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.agents.orchestrator import orchestrator


router = APIRouter(
    prefix="/ai",
    tags=["AI Orchestrator"],
)


# ============================================================
# REQUEST SCHEMA
# ============================================================

class OrchestrateRequest(BaseModel):
    customer_id: int = Field(..., gt=0)

    loan_requested: bool = False

    loan_amount: float = Field(
        default=0.0,
        ge=0.0,
    )

    tenure_months: int = Field(
        default=36,
        gt=0,
    )

    interest_rate: float = Field(
        default=12.0,
        ge=0.0,
    )

    transaction_id: Optional[int] = None

    language: str = "English"


# ============================================================
# RESPONSE
# ============================================================

class OrchestrateResponse(BaseModel):
    success: bool
    customer: dict
    pipeline: list
    financial_analysis: dict
    security_analysis: dict
    recommendation: dict
    policy: dict
    communication: dict
    final_decision: dict


# ============================================================
# COMPLETE AI PIPELINE
# ============================================================

@router.post(
    "/orchestrate",
    response_model=OrchestrateResponse,
)
def orchestrate_ai(
    request: OrchestrateRequest,
    db: Session = Depends(get_db),
):
    """
    Execute the complete FinGuru AI pipeline.

    Customer
        ↓
    Financial Analyst
        ↓
    Risk & Security
        ↓
    Recommendation
        ↓
    Policy Guardrail
        ↓
    Communication
        ↓
    Final Decision
    """

    try:

        result = orchestrator.run(
            db=db,
            customer_id=request.customer_id,

            loan_requested=request.loan_requested,

            loan_amount=request.loan_amount,

            tenure_months=request.tenure_months,

            interest_rate=request.interest_rate,

            transaction_id=request.transaction_id,

            language=request.language,
        )

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"AI orchestration failed: {exc}",
        )