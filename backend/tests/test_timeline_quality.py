from datetime import date, timedelta

from app.domain.models import TimelineRecord
from app.ingestion.i485tracker import load_i485tracker_mock_records
from app.ingestion.i485tracker import TrackerCaseValidationError
from app.ingestion.quality import build_timeline_quality_report, build_validation_gate_report


def test_build_quality_report_from_small_mock_fixture() -> None:
    result = load_i485tracker_mock_records()

    report = build_timeline_quality_report(result.records)

    assert report.total_records == 3
    assert report.approved_records == 1
    assert report.pending_records == 2
    assert report.category_counts == {"EB2 NIW": 2, "EB1": 1}
    assert report.average_processing_days == 245
    assert report.date_quality.missing_category == 0


def test_quality_report_scales_to_larger_synthetic_dataset() -> None:
    filed = date(2026, 1, 1)
    records = [
        TimelineRecord(
            id=f"synthetic-{index}",
            cat="EB2 NIW" if index % 2 == 0 else "EB1",
            filed=filed,
            gc_approved=filed + timedelta(days=30 + index),
            field_office="NBC" if index % 3 else "Dallas, TX",
        )
        for index in range(100)
    ]

    report = build_timeline_quality_report(records)

    assert report.total_records == 100
    assert report.approved_records == 100
    assert report.category_counts["EB2 NIW"] == 50
    assert report.category_counts["EB1"] == 50
    assert report.min_processing_days == 30
    assert report.max_processing_days == 129


def test_validation_gate_blocks_small_mock_fixture_for_public_dashboard() -> None:
    result = load_i485tracker_mock_records()

    report = build_validation_gate_report(result.records, result.errors)

    assert report.public_dashboard_ready is False
    assert report.quality.total_records == 3
    assert report.cohort_readiness.publishable_cohorts == 0
    assert "minimum cohort size" in report.blockers[0]
    assert "percentile" in " ".join(report.warnings)


def test_validation_gate_allows_larger_publishable_cohort() -> None:
    filed = date(2026, 1, 1)
    records = [
        TimelineRecord(
            id=f"publishable-{index}",
            cat="EB2 NIW",
            filed=filed,
            gc_approved=filed + timedelta(days=60 + index),
            field_office="NBC",
        )
        for index in range(20)
    ]

    report = build_validation_gate_report(records)

    assert report.public_dashboard_ready is True
    assert report.cohort_readiness.publishable_cohorts == 1
    assert report.cohort_readiness.percentile_ready_cohorts == 1
    assert report.blockers == []


def test_validation_gate_keeps_invalid_row_samples_reviewable() -> None:
    filed = date(2026, 1, 1)
    records = [
        TimelineRecord(
            id=f"valid-{index}",
            cat="EB2 NIW",
            filed=filed,
            gc_approved=filed + timedelta(days=40 + index),
            field_office="NBC",
        )
        for index in range(10)
    ]
    errors = [
        TrackerCaseValidationError(
            index=11,
            reason="invalid filed date: 3026-01-01",
            case={"id": "bad-date", "cat": "EB2 NIW", "filed": "3026-01-01"},
        )
    ]

    report = build_validation_gate_report(records, errors)

    assert report.public_dashboard_ready is True
    assert report.invalid_records == 1
    assert report.invalid_record_ratio == 0.0909
    assert report.invalid_samples[0].index == 11
    assert report.invalid_samples[0].fields_present == ["cat", "filed", "id"]
    assert "invalid raw row" in report.warnings[0]
