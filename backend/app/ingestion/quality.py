from collections import Counter
from datetime import datetime, timezone
from statistics import mean, median

from pydantic import BaseModel, Field

from app.domain.models import PrivacyRule, TimelineRecord


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


class InvalidRowSample(BaseModel):
    index: int
    reason: str
    fields_present: list[str] = Field(default_factory=list)


class CohortReadinessSummary(BaseModel):
    cohort_key_fields: list[str] = Field(default_factory=lambda: ["cat", "field_office"])
    total_cohorts: int = 0
    publishable_cohorts: int = 0
    small_cohorts: int = 0
    percentile_ready_cohorts: int = 0
    largest_cohort_size: int = 0


class ValidationGateReport(BaseModel):
    quality: TimelineQualityReport
    invalid_records: int
    invalid_record_ratio: float
    invalid_samples: list[InvalidRowSample] = Field(default_factory=list)
    normalized_mapping_fields: list[str] = Field(default_factory=list)
    cohort_readiness: CohortReadinessSummary = Field(default_factory=CohortReadinessSummary)
    public_dashboard_ready: bool
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


def build_validation_gate_report(
    records: list[TimelineRecord],
    errors: list[object] | None = None,
    rule: PrivacyRule | None = None,
    invalid_sample_size: int = 5,
    invalid_ratio_warning_threshold: float = 0.05,
) -> ValidationGateReport:
    active_rule = rule or PrivacyRule()
    active_errors = errors or []
    quality = build_timeline_quality_report(records)
    cohort_readiness = _build_cohort_readiness(records, active_rule)
    invalid_ratio = round(len(active_errors) / (len(records) + len(active_errors)), 4) if records or active_errors else 0

    blockers: list[str] = []
    warnings: list[str] = []

    if quality.total_records == 0:
        blockers.append("검증 가능한 normalized record가 없습니다.")
    if quality.date_quality.missing_category > 0:
        blockers.append("category가 없는 record가 있어 cohort 기준을 만들 수 없습니다.")
    if cohort_readiness.publishable_cohorts == 0:
        blockers.append("minimum cohort size를 만족하는 public aggregate cohort가 없습니다.")

    if active_errors:
        warnings.append("invalid raw row가 있어 sample 검토가 필요합니다.")
    if invalid_ratio > invalid_ratio_warning_threshold:
        warnings.append("invalid raw row 비율이 warning threshold를 초과했습니다.")
    if quality.date_quality.missing_field_office > 0:
        warnings.append("field office가 없는 record는 field-office cohort에서 제외될 수 있습니다.")
    if cohort_readiness.percentile_ready_cohorts == 0:
        warnings.append("percentile을 공개할 만큼 충분한 cohort가 아직 없습니다.")

    return ValidationGateReport(
        quality=quality,
        invalid_records=len(active_errors),
        invalid_record_ratio=invalid_ratio,
        invalid_samples=_invalid_samples(active_errors, invalid_sample_size),
        normalized_mapping_fields=[
            "id",
            "pd",
            "cat",
            "filed",
            "receipt",
            "receipt_block",
            "bio",
            "ead",
            "ap",
            "field_office",
            "fo_transfer_date",
            "silent",
            "gc_approved",
            "gc_received",
            "interview",
            "coc",
            "rfe",
            "region",
            "notes",
            "last_updated",
            "created_at",
            "has_password",
            "source_id",
        ],
        cohort_readiness=cohort_readiness,
        public_dashboard_ready=not blockers,
        blockers=blockers,
        warnings=warnings,
    )


def _build_cohort_readiness(records: list[TimelineRecord], rule: PrivacyRule) -> CohortReadinessSummary:
    cohort_counts = Counter((record.cat, record.field_office) for record in records if record.cat and record.field_office)
    sizes = list(cohort_counts.values())
    return CohortReadinessSummary(
        total_cohorts=len(sizes),
        publishable_cohorts=sum(1 for size in sizes if size >= rule.minimum_cohort_size),
        small_cohorts=sum(1 for size in sizes if size < rule.minimum_cohort_size),
        percentile_ready_cohorts=sum(1 for size in sizes if size >= rule.minimum_percentile_size),
        largest_cohort_size=max(sizes) if sizes else 0,
    )


def _invalid_samples(errors: list[object], limit: int) -> list[InvalidRowSample]:
    samples: list[InvalidRowSample] = []
    for error in errors[:limit]:
        index = getattr(error, "index", 0)
        reason = getattr(error, "reason", str(error))
        raw_case = getattr(error, "case", {}) or {}
        fields_present = sorted(str(key) for key, value in raw_case.items() if value not in (None, ""))
        samples.append(InvalidRowSample(index=index, reason=reason, fields_present=fields_present))
    return samples
