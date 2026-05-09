from datetime import date, datetime, timezone
from statistics import mean, median

from app.domain.models import CohortSummary, PrivacyRule, TimelineRecord
from app.domain.privacy import PERCENTILE_FIELD, RECENT_TREND_FIELD, should_show_percentile, should_show_recent_trend, suppressed_fields_for


def summarize_cohort(
    records: list[TimelineRecord],
    cohort_key: dict[str, str],
    rule: PrivacyRule | None = None,
    user_record: TimelineRecord | None = None,
    recent_since: date | None = None,
) -> CohortSummary:
    active_rule = rule or PrivacyRule()
    processing_days = [record.processing_days for record in records if record.processing_days is not None]
    sample_size = len(records)
    suppressed_fields = suppressed_fields_for(sample_size, active_rule)

    recent_approval_count = _recent_approval_count(records, recent_since)
    if not should_show_recent_trend(sample_size, active_rule):
        recent_approval_count = None

    user_percentile = _user_percentile(processing_days, user_record)
    if not should_show_percentile(sample_size, active_rule):
        user_percentile = None
    elif user_percentile is None and PERCENTILE_FIELD not in suppressed_fields:
        suppressed_fields.append(PERCENTILE_FIELD)

    if recent_approval_count is None and RECENT_TREND_FIELD not in suppressed_fields:
        suppressed_fields.append(RECENT_TREND_FIELD)

    return CohortSummary(
        cohort_key=cohort_key,
        sample_size=sample_size,
        average_processing_days=round(mean(processing_days), 2) if processing_days else None,
        median_processing_days=round(float(median(processing_days)), 2) if processing_days else None,
        user_percentile=user_percentile,
        recent_approval_count=recent_approval_count,
        suppressed_fields=suppressed_fields,
        source_ids=sorted({record.source_id for record in records if record.source_id}),
        computed_at=datetime.now(timezone.utc),
    )


def _recent_approval_count(records: list[TimelineRecord], recent_since: date | None) -> int | None:
    if recent_since is None:
        return None
    return sum(1 for record in records if record.gc_approved is not None and record.gc_approved >= recent_since)


def _user_percentile(processing_days: list[int], user_record: TimelineRecord | None) -> float | None:
    user_days = user_record.processing_days if user_record else None
    if user_days is None or not processing_days:
        return None
    completed_no_slower = sum(1 for days in processing_days if days <= user_days)
    return round((completed_no_slower / len(processing_days)) * 100, 2)
