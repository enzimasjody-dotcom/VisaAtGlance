from collections import Counter
from datetime import datetime, timezone
from statistics import mean, median

from pydantic import BaseModel, Field

from app.domain.models import TimelineRecord


class DateQualitySummary(BaseModel):
    missing_filed: int = 0
    missing_category: int = 0
    missing_field_office: int = 0
    approved_without_filed: int = 0
    negative_processing_days: int = 0


class TimelineQualityReport(BaseModel):
    total_records: int
    approved_records: int
    pending_records: int
    category_counts: dict[str, int] = Field(default_factory=dict)
    status_counts: dict[str, int] = Field(default_factory=dict)
    field_office_counts: dict[str, int] = Field(default_factory=dict)
    average_processing_days: float | None = None
    median_processing_days: float | None = None
    min_processing_days: int | None = None
    max_processing_days: int | None = None
    date_quality: DateQualitySummary = Field(default_factory=DateQualitySummary)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


def build_timeline_quality_report(records: list[TimelineRecord]) -> TimelineQualityReport:
    processing_days = [record.processing_days for record in records if record.processing_days is not None]
    date_quality = DateQualitySummary(
        missing_filed=sum(1 for record in records if record.filed is None),
        missing_category=sum(1 for record in records if not record.cat),
        missing_field_office=sum(1 for record in records if not record.field_office),
        approved_without_filed=sum(1 for record in records if record.gc_approved is not None and record.filed is None),
        negative_processing_days=sum(1 for record in records if record.gc_approved is not None and record.filed is not None and record.gc_approved < record.filed),
    )

    return TimelineQualityReport(
        total_records=len(records),
        approved_records=sum(1 for record in records if record.gc_approved is not None),
        pending_records=sum(1 for record in records if record.gc_approved is None),
        category_counts=dict(Counter(record.cat for record in records if record.cat)),
        status_counts=dict(Counter(record.status.value for record in records)),
        field_office_counts=dict(Counter(record.field_office for record in records if record.field_office).most_common(20)),
        average_processing_days=round(mean(processing_days), 2) if processing_days else None,
        median_processing_days=round(float(median(processing_days)), 2) if processing_days else None,
        min_processing_days=min(processing_days) if processing_days else None,
        max_processing_days=max(processing_days) if processing_days else None,
        date_quality=date_quality,
    )
