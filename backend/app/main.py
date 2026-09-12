from fastapi import FastAPI

from app.api.customers import router as customer_router
from app.api.recommendations import router as recommendation_router
from app.api.loans import router as loan_router
from app.api.incidents import router as incident_router


app = FastAPI(
    title="FinGuru API",
    description="AI-powered Personal Financial Copilot",
    version="1.0.0",
)


# ============================================================
# API ROUTERS
# ============================================================

app.include_router(customer_router)
app.include_router(recommendation_router)
app.include_router(loan_router)
app.include_router(incident_router)


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
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FinGuru API",
    }