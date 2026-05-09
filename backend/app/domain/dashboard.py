from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from statistics import mean, median

from pydantic import BaseModel, Field

from app.domain.cohorts import summarize_cohort
from app.domain.models import PrivacyRule, SourceRecord, TimelineRecord

SUPPRESSED_BUCKET_LABEL = "suppressed_small_cohort"


class DashboardBucket(BaseModel):
    label: str
    count: int
    suppressed: bool = False


class ProcessingDaysSummary(BaseModel):
    sample_size: int
    average_days: float | None = None
    median_days: float | None = None
    min_days: int | None = None
    max_days: int | None = None


class PublicDashboardCohort(BaseModel):
    cohort_key: dict[str, str]
    sample_size: int
    average_processing_days: float | None = None
    median_processing_days: float | None = None
    recent_approval_count: int | None = None
    suppressed_fields: list[str] = Field(default_factory=list)


class DashboardSourceSummary(BaseModel):
    source_id: str
    title: str
    checked_at: datetime
    sample_size: int
    limitation: str | None = None
    is_official: bool = False


class PublicDashboardSummary(BaseModel):
    total_records: int
    approved_records: int
    pending_records: int
    category_counts: list[DashboardBucket] = Field(default_factory=list)
    field_office_counts: list[DashboardBucket] = Field(default_factory=list)
    status_counts: list[DashboardBucket] = Field(default_factory=list)
    processing_days: ProcessingDaysSummary
    cohorts: list[PublicDashboardCohort] = Field(default_factory=list)
    sources: list[DashboardSourceSummary] = Field(default_factory=list)
    suppressed_small_cohort_count: int = 0
    warnings: list[str] = Field(default_factory=list)
    computed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


def build_public_dashboard_summary(
    records: list[TimelineRecord],
    sources: list[SourceRecord] | None = None,
    rule: PrivacyRule | None = None,
    recent_since: date | None = None,
    top_limit: int = 10,
) -> PublicDashboardSummary:
    active_rule = rule or PrivacyRule()
    source_records = sources or []
    processing_days = [record.processing_days for record in records if record.processing_days is not None]
    cohort_groups = _group_by_public_cohort(records)
    publishable_cohorts = {
        key: cohort_records
        for key, cohort_records in cohort_groups.items()
        if len(cohort_records) >= active_rule.minimum_cohort_size
    }
    small_cohort_count = len(cohort_groups) - len(publishable_cohorts)

    warnings: list[str] = []
    if small_cohort_count:
        warnings.append("small cohort bucket은 public dashboard에서 개별 label을 숨깁니다.")
    if not publishable_cohorts:
        warnings.append("minimum cohort size를 만족하는 public cohort가 없습니다.")

    return PublicDashboardSummary(
        total_records=len(records),
        approved_records=sum(1 for record in records if record.gc_approved is not None),
        pending_records=sum(1 for record in records if record.gc_approved is None),
        category_counts=_privacy_safe_buckets((record.cat for record in records if record.cat), active_rule, top_limit),
        field_office_counts=_privacy_safe_buckets((record.field_office for record in records if record.field_office), active_rule, top_limit),
        status_counts=_count_buckets(record.status.value for record in records),
        processing_days=ProcessingDaysSummary(
            sample_size=len(processing_days),
            average_days=round(mean(processing_days), 2) if processing_days else None,
            median_days=round(float(median(processing_days)), 2) if processing_days else None,
            min_days=min(processing_days) if processing_days else None,
            max_days=max(processing_days) if processing_days else None,
        ),
        cohorts=_public_cohort_summaries(publishable_cohorts, active_rule, recent_since, top_limit),
        sources=_source_summaries(records, source_records),
        suppressed_small_cohort_count=small_cohort_count,
        warnings=warnings,
    )


def _group_by_public_cohort(records: list[TimelineRecord]) -> dict[tuple[str, str], list[TimelineRecord]]:
    groups: dict[tuple[str, str], list[TimelineRecord]] = defaultdict(list)
    for record in records:
        if record.cat and record.field_office:
            groups[(record.cat, record.field_office)].append(record)
    return dict(groups)


def _privacy_safe_buckets(values: object, rule: PrivacyRule, top_limit: int) -> list[DashboardBucket]:
    counter = Counter(values)
    visible = [(label, count) for label, count in counter.most_common() if count >= rule.minimum_cohort_size]
    suppressed_count = sum(count for count in counter.values() if count < rule.minimum_cohort_size)
    buckets = [DashboardBucket(label=str(label), count=count) for label, count in visible[:top_limit]]
    if suppressed_count:
        buckets.append(DashboardBucket(label=SUPPRESSED_BUCKET_LABEL, count=suppressed_count, suppressed=True))
    return buckets


def _count_buckets(values: object) -> list[DashboardBucket]:
    return [DashboardBucket(label=str(label), count=count) for label, count in Counter(values).most_common()]


def _public_cohort_summaries(
    cohorts: dict[tuple[str, str], list[TimelineRecord]],
    rule: PrivacyRule,
    recent_since: date | None,
    top_limit: int,
) -> list[PublicDashboardCohort]:
    ranked = sorted(cohorts.items(), key=lambda item: len(item[1]), reverse=True)[:top_limit]
    summaries: list[PublicDashboardCohort] = []
    for (cat, field_office), records in ranked:
        cohort_summary = summarize_cohort(
            records,
            cohort_key={"cat": cat, "field_office": field_office},
            rule=rule,
            recent_since=recent_since,
        )
        summaries.append(
            PublicDashboardCohort(
                cohort_key=cohort_summary.cohort_key,
                sample_size=cohort_summary.sample_size,
                average_processing_days=cohort_summary.average_processing_days,
                median_processing_days=cohort_summary.median_processing_days,
                recent_approval_count=cohort_summary.recent_approval_count,
                suppressed_fields=cohort_summary.suppressed_fields,
            )
        )
    return summaries


def _source_summaries(records: list[TimelineRecord], sources: list[SourceRecord]) -> list[DashboardSourceSummary]:
    source_counts = Counter(record.source_id for record in records if record.source_id)
    source_by_id = {source.id: source for source in sources}
    summaries: list[DashboardSourceSummary] = []
    for source_id, sample_size in source_counts.most_common():
        source = source_by_id.get(source_id)
        if source is None:
            continue
        summaries.append(
            DashboardSourceSummary(
                source_id=source.id,
                title=source.title,
                checked_at=source.checked_at,
                sample_size=sample_size,
                limitation=source.limitation,
                is_official=source.is_official,
            )
        )
    return summaries
