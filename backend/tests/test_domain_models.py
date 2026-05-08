from datetime import date

from app.domain.models import CaseStatus, ContributionType, RecordVisibility, SourceKind, SourceRecord, TimelineRecord


def test_timeline_record_matches_apr_26_i485_columns() -> None:
    record = TimelineRecord(
        id="apr26-row-1",
        priority_date=date(2024, 3, 8),
        category="EB2 NIW",
        i485_mailed_date=date(2026, 4, 1),
        i485_received_date=date(2026, 4, 1),
        i485_receipt_date=date(2026, 4, 1),
        block_number="IOE09362",
        lockbox="Dallas, TX",
        biometric_date=date(2026, 4, 14),
        interview_status="Waived (04/15)",
        field_office_name="Jacksonville FO (Local)",
        field_office_transfer_date=date(2026, 4, 21),
        fta_updates="2x FTA0: 4/14/2026",
        silent_updates_after_biometrics="4/15, 4/21",
        country_of_concern="75 COC",
        applicant_group="ROW / Single",
        source_id="source-apr-26",
    )

    assert record.status == CaseStatus.PENDING
    assert record.processing_days is None
    assert record.contribution_type == ContributionType.SPREADSHEET
    assert record.visibility == RecordVisibility.AGGREGATE_ONLY


def test_approved_timeline_record_calculates_processing_days() -> None:
    record = TimelineRecord(
        id="approved-row",
        category="EB2 NIW",
        i485_received_date=date(2026, 4, 1),
        gc_approved_date=date(2026, 5, 1),
    )

    assert record.status == CaseStatus.APPROVED
    assert record.processing_days == 30


def test_source_record_keeps_sheet_freshness_metadata() -> None:
    source = SourceRecord(
        id="source-apr-26",
        source_kind=SourceKind.GOOGLE_SHEET,
        title="Apr '26 I-485 tracker tab",
        url="https://docs.google.com/spreadsheets/d/1Ty3k9RIrOp8CtPmGMR8m2Nmtk30jy5quJM3JTq8xlbs/edit",
        limitation="Crowd-sourced data can contain missing, duplicated, or user-edited rows.",
    )

    assert source.source_kind == SourceKind.GOOGLE_SHEET
    assert source.is_official is False
    assert source.limitation is not None
