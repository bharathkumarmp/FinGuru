from fastapi import FastAPI

from app.api.customers import router as customer_router
from app.api.recommendations import router as recommendation_router
from app.api.loans import router as loan_router
from app.api.incidents import router as incident_router
from app.api.consent import router as consent_router
from app.api.offers import router as offer_router
from app.api.copilot import router as copilot_router


# ============================================================
# FINGURU APPLICATION
# ============================================================

app = FastAPI(
    title="FinGuru API",
    description="AI-powered Personal Financial Copilot",
    version="1.0.0",
)


# ============================================================
# API ROUTERS
# ============================================================

# Customer 360
app.include_router(customer_router)

# Financial recommendations
app.include_router(recommendation_router)

# Loan simulation and risk
app.include_router(loan_router)

# Security incidents
app.include_router(incident_router)

# Privacy and consent
app.include_router(consent_router)

# Personalized offers
app.include_router(offer_router)

# AI Copilot + RAG
app.include_router(copilot_router)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "name": "FinGuru",
        "description": "AI-powered Personal Financial Copilot",
        "status": "online",
        "version": "1.0.0",
        "architecture": {
            "customer_360": True,
            "financial_intelligence": True,
            "security_intelligence": True,
            "recommendation_engine": True,
            "personalized_offers": True,
            "rag": True,
            "ai_copilot": True,
            "privacy_guardrails": True,
        },
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FinGuru API",
        "version": "1.0.0",
    }