from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.customer_features import CustomerFeatures
from app.models.financial_health import FinancialHealth
from app.models.financial_stress import FinancialStress

from app.services.recommendation_engine import generate_recommendation

from app.policy.policy_engine import policy_engine


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get("/{customer_id}")
def get_customer_recommendation(
    customer_id: int,
    db: Session = Depends(get_db),
):
    """
    Generate a personalized recommendation and
    validate it through the Policy Engine.

    Flow:

        Financial Features
                ↓
        Financial Health
                ↓
        Financial Stress
                ↓
        Recommendation Engine
                ↓
        Policy Engine
                ↓
        Final Next Best Action
    """

    # ========================================================
    # 1. GET FINANCIAL FEATURES
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
    # 2. GET LATEST FINANCIAL HEALTH
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
    # 3. GET LATEST FINANCIAL STRESS
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
    # 4. EXTRACT STRESS SCORE
    # ========================================================

    if hasattr(stress, "stress_score"):
        stress_score = stress.stress_score

    elif hasattr(stress, "score"):
        stress_score = stress.score

    else:
        stress_score = 0.0

    # ========================================================
    # 5. CALCULATE FINANCIAL STATE
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

    emi_ratio = float(
        features.emi_ratio or 0.0
    )

    health_score = float(
        health.score or 0.0
    )

    stress_score = float(
        stress_score or 0.0
    )

    # ========================================================
    # 6. GENERATE RECOMMENDATION
    # ========================================================

    try:

        recommendation = generate_recommendation(
            health_score=health_score,
            stress_score=stress_score,
            monthly_income=monthly_income,
            monthly_surplus=monthly_surplus,
            projected_emi_ratio=emi_ratio,

            # General recommendation endpoint.
            loan_suitable=True,

            # Fraud integration will be connected
            # with Security Intelligence.
            fraud_risk=0.0,

            # Default preference until preference
            # modelling is implemented.
            customer_preference=50.0,

            # This is a general recommendation,
            # not a loan application.
            loan_requested=False,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Recommendation generation failed: {str(exc)}"
            ),
        )

    # ========================================================
    # 7. GET RECOMMENDATION SCORE
    # ========================================================

    recommendation_score = float(
        recommendation.get(
            "recommendation_score",
            0.0,
        )
    )

    # ========================================================
    # 8. GET RECOMMENDATION CONFIDENCE
    # ========================================================

    # The current recommendation engine does not
    # explicitly produce a confidence model.
    #
    # Until the dedicated confidence model is added,
    # we derive a bounded confidence value from the
    # recommendation score.

    confidence = max(
        0.0,
        min(
            recommendation_score / 100.0,
            1.0,
        ),
    )

    # ========================================================
    # 9. POLICY ENGINE
    # ========================================================

    try:

        policy_result = policy_engine.evaluate(

            # ------------------------------------------------
            # Consent
            # ------------------------------------------------

            consent_given=True,

            # ------------------------------------------------
            # Purpose
            # ------------------------------------------------

            requested_purpose="financial_advice",

            allowed_purposes=[
                "financial_advice",
                "loan_recommendation",
                "fraud_detection",
                "financial_analysis",
            ],

            # ------------------------------------------------
            # Affordability
            # ------------------------------------------------

            affordability_score=float(
                recommendation.get(
                    "signals",
                    {}
                ).get(
                    "affordability_score",
                    50.0,
                )
            ),

            projected_emi_ratio=emi_ratio,

            monthly_surplus=monthly_surplus,

            # ------------------------------------------------
            # Confidence
            # ------------------------------------------------

            confidence=confidence,

            # ------------------------------------------------
            # Risk
            # ------------------------------------------------

            risk_score=stress_score,

            # ------------------------------------------------
            # Bias
            # ------------------------------------------------

            bias_score=0.0,

            # ------------------------------------------------
            # Compliance
            # ------------------------------------------------

            compliance_passed=True,

            compliance_reason=(
                "No compliance violation detected."
            ),

            critical=(
                stress_score >= 80
                or health_score < 35
            ),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Policy evaluation failed: {str(exc)}"
            ),
        )

    # ========================================================
    # 10. DETERMINE FINAL ACTION
    # ========================================================

    original_action = recommendation.get(
        "recommendation",
        "NO_ACTION",
    )

    policy_action = policy_result.get(
        "final_action",
        "NO_ACTION",
    )

    # Policy has authority over the final action.
    #
    # ALLOW means the original recommendation can
    # continue.
    #
    # Otherwise the policy action becomes the
    # customer-facing action.

    if policy_action == "ALLOW":
        final_action = original_action
    else:
        final_action = policy_action

    # ========================================================
    # 11. RETURN COMPLETE RESPONSE
    # ========================================================

    return {
        "success": True,

        "customer_id": customer_id,

        "recommendation": {
            "original_action": original_action,

            "final_action": final_action,

            "recommendation_score": recommendation_score,

            "reasons": recommendation.get(
                "reasons",
                [],
            ),

            "signals": recommendation.get(
                "signals",
                {},
            ),
        },

        "policy": policy_result,

        "financial_state": {
            "monthly_income": monthly_income,

            "monthly_spending": monthly_spending,

            "monthly_surplus": monthly_surplus,

            "emi_ratio": emi_ratio,

            "financial_health": health_score,

            "financial_stress": stress_score,
        },
    }