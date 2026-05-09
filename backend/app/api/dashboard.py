from fastapi import APIRouter

from app.domain.dashboard import PublicDashboardSummary, build_public_dashboard_summary
from app.ingestion.i485tracker import load_i485tracker_mock_records

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/public", response_model=PublicDashboardSummary)
def public_dashboard() -> PublicDashboardSummary:
    result = load_i485tracker_mock_records()
    return build_public_dashboard_summary(result.records, sources=[result.source])
