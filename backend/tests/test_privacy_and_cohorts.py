from datetime import date, timedelta

from app.domain.cohorts import summarize_cohort
from app.domain.models import PrivacyRule, RecordVisibility, TimelineRecord
from app.domain.privacy import can_expose_row_preview, should_show_percentile, suppressed_fields_for


def _approved_record(index: int, processing_days: int, source_id: str = "source-apr-26") -> TimelineRecord:
    received = date(2026, 4, 1)
    return TimelineRecord(
        id=f"row-{index}",
        category="EB2 NIW",
        i485_received_date=received,
        gc_approved_date=received + timedelta(days=processing_days),
        lockbox="Dallas, TX",
        source_id=source_id,
    )


def test_small_cohort_suppresses_percentile_and_recent_trend() -> None:
    rule = PrivacyRule(minimum_percentile_size=20, minimum_recent_trend_size=10)
    records = [_approved_record(index, 20 + index) for index in range(5)]
    user_record = _approved_record(99, 23)

    summary = summarize_cohort(
        records,
        cohort_key={"category": "EB2 NIW", "lockbox": "Dallas, TX"},
        rule=rule,
        user_record=user_record,
        recent_since=date(2026, 4, 20),
    )

    assert summary.sample_size == 5
    assert summary.average_processing_days == 22
    assert summary.user_percentile is None
    assert summary.recent_approval_count is None
    assert "user_percentile" in summary.suppressed_fields
    assert "recent_approval_count" in summary.suppressed_fields
    assert "row_level_public_preview" in summary.suppressed_fields


def test_sufficient_cohort_allows_percentile_and_recent_trend() -> None:
    rule = PrivacyRule(minimum_percentile_size=20, minimum_recent_trend_size=10)
    records = [_approved_record(index, 10 + index) for index in range(20)]
    user_record = _approved_record(99, 19)

    summary = summarize_cohort(
        records,
        cohort_key={"category": "EB2 NIW", "lockbox": "Dallas, TX"},
        rule=rule,
        user_record=user_record,
        recent_since=date(2026, 4, 20),
    )

    assert summary.sample_size == 20
    assert summary.average_processing_days == 19.5
    assert summary.median_processing_days == 19.5
    assert summary.user_percentile == 50
    assert summary.recent_approval_count == 11
    assert "user_percentile" not in summary.suppressed_fields
    assert "recent_approval_count" not in summary.suppressed_fields
    assert summary.source_ids == ["source-apr-26"]


def test_privacy_rule_blocks_row_level_preview_by_default() -> None:
    rule = PrivacyRule()
    record = TimelineRecord(
        id="public-looking-row",
        category="EB2 NIW",
        visibility=RecordVisibility.PUBLIC_PREVIEW,
    )

    assert can_expose_row_preview(record, rule) is False
    assert "row_level_public_preview" in suppressed_fields_for(25, rule)
    assert should_show_percentile(25, rule) is True
