from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.digital_twin import simulate_financial_future

router = APIRouter(prefix="/loan", tags=["Loan Simulation"])


@router.post("/simulate")
def simulate_loan(
    customer_id: int,
    loan_amount: float,
    tenure_months: int,
    interest_rate: float,
    db: Session = Depends(get_db),
):
    try:
        result = simulate_financial_future(
            db=db,
            customer_id=customer_id,
            loan_amount=loan_amount,
            tenure_months=tenure_months,
            interest_rate=interest_rate,
        )

        return {
            "success": True,
            "data": result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Loan simulation failed: {exc}",
        )