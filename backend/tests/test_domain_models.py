from datetime import date

from app.domain.models import CaseStatus, ContributionType, RecordVisibility, SourceKind, SourceRecord, TimelineRecord


def test_timeline_record_uses_tracker_like_normalized_shape() -> None:
    record = TimelineRecord(
        id="apr26-row-1",
        pd=date(2024, 3, 8),
        cat="EB2 NIW",
        filed=date(2026, 4, 1),
        receipt=date(2026, 4, 1),
        receipt_block="IOE09362",
        bio=date(2026, 4, 14),
        field_office="Jacksonville FO (Local)",
        fo_transfer_date=date(2026, 4, 21),
        silent=[date(2026, 4, 15), date(2026, 4, 21)],
        coc="75 COC",
        region="ROW",
        applicant_group="Single",
        source_id="source-apr-26",
    )

    assert record.status == CaseStatus.BIOMETRICS_DONE
    assert record.processing_days is None
    assert record.contribution_type == ContributionType.SPREADSHEET
    assert record.visibility == RecordVisibility.AGGREGATE_ONLY


def test_approved_timeline_record_calculates_processing_days() -> None:
    record = TimelineRecord(
        id="approved-row",
        cat="EB2 NIW",
        filed=date(2026, 4, 1),
        gc_approved=date(2026, 5, 1),
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
