import argparse
from pathlib import Path
import httpx

from app.ingestion.i485tracker import make_i485tracker_mock_source, parse_i485tracker_json
from app.ingestion.quality import build_timeline_quality_report

DEFAULT_URL = "https://i485tracker.opentoolkits.com/api/cases"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / ".data" / "i485tracker_cases.full.json"
DEFAULT_REPORT = Path(__file__).resolve().parents[1] / ".data" / "i485tracker_quality_report.json"


def fetch_json(url: str) -> str:
    response = httpx.get(url, headers={"User-Agent": "VisaAtGlance development data fetcher"}, timeout=30)
    response.raise_for_status()
    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch i485tracker-like full data into a local ignored cache.")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = fetch_json(args.url)
    args.output.write_text(payload)

    source = make_i485tracker_mock_source(source_id="source-i485tracker-full-local")
    result = parse_i485tracker_json(payload, source)
    report = build_timeline_quality_report(result.records).model_dump_json(indent=2)
    args.report.write_text(report)

    print(f"saved full data: {args.output}")
    print(f"saved quality report: {args.report}")
    print(f"records: {len(result.records)} errors: {len(result.errors)}")


if __name__ == "__main__":
    main()
