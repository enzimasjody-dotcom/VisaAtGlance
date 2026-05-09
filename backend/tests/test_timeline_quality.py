from datetime import date, timedelta

from app.domain.models import TimelineRecord
from app.ingestion.i485tracker import load_i485tracker_mock_records
from app.ingestion.quality import build_timeline_quality_report


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
