from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ============================================================
# API ROUTERS
# ============================================================

from app.api.auth import router as auth_router

from app.api.ai import router as ai_router
from app.api.copilot import router as copilot_router
from app.api.recommendations import router as recommendations_router
from app.api.offers import router as offers_router
from app.api.loans import router as loans_router
from app.api.customers import router as customers_router
from app.api.accounts import router as accounts_router
from app.api.transactions import router as transactions_router
from app.api.financial_health import router as financial_health_router
from app.api.financial_stress import router as financial_stress_router
from app.api.fraud import router as fraud_router
from app.api.events import router as events_router
from app.api.incidents import router as incidents_router
from app.api.consent import router as consent_router


# ============================================================
# FINGURU AI APPLICATION
# ============================================================

app = FastAPI(
    title="FinGuru AI",
    description=(
        "AI-Powered Hyper-Personalized Banking "
        "Intelligence Platform for Bharat"
    ),
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "success": True,
        "application": "FinGuru AI",
        "version": "1.0.0",
        "status": "running",
        "message": (
            "AI-powered hyper-personalized banking platform"
        ),
        "architecture": (
            "Banking Data → Customer 360 → "
            "Financial Intelligence → Security Intelligence → "
            "Prescriptive Engine → Multi-Agent AI → "
            "Policy Guardrail → Communication"
        ),
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "success": True,
        "status": "healthy",
        "service": "FinGuru AI Backend",
        "version": "1.0.0",
    }


# ============================================================
# REGISTER API ROUTERS
# ============================================================


# ------------------------------------------------------------
# AUTHENTICATION
# ------------------------------------------------------------

app.include_router(
    auth_router
)


# ------------------------------------------------------------
# AI ORCHESTRATOR
# ------------------------------------------------------------

app.include_router(
    ai_router
)


# ------------------------------------------------------------
# CUSTOMER 360
# ------------------------------------------------------------

app.include_router(
    customers_router
)


# ------------------------------------------------------------
# ACCOUNTS
# ------------------------------------------------------------

app.include_router(
    accounts_router
)


# ------------------------------------------------------------
# FINANCIAL HEALTH
# ------------------------------------------------------------

app.include_router(
    financial_health_router
)


# ------------------------------------------------------------
# FINANCIAL STRESS
# ------------------------------------------------------------

app.include_router(
    financial_stress_router
)


# ------------------------------------------------------------
# TRANSACTIONS
# ------------------------------------------------------------

app.include_router(
    transactions_router
)


# ------------------------------------------------------------
# FRAUD DETECTION
# ------------------------------------------------------------

app.include_router(
    fraud_router
)


# ------------------------------------------------------------
# EVENTS
# ------------------------------------------------------------

app.include_router(
    events_router
)


# ------------------------------------------------------------
# RECOMMENDATIONS
# ------------------------------------------------------------

app.include_router(
    recommendations_router
)


# ------------------------------------------------------------
# PERSONALIZED OFFERS
# ------------------------------------------------------------

app.include_router(
    offers_router
)


# ------------------------------------------------------------
# LOAN SIMULATION
# ------------------------------------------------------------

app.include_router(
    loans_router
)


# ------------------------------------------------------------
# AI COPILOT
# ------------------------------------------------------------

app.include_router(
    copilot_router
)


# ------------------------------------------------------------
# SECURITY INCIDENTS
# ------------------------------------------------------------

app.include_router(
    incidents_router
)


# ------------------------------------------------------------
# CONSENT / PRIVACY
# ------------------------------------------------------------

app.include_router(
    consent_router
)


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup_event():

    print("=" * 65)
    print("                  FINGURU AI BACKEND")
    print("=" * 65)

    print("Application         : FinGuru AI")
    print("Version             : 1.0.0")
    print()

    # --------------------------------------------------------
    # CORE INTELLIGENCE
    # --------------------------------------------------------

    print("CORE INTELLIGENCE")
    print("-----------------")

    print("Customer 360         : ENABLED")
    print("Accounts             : ENABLED")
    print("Financial Health     : ENABLED")
    print("Financial Stress     : ENABLED")
    print("Digital Twin         : ENABLED")
    print("Life Events          : ENABLED")
    print("Loan Risk            : ENABLED")
    print("Recommendations      : ENABLED")
    print("Personalized Offers  : ENABLED")
    print()

    # --------------------------------------------------------
    # SECURITY INTELLIGENCE
    # --------------------------------------------------------

    print("SECURITY INTELLIGENCE")
    print("---------------------")

    print("Fraud Detection      : ENABLED")
    print("Transaction Anomaly  : ENABLED")
    print("UEBA                 : ENABLED")
    print("Identity Risk        : ENABLED")
    print("Threat Correlation   : ENABLED")
    print("Incident Response    : ENABLED")
    print("Audit Logging        : ENABLED")
    print()

    # --------------------------------------------------------
    # EVENT INTELLIGENCE
    # --------------------------------------------------------

    print("EVENT INTELLIGENCE")
    print("------------------")

    print("Event Publisher      : ENABLED")
    print("Event Consumer       : ENABLED")
    print("Event Handlers       : ENABLED")
    print("Event Processing     : ENABLED")
    print()

    # --------------------------------------------------------
    # AI PLATFORM
    # --------------------------------------------------------

    print("AI PLATFORM")
    print("-----------")

    print("Financial Agent       : ENABLED")
    print("Risk Agent            : ENABLED")
    print("Recommendation Agent : ENABLED")
    print("Communication Agent   : ENABLED")
    print("Multi-Agent AI        : ENABLED")
    print("Policy Guardrails     : ENABLED")
    print("RAG                   : ENABLED")
    print("AI Copilot            : ENABLED")
    print()

    # --------------------------------------------------------
    # API LAYER
    # --------------------------------------------------------

    print("API LAYER")
    print("---------")

    print("Authentication API    : ENABLED")
    print("AI Orchestrator       : ENABLED")
    print("Customer APIs         : ENABLED")
    print("Accounts API          : ENABLED")
    print("Financial Health API  : ENABLED")
    print("Financial Stress API  : ENABLED")
    print("Transaction API       : ENABLED")
    print("Fraud Detection API   : ENABLED")
    print("Events API            : ENABLED")
    print("Recommendation API    : ENABLED")
    print("Offers API            : ENABLED")
    print("Loan API              : ENABLED")
    print("Copilot API            : ENABLED")
    print("Incident API          : ENABLED")
    print("Consent API           : ENABLED")

    print("=" * 65)


# ============================================================
# SHUTDOWN
# ============================================================

@app.on_event("shutdown")
def shutdown_event():

    print("=" * 65)
    print("FinGuru AI Backend Shutdown")
    print("=" * 65)