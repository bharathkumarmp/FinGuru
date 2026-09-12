from typing import Any, Dict, List, Optional


# ============================================================
# OFFER TYPES
# ============================================================

OFFER_TYPES = [
    "SAVINGS_PLAN",
    "EMERGENCY_FUND",
    "DEBT_SUPPORT",
    "INVESTMENT",
    "PERSONAL_LOAN",
    "INSURANCE",
    "FINANCIAL_EDUCATION",
]


# ============================================================
# LIFE EVENT → OFFER MAPPING
# ============================================================

LIFE_EVENT_OFFERS = {
    "SALARY_CREDITED": [
        "SAVINGS_PLAN",
        "EMERGENCY_FUND",
        "INVESTMENT",
    ],
    "INCOME_INCREASE": [
        "SAVINGS_PLAN",
        "INVESTMENT",
        "INSURANCE",
    ],
    "INCOME_DECREASE": [
        "EMERGENCY_FUND",
        "DEBT_SUPPORT",
        "FINANCIAL_EDUCATION",
    ],
    "SPENDING_SPIKE": [
        "FINANCIAL_EDUCATION",
        "SAVINGS_PLAN",
        "DEBT_SUPPORT",
    ],
    "LARGE_PURCHASE": [
        "EMERGENCY_FUND",
        "SAVINGS_PLAN",
    ],
    "BALANCE_DROP": [
        "EMERGENCY_FUND",
        "DEBT_SUPPORT",
        "FINANCIAL_EDUCATION",
    ],
    "NEW_BENEFICIARY": [
        "FINANCIAL_EDUCATION",
    ],
}


# ============================================================
# HELPER
# ============================================================

def clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> float:
    return max(
        minimum,
        min(value, maximum),
    )


# ============================================================
# BASE OFFER SCORE
# ============================================================

def calculate_offer_score(
    health_score: float,
    stress_score: float,
    monthly_surplus: float,
    savings_rate: float,
    emi_ratio: float,
    income_stability: float,
    offer_type: str,
) -> float:

    score = 0.0

    if offer_type == "SAVINGS_PLAN":

        if monthly_surplus > 0:
            score += 35

        if savings_rate < 0.20:
            score += 30

        if health_score >= 50:
            score += 20

        if stress_score < 60:
            score += 15

    elif offer_type == "EMERGENCY_FUND":

        if monthly_surplus > 0:
            score += 30

        if savings_rate < 0.15:
            score += 30

        if health_score < 65:
            score += 20

        if stress_score >= 40:
            score += 20

    elif offer_type == "DEBT_SUPPORT":

        if emi_ratio > 0.30:
            score += 35

        if monthly_surplus < 0:
            score += 35

        if stress_score >= 50:
            score += 20

        if health_score < 50:
            score += 10

    elif offer_type == "INVESTMENT":

        if monthly_surplus > 0:
            score += 30

        if savings_rate >= 0.20:
            score += 25

        if health_score >= 70:
            score += 30

        if stress_score < 30:
            score += 15

    elif offer_type == "PERSONAL_LOAN":

        if monthly_surplus > 0:
            score += 25

        if health_score >= 65:
            score += 30

        if stress_score < 40:
            score += 20

        if emi_ratio < 0.40:
            score += 15

        if income_stability >= 70:
            score += 10

    elif offer_type == "INSURANCE":

        if health_score >= 60:
            score += 30

        if monthly_surplus > 0:
            score += 25

        if stress_score < 50:
            score += 25

        if income_stability >= 60:
            score += 20

    elif offer_type == "FINANCIAL_EDUCATION":

        if health_score < 65:
            score += 30

        if stress_score >= 40:
            score += 30

        if monthly_surplus < 0:
            score += 25

        score += 15

    return clamp(score)


# ============================================================
# LIFE EVENT ADJUSTMENT
# ============================================================

def apply_life_event_adjustment(
    offer_score: float,
    offer_type: str,
    life_events: List[Dict[str, Any]],
) -> float:

    adjusted_score = offer_score

    for event in life_events:

        event_type = event.get(
            "event_type",
            "",
        )

        confidence = float(
            event.get(
                "confidence",
                1.0,
            )
        )

        confidence = clamp(
            confidence * 100.0
            if confidence <= 1.0
            else confidence
        ) / 100.0

        relevant_offers = LIFE_EVENT_OFFERS.get(
            event_type,
            [],
        )

        if offer_type in relevant_offers:

            # Maximum event boost = 20 points.
            boost = 20.0 * confidence

            adjusted_score += boost

    return clamp(adjusted_score)


# ============================================================
# SAFETY FILTER
# ============================================================

