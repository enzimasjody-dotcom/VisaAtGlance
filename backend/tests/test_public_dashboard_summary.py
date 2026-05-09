from datetime import date, datetime, timedelta, timezone

from app.domain.dashboard import SUPPRESSED_BUCKET_LABEL, build_public_dashboard_summary
from app.domain.models import PrivacyRule, SourceKind, SourceRecord, TimelineRecord


def _record(index: int, cat: str = "EB2 NIW", field_office: str = "NBC", days: int | None = 40, source_id: str = "source-i485tracker-mock-v0") -> TimelineRecord:
    filed = date(2026, 1, 1)
    return TimelineRecord(
        id=f"case-{index}",
        cat=cat,
        filed=filed,
        gc_approved=filed + timedelta(days=days) if days is not None else None,
        field_office=field_office,
        notes="do not expose row notes",
        receipt_block="IOE12345",
        source_id=source_id,
    )


def test_public_dashboard_summary_exposes_only_aggregate_data() -> None:
    source = SourceRecord(
        id="source-i485tracker-mock-v0",
        source_kind=SourceKind.MANUAL,
        title="Local mock source",
        checked_at=datetime(2026, 5, 9, tzinfo=timezone.utc),
        limitation="Development fixture only.",
    )
    records = [_record(index, days=30 + index) for index in range(12)]

    summary = build_public_dashboard_summary(records, sources=[source], recent_since=date(2026, 2, 1))
    payload = summary.model_dump()

    assert summary.total_records == 12
    assert summary.approved_records == 12
    assert summary.pending_records == 0
    assert summary.processing_days.average_days == 35.5
    assert summary.processing_days.median_days == 35.5
    assert summary.category_counts[0].label == "EB2 NIW"
    assert summary.field_office_counts[0].label == "NBC"
    assert summary.cohorts[0].cohort_key == {"cat": "EB2 NIW", "field_office": "NBC"}
    assert summary.cohorts[0].recent_approval_count == 11
    assert summary.sources[0].sample_size == 12
    assert summary.sources[0].limitation == "Development fixture only."
    assert "case-" not in str(payload)
    assert "do not expose row notes" not in str(payload)
    assert "IOE12345" not in str(payload)


def test_public_dashboard_summary_suppresses_small_bucket_labels() -> None:
    rule = PrivacyRule(minimum_cohort_size=5, minimum_recent_trend_size=5, minimum_percentile_size=10)
    records = [_record(index, field_office="NBC") for index in range(5)]
    records.extend(_record(100 + index, field_office=f"Small FO {index}") for index in range(4))

    summary = build_public_dashboard_summary(records, rule=rule)

    assert summary.total_records == 9
    assert summary.suppressed_small_cohort_count == 4
    assert summary.field_office_counts[0].label == "NBC"
    assert summary.field_office_counts[1].label == SUPPRESSED_BUCKET_LABEL
    assert summary.field_office_counts[1].count == 4
    assert summary.field_office_counts[1].suppressed is True
    assert all("Small FO" not in bucket.label for bucket in summary.field_office_counts)
    assert len(summary.cohorts) == 1
    assert summary.cohorts[0].sample_size == 5
    assert "user_percentile" in summary.cohorts[0].suppressed_fields


def test_public_dashboard_summary_keeps_pending_status_and_processing_sample_separate() -> None:
    records = [_record(index, days=None) for index in range(3)]
    records.extend(_record(10 + index, days=20 + index) for index in range(5))

    summary = build_public_dashboard_summary(records, rule=PrivacyRule(minimum_cohort_size=3))
    status_counts = {bucket.label: bucket.count for bucket in summary.status_counts}

    assert summary.total_records == 8
    assert summary.approved_records == 5
    assert summary.pending_records == 3
    assert summary.processing_days.sample_size == 5
    assert status_counts["filed"] == 3
    assert status_counts["approved"] == 5
