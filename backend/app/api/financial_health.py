from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Customer, CustomerFeatures, FinancialHealth
from app.services.financial_health import calculate_customer_health


router = APIRouter(
    prefix="/customers",
    tags=["Financial Health"],
)


# ============================================================
# SERIALIZER
# ============================================================

def health_to_dict(health) -> dict:
    """
    Convert FinancialHealth SQLAlchemy object to JSON-safe dict.
    """

    return {
        "id": health.id,
        "customer_id": health.customer_id,

        "score": float(health.score),
        "health_level": health.health_level,

        "income_score": float(health.income_score),
        "spending_score": float(health.spending_score),
        "savings_score": float(health.savings_score),
        "debt_score": float(health.debt_score),
        "stability_score": float(health.stability_score),

        "monthly_income": float(health.monthly_income),
        "monthly_spending": float(health.monthly_spending),
        "savings_rate": float(health.savings_rate),
        "emi_ratio": float(health.emi_ratio),
        "balance_volatility": float(health.balance_volatility),

        "strengths": health.strengths,
        "weaknesses": health.weaknesses,
        "recommendations": health.recommendations,

        "calculated_at": health.calculated_at,
    }


# ============================================================
# CALCULATE / GET FINANCIAL HEALTH
# ============================================================

@router.get("/{customer_id}/financial-health")
def get_financial_health(
    customer_id: int,
    db: Session = Depends(get_db),
):
    """
    Calculate and return the customer's latest financial health.

    Flow:

    Customer
        ↓
    Customer Features
        ↓
    Financial Health Engine
        ↓
    Financial Health Score
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
    # GET FEATURES
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
    # CALCULATE HEALTH
    # --------------------------------------------------------

    try:
        health = calculate_customer_health(
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
                f"Financial health calculation failed: "
                f"{exc}"
            ),
        )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "success": True,
        "customer_id": customer_id,
        "financial_health": health_to_dict(health),
    }


# ============================================================
# GET STORED HEALTH RECORD
# ============================================================

@router.get("/{customer_id}/financial-health/latest")
def get_latest_financial_health(
    customer_id: int,
    db: Session = Depends(get_db),
):
    """
    Return the latest stored financial health record
    without recalculating it.
    """

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

    if not health:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No financial health record "
                f"found for customer {customer_id}"
            ),
        )

    return {
        "success": True,
        "customer_id": customer_id,
        "financial_health": health_to_dict(health),
    }