def apply_safety_filter(
    offers: List[Dict[str, Any]],
    health_score: float,
    stress_score: float,
    monthly_surplus: float,
    emi_ratio: float,
) -> List[Dict[str, Any]]:

    filtered_offers = []

    for offer in offers:

        offer_type = offer["offer_type"]

        # ----------------------------------------------------
        # Personal loan safety
        # ----------------------------------------------------

        if offer_type == "PERSONAL_LOAN":

            if monthly_surplus < 0:
                continue

            if stress_score >= 60:
                continue

            if health_score < 50:
                continue

            if emi_ratio >= 0.50:
                continue

        # ----------------------------------------------------
        # Investment safety
        # ----------------------------------------------------

        if offer_type == "INVESTMENT":

            if monthly_surplus <= 0:
                continue

            if stress_score >= 60:
                continue

            if health_score < 50:
                continue

        # ----------------------------------------------------
        # Insurance safety
        # ----------------------------------------------------

        if offer_type == "INSURANCE":

            if monthly_surplus <= 0:
                continue

            if stress_score >= 70:
                continue

        filtered_offers.append(offer)

    return filtered_offers


# ============================================================
# NEXT BEST OFFER
# ============================================================

def generate_next_best_offer(
    health_score: float,
    stress_score: float,
    monthly_surplus: float,
    savings_rate: float,
    emi_ratio: float,
    income_stability: float,
    consent_given: bool,
    life_events: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:

    if life_events is None:
        life_events = []

    # ========================================================
    # CONSENT GUARDRAIL
    # ========================================================

    if not consent_given:

        return {
            "offer": "NO_OFFER",
            "offer_score": 0.0,
            "reason": (
                "Customer consent is required before "
                "personalized financial offers can be generated."
            ),
            "offers": [],
            "life_events_considered": [],
        }

    # ========================================================
    # SEVERE FINANCIAL DISTRESS
    # ========================================================

    if (
        monthly_surplus < 0
        and stress_score >= 60
    ):

        return {
            "offer": "DEBT_SUPPORT",
            "offer_score": 90.0,
            "reason": (
                "Customer has negative monthly cash flow "
                "and elevated financial stress. Debt support "
                "and financial recovery should be prioritized "
                "over new financial products."
            ),
            "offers": [
                {
                    "offer_type": "DEBT_SUPPORT",
                    "score": 90.0,
                    "priority": "HIGH",
                    "reason": (
                        "Negative cash flow and elevated "
                        "financial stress detected."
                    ),
                },
                {
                    "offer_type": "FINANCIAL_EDUCATION",
                    "score": 80.0,
                    "priority": "HIGH",
                    "reason": (
                        "Financial guidance may help improve "
                        "cash-flow management."
                    ),
                },
            ],
            "life_events_considered": life_events,
        }

    # ========================================================
    # GENERATE CANDIDATES
    # ========================================================

    candidates = []

    for offer_type in OFFER_TYPES:

        base_score = calculate_offer_score(
            health_score=health_score,
            stress_score=stress_score,
            monthly_surplus=monthly_surplus,
            savings_rate=savings_rate,
            emi_ratio=emi_ratio,
            income_stability=income_stability,
            offer_type=offer_type,
        )

        adjusted_score = apply_life_event_adjustment(
            offer_score=base_score,
            offer_type=offer_type,
            life_events=life_events,
        )

        candidates.append(
            {
                "offer_type": offer_type,
                "score": round(
                    adjusted_score,
                    2,
                ),
            }
        )

    # ========================================================
    # SAFETY FILTER
    # ========================================================

    candidates = apply_safety_filter(
        offers=candidates,
        health_score=health_score,
        stress_score=stress_score,
        monthly_surplus=monthly_surplus,
        emi_ratio=emi_ratio,
    )

    # ========================================================
    # SORT
    # ========================================================

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    # ========================================================
    # NO OFFER
    # ========================================================

    if not candidates:

        return {
            "offer": "NO_OFFER",
            "offer_score": 0.0,
            "reason": (
                "No suitable financial offer passed "
                "the current safety criteria."
            ),
            "offers": [],
            "life_events_considered": life_events,
        }

    # ========================================================
    # BEST OFFER
    # ========================================================

    best_offer = candidates[0]

    # ========================================================
    # MINIMUM SCORE THRESHOLD
    # ========================================================

    if best_offer["score"] < 50:

        return {
            "offer": "NO_OFFER",
            "offer_score": best_offer["score"],
            "reason": (
                "No financial product currently has "
                "sufficient suitability."
            ),
            "offers": candidates[:3],
            "life_events_considered": life_events,
        }

    # ========================================================
    # PRIORITIES
    # ========================================================

    for index, offer in enumerate(candidates):

        if index == 0:
            offer["priority"] = "HIGH"

        elif index == 1:
            offer["priority"] = "MEDIUM"

        else:
            offer["priority"] = "LOW"

    # ========================================================
    # RETURN
    # ========================================================

    return {
        "offer": best_offer["offer_type"],
        "offer_score": best_offer["score"],
        "reason": (
            "Offer selected using the customer's financial "
            "health, stress, cash flow, savings, debt burden, "
            "income stability and detected life events."
        ),
        "offers": candidates[:5],
        "life_events_considered": life_events,
    }