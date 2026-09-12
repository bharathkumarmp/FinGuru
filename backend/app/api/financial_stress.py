from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Customer, CustomerFeatures, FinancialStress
from app.services.financial_stress import calculate_customer_stress


router = APIRouter(
    prefix="/customers",
    tags=["Financial Stress"],
)


# ============================================================
# SERIALIZER
# ============================================================

def stress_to_dict(stress) -> dict:
    """
    Convert FinancialStress SQLAlchemy object
    into a JSON-safe dictionary.
    """

    # The project has used both naming conventions
    # stress_score / score and stress_level / level
    # in different parts of the implementation.

    score = getattr(
        stress,
        "stress_score",
        getattr(stress, "score", 0),
    )

    level = getattr(
        stress,
        "stress_level",
        getattr(stress, "level", "UNKNOWN"),
    )

    factors = getattr(
        stress,
        "stress_factors",
        getattr(stress, "factors", None),
    )

    return {
        "id": stress.id,
        "customer_id": stress.customer_id,

        "stress_score": float(score),
        "stress_level": level,

        "stress_factors": factors,

        "calculated_at": stress.calculated_at,
    }


# ============================================================
# CALCULATE FINANCIAL STRESS
# ============================================================

@router.get("/{customer_id}/financial-stress")
def get_financial_stress(
    customer_id: int,
    db: Session = Depends(get_db),
):
    """
    Calculate and return the customer's financial stress.

    Flow:

    Customer
        ↓
    Customer Features
        ↓
    Financial Stress Engine
        ↓
    Stress Score
        ↓
    Stress Level
    """

    # --------------------------------------------------------
    # CHECK CUSTOMER
    # --------------------------------------------------------

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {customer_id} not found",
        )

    # --------------------------------------------------------
    # CHECK FEATURES
    # --------------------------------------------------------

    features = (
        db.query(CustomerFeatures)
        .filter(
            CustomerFeatures.customer_id == customer_id
        )
        .first()
    )

    if not features:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Financial features for "
                f"customer {customer_id} not found. "
                f"Run feature engineering first."
            ),
        )

    # --------------------------------------------------------
    # CALCULATE STRESS
    # --------------------------------------------------------

    try:

        stress = calculate_customer_stress(
            db=db,
            customer_id=customer_id,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Financial stress calculation failed: "
                f"{exc}"
            ),
        )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "success": True,
        "customer_id": customer_id,
        "financial_stress": stress_to_dict(stress),
    }


# ============================================================
# GET LATEST STORED STRESS
# ============================================================

@router.get("/{customer_id}/financial-stress/latest")
def get_latest_financial_stress(
    customer_id: int,
    db: Session = Depends(get_db),
):
    """
    Return the latest stored financial stress record
    without recalculating it.
    """

    # --------------------------------------------------------
    # CHECK CUSTOMER
    # --------------------------------------------------------

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {customer_id} not found",
        )

    # --------------------------------------------------------
    # GET LATEST RECORD
    # --------------------------------------------------------

    stress = (
        db.query(FinancialStress)
        .filter(
            FinancialStress.customer_id == customer_id
        )
        .order_by(
            FinancialStress.calculated_at.desc()
        )
        .first()
    )

    if not stress:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No financial stress record "
                f"found for customer {customer_id}"
            ),
        )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "success": True,
        "customer_id": customer_id,
        "financial_stress": stress_to_dict(
            stress
        ),
    }