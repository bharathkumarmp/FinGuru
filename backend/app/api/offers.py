from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.customer import Customer
from app.models.customer_features import CustomerFeatures
from app.models.financial_health import FinancialHealth
from app.models.financial_stress import FinancialStress

from app.privacy.consent_manager import has_consent

from app.services.offer_engine import generate_next_best_offer
from app.services.life_events import detect_life_events


router = APIRouter(
    prefix="/offers",
    tags=["Next Best Offers"],
)


@router.get("/{customer_id}")
def get_customer_offers(
    customer_id: int,
    db: Session = Depends(get_db),
):
    """
    Generate personalized financial offers.

    Flow:

        Customer
            ↓
        Financial Features
            ↓
        Financial Health
            ↓
        Financial Stress
            ↓
        Life Event Detection
            ↓
        Consent
            ↓
        Next Best Offer Engine
            ↓
        Personalized Offer
    """

    # ========================================================
    # 1. VERIFY CUSTOMER
    # ========================================================

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id
        )
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {customer_id} not found",
        )

    # ========================================================
    # 2. GET CUSTOMER FEATURES
    # ========================================================

    features = (
        db.query(CustomerFeatures)
        .filter(
            CustomerFeatures.customer_id == customer_id
        )
        .first()
    )

    if features is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Financial features for customer "
                f"{customer_id} not found"
            ),
        )

    # ========================================================
    # 3. GET LATEST FINANCIAL HEALTH
    # ========================================================

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

    if health is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Financial health for customer "
                f"{customer_id} not found"
            ),
        )

    # ========================================================
    # 4. GET LATEST FINANCIAL STRESS
    # ========================================================

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

    if stress is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Financial stress for customer "
                f"{customer_id} not found"
            ),
        )

    # ========================================================
    # 5. EXTRACT FINANCIAL STATE
    # ========================================================

    monthly_income = float(
        features.avg_monthly_income or 0.0
    )

    monthly_spending = float(
        features.avg_monthly_spending or 0.0
    )

    monthly_surplus = (
        monthly_income - monthly_spending
    )

    savings_rate = float(
        features.savings_rate or 0.0
    )

    emi_ratio = float(
        features.emi_ratio or 0.0
    )

    income_stability = float(
        features.income_stability or 0.0
    )

    health_score = float(
        health.score or 0.0
    )

    # ========================================================
    # 6. EXTRACT STRESS SCORE
    # ========================================================

    if hasattr(stress, "stress_score"):
        stress_score = float(
            stress.stress_score or 0.0
        )

    elif hasattr(stress, "score"):
        stress_score = float(
            stress.score or 0.0
        )

    else:
        stress_score = 0.0

    # ========================================================
    # 7. CHECK CONSENT
    # ========================================================

    consent_given = has_consent(
        db=db,
        customer_id=customer_id,
        purpose="financial_advice",
    )

    # ========================================================
    # 8. DETECT LIFE EVENTS
    # ========================================================

    try:

        detected_events = detect_life_events(
            db=db,
            customer_id=customer_id,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Life event detection failed: {str(exc)}"
            ),
        )

    # ========================================================
    # 9. NORMALIZE LIFE EVENT OUTPUT
    # ========================================================

    life_events = []

    for event in detected_events:

        if isinstance(event, dict):

            life_events.append(
                {
                    "event_type": event.get(
                        "event_type",
                        event.get(
                            "type",
                            "UNKNOWN",
                        ),
                    ),
                    "confidence": event.get(
                        "confidence",
                        1.0,
                    ),
                    "reason": event.get(
                        "reason",
                        "",
                    ),
                }
            )

    # ========================================================
    # 10. GENERATE NEXT BEST OFFER
    # ========================================================

    try:

        result = generate_next_best_offer(
            health_score=health_score,
            stress_score=stress_score,
            monthly_surplus=monthly_surplus,
            savings_rate=savings_rate,
            emi_ratio=emi_ratio,
            income_stability=income_stability,
            consent_given=consent_given,
            life_events=life_events,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Offer generation failed: {str(exc)}"
            ),
        )

    # ========================================================
    # 11. RETURN COMPLETE RESPONSE
    # ========================================================

    return {
        "success": True,

        "customer_id": customer_id,

        "customer": {
            "name": customer.full_name,
            "city": customer.city,
            "occupation": customer.occupation,
        },

        "consent": {
            "purpose": "financial_advice",
            "granted": consent_given,
        },

        "financial_state": {
            "monthly_income": monthly_income,
            "monthly_spending": monthly_spending,
            "monthly_surplus": monthly_surplus,
            "savings_rate": savings_rate,
            "emi_ratio": emi_ratio,
            "income_stability": income_stability,
            "financial_health": health_score,
            "financial_stress": stress_score,
        },

        "life_events": life_events,

        "next_best_offer": result,
    }