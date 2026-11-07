
import json
from datetime import datetime
from pathlib import Path
from ipaddress import ip_address as parse_ip
from langchain.tools import tool


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_gateway_logs() -> list[dict]:
    """Load the synthetic gateway logs."""
    with open(DATA_DIR / "gateway_logs.json", "r") as file:
        return json.load(file)


@tool
def search_gateway_logs(
    ip_address: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    endpoint: str | None = None,
    status_code: int | None = None,
    limit: int = 100,
) -> dict:
    """Search gateway logs by IP, time range, endpoint, or status code.

    At least one filter must be provided. The start time is inclusive
    and the end time is exclusive. Results are limited to 100 events.
    """
    if not any([
        ip_address,
        start_time,
        end_time,
        endpoint,
        status_code is not None,
    ]):
        return {"error": "At least one filter must be provided."}

    if not 1 <= limit <= 100:
        return {"error": "Limit must be between 1 and 100."}

    try:
        if ip_address:
            parse_ip(ip_address)

        start = datetime.fromisoformat(
            start_time.replace("Z", "+00:00")
        ) if start_time else None

        end = datetime.fromisoformat(
            end_time.replace("Z", "+00:00")
        ) if end_time else None

        if start and end and start >= end:
            return {"error": "Start time must be before end time."}

        logs = load_gateway_logs()
        matches = []

        for event in logs:
            timestamp = datetime.fromisoformat(
                event["timestamp"].replace("Z", "+00:00")
            )

            if ip_address and event["ip_address"] != ip_address:
                continue

            if start and timestamp < start:
                continue

            if end and timestamp >= end:
                continue

            if endpoint and event["endpoint"] != endpoint:
                continue

            if (
                status_code is not None
                and event["status_code"] != status_code
            ):
                continue

            matches.append(event)

        return {
            "events": matches[:limit],
            "total_matches": len(matches),
        }

    except ValueError as error:
        return {"error": f"Invalid input: {error}"}

result = search_gateway_logs.invoke({
    "ip_address": "203.0.113.10",
    "status_code": 401,
})

print(result)

@tool
def lookup_ip_reputation(ip_address: str) -> dict:
    """Look up an IP address in the mock threat intelligence dataset."""
    try:
        parse_ip(ip_address)
    except ValueError:
        return {"error": "Invalid IP address."}

    threat_data = {
        "203.0.113.10": {
            "reputation": "suspicious",
            "threat_categories": ["brute_force"],
            "source": "mock_threat_intelligence",
        }
    }

    result = threat_data.get(ip_address)

    if result is None:
        return {
            "ip_address": ip_address,
            "reputation": "unknown",
            "threat_categories": [],
            "source": "mock_threat_intelligence",
        }

    return {
        "ip_address": ip_address,
        **result,
    }


@tool
def get_request_details(request_id: str) -> dict:
    """Retrieve the complete details of a gateway request by request ID."""
    logs = load_gateway_logs()

    for event in logs:
        if event["request_id"] == request_id:
            return event

    return {
        "error": f"Request {request_id} was not found."
    }
