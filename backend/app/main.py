from fastapi import FastAPI

from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router

app = FastAPI(
    title="VisaAtGlance API",
    version="0.1.0",
    description="Backend API for VisaAtGlance data ingestion, cohort analysis, and privacy-safe dashboard data.",
)

app.include_router(health_router)
app.include_router(dashboard_router)
