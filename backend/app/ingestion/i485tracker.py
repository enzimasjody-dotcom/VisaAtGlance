import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ValidationError

from app.domain.models import SourceKind, SourceRecord, TimelineRecord

DEFAULT_MOCK_CASES_PATH = Path(__file__).with_name("mock_data") / "i485tracker_cases.sample.json"


class TrackerCaseValidationError(BaseModel):
    index: int
    reason: str
    case: dict[str, Any] = Field(default_factory=dict)


class TrackerIngestionResult(BaseModel):
    source: SourceRecord
    records: list[TimelineRecord] = Field(default_factory=list)
    errors: list[TrackerCaseValidationError] = Field(default_factory=list)


def make_i485tracker_mock_source(
    source_id: str = "source-i485tracker-mock-v0",
    checked_at: datetime | None = None,
) -> SourceRecord:
    return SourceRecord(
        id=source_id,
        source_kind=SourceKind.MANUAL,
        title="Local i485tracker-like development fixture",
        checked_at=checked_at or datetime.now(timezone.utc),
        limitation="Local mock fixture derived from observed public shape. Not a production data source.",
        is_official=False,
    )


def load_i485tracker_mock_records(path: Path | None = None, source: SourceRecord | None = None) -> TrackerIngestionResult:
    fixture_path = path or DEFAULT_MOCK_CASES_PATH
    active_source = source or make_i485tracker_mock_source()
    return parse_i485tracker_json(fixture_path.read_text(), active_source)


def parse_i485tracker_json(json_text: str, source: SourceRecord) -> TrackerIngestionResult:
    payload = json.loads(json_text)
    if not isinstance(payload, list):
        raise ValueError("i485tracker-like payload must be a JSON array")
    return parse_i485tracker_cases(payload, source)


def parse_i485tracker_cases(cases: list[dict[str, Any]], source: SourceRecord) -> TrackerIngestionResult:
    records: list[TimelineRecord] = []
    errors: list[TrackerCaseValidationError] = []

    for index, case in enumerate(cases):
        try:
            records.append(i485tracker_case_to_timeline_record(case, source_id=source.id, fallback_index=index))
        except (ValueError, ValidationError) as exc:
            errors.append(TrackerCaseValidationError(index=index, reason=str(exc), case=case))

    return TrackerIngestionResult(source=source, records=records, errors=errors)


def i485tracker_case_to_timeline_record(case: dict[str, Any], source_id: str, fallback_index: int) -> TimelineRecord:
    cat = _clean_text(case.get("cat"))
    if not cat:
        raise ValueError("cat is required")

    return TimelineRecord(
        id=_clean_text(case.get("id")) or f"{source_id}:case-{fallback_index}",
        pd=parse_iso_date(case.get("pd"), field_name="pd"),
        cat=cat,
        filed=parse_iso_date(case.get("filed"), field_name="filed"),
        receipt=parse_iso_date(case.get("receipt"), field_name="receipt"),
        receipt_block=_safe_receipt_block(case.get("receipt_num")),
        bio=parse_iso_date(case.get("bio"), field_name="bio"),
        ead=parse_iso_date(case.get("ead"), field_name="ead"),
        ap=parse_iso_date(case.get("ap"), field_name="ap"),
        field_office=_clean_text(case.get("field_office")),
        fo_transfer_date=parse_iso_date(case.get("fo_transfer_date"), field_name="fo_transfer_date"),
        silent=[date_value for date_value in (parse_iso_date(value, field_name="silent") for value in case.get("silent") or []) if date_value is not None],
        gc_approved=parse_iso_date(case.get("gc_approved"), field_name="gc_approved"),
        gc_received=parse_iso_date(case.get("gc_received"), field_name="gc_received"),
        interview=parse_iso_date(case.get("interview"), field_name="interview"),
        coc=_clean_text(case.get("coc")) or "None",
        rfe=_clean_text(case.get("rfe")) or "None",
        region=_clean_text(case.get("region")),
        notes=_clean_text(case.get("notes")),
        last_updated=parse_iso_date(case.get("last_updated"), field_name="last_updated"),
        created_at=parse_iso_datetime(case.get("created_at")) or datetime.now(timezone.utc),
        has_password=bool(case.get("has_password")),
        source_id=source_id,
    )


def parse_iso_date(value: Any, *, field_name: str) -> date | None:
    clean_value = _clean_text(value)
    if not clean_value:
        return None
    try:
        parsed = date.fromisoformat(clean_value)
    except ValueError as exc:
        raise ValueError(f"invalid {field_name} date: {clean_value}") from exc
    if parsed.year < 2000 or parsed.year > 2100:
        raise ValueError(f"invalid {field_name} date: {clean_value}")
    return parsed


def parse_iso_datetime(value: Any) -> datetime | None:
    clean_value = _clean_text(value)
    if not clean_value:
        return None
    try:
        return datetime.fromisoformat(clean_value)
    except ValueError:
        return None


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _safe_receipt_block(value: Any) -> str | None:
    text = _clean_text(value)
    if text is None:
        return None
    return text[:8]
