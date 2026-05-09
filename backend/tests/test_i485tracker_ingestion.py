from datetime import date, datetime, timezone

import pytest

from app.domain.models import CaseStatus
from app.ingestion.i485tracker import load_i485tracker_mock_records, make_i485tracker_mock_source, parse_i485tracker_cases, parse_i485tracker_json, parse_iso_date


def test_parse_i485tracker_cases_maps_mock_shape() -> None:
    source = make_i485tracker_mock_source(checked_at=datetime(2026, 5, 8, tzinfo=timezone.utc))
    payload = [
        {
            "id": "52df67db-336d-4592-b8bf-4872fc5cec1f",
            "pd": "2023-07-07",
            "cat": "EB2 NIW",
            "filed": "2025-06-02",
            "receipt": "2025-06-03",
            "receipt_num": "IOE09340xxxxx",
            "bio": "2025-07-03",
            "ead": "2025-07-04",
            "ap": None,
            "field_office": "NBC",
            "fo_transfer_date": None,
            "silent": ["2025-12-31"],
            "gc_approved": "2026-02-02",
            "gc_received": None,
            "interview": None,
            "coc": "39 COC",
            "rfe": "None",
            "region": "ROW",
            "notes": "sample note",
            "last_updated": "2026-05-07",
            "created_at": "2026-05-07T04:21:51.738327+00:00",
            "has_password": False,
        }
    ]

    result = parse_i485tracker_cases(payload, source)

    assert result.errors == []
    assert len(result.records) == 1
    record = result.records[0]
    assert record.id == "52df67db-336d-4592-b8bf-4872fc5cec1f"
    assert record.pd == date(2023, 7, 7)
    assert record.cat == "EB2 NIW"
    assert record.filed == date(2025, 6, 2)
    assert record.receipt_block == "IOE09340"
    assert record.silent == [date(2025, 12, 31)]
    assert record.gc_approved == date(2026, 2, 2)
    assert record.processing_days == 245
    assert record.status == CaseStatus.APPROVED
    assert record.source_id == "source-i485tracker-mock-v0"


def test_load_i485tracker_mock_records_loads_local_fixture() -> None:
    result = load_i485tracker_mock_records()

    assert result.errors == []
    assert len(result.records) == 3
    assert {record.cat for record in result.records} == {"EB1", "EB2 NIW"}
    assert any(record.status == CaseStatus.APPROVED for record in result.records)


def test_parse_i485tracker_json_collects_invalid_cases_without_mixing_them() -> None:
    source = make_i485tracker_mock_source()
    payload = '[{"id":"ok","cat":"EB1","filed":"2026-04-01"},{"id":"bad","cat":"","filed":"2026-04-01"}]'

    result = parse_i485tracker_json(payload, source)

    assert len(result.records) == 1
    assert len(result.errors) == 1
    assert result.errors[0].index == 1
    assert "cat is required" in result.errors[0].reason


def test_parse_i485tracker_json_requires_array_payload() -> None:
    source = make_i485tracker_mock_source()

    with pytest.raises(ValueError, match="JSON array"):
        parse_i485tracker_json('{"id":"not-array"}', source)


def test_parse_iso_date_reports_invalid_field() -> None:
    with pytest.raises(ValueError, match="invalid filed date: 1025-10-06"):
        parse_iso_date("1025-10-06", field_name="filed")
