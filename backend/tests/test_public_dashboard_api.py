from fastapi.testclient import TestClient

from app.main import app


def test_public_dashboard_endpoint_returns_aggregate_summary() -> None:
    client = TestClient(app)

    response = client.get("/dashboard/public")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_records"] == 3
    assert payload["approved_records"] == 1
    assert payload["pending_records"] == 2
    assert payload["processing_days"]["sample_size"] == 1
    assert payload["sources"][0]["source_id"] == "source-i485tracker-mock-v0"
    assert payload["sources"][0]["is_official"] is False
    assert "minimum cohort size" in " ".join(payload["warnings"])


def test_public_dashboard_endpoint_does_not_expose_row_level_fields() -> None:
    client = TestClient(app)

    response = client.get("/dashboard/public")

    payload_text = response.text
    assert "mock-eb2-approved-1" not in payload_text
    assert "receipt_block" not in payload_text
    assert "receipt_num" not in payload_text
    assert "notes" not in payload_text


def test_public_dashboard_endpoint_is_in_openapi_schema() -> None:
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/dashboard/public" in response.json()["paths"]
