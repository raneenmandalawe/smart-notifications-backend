from tests.assertions.api_assertions import assert_json_has_keys, assert_status
from tests.assertions.decision_assertions import assert_decision_schema


def test_scan_endpoint_returns_items(monkeypatch, client):
    def fake_run_scan():
        return [
            {
                "invoice_id": "INV-200",
                "customer": "Nova",
                "days_overdue": 8,
                "amount": 500.0,
                "history_count": 0,
                "risk_level": "MEDIUM",
                "channels": ["email"],
                "status": "sent",
            }
        ]

    monkeypatch.setattr("app.routes.scan.scan_overdue", fake_run_scan)

    response = client.post("/scan")
    assert_status(response, 200)
    payload = response.json()
    assert_json_has_keys(payload, ["count", "items"])
    assert payload["count"] == 1
    assert_decision_schema(payload["items"][0])
    assert payload["items"][0]["invoice_id"] == "INV-200"


def test_scan_endpoint_handles_errors(monkeypatch, client):
    def raise_error():
        raise RuntimeError("ERPNext unavailable")

    monkeypatch.setattr("app.routes.scan.scan_overdue", raise_error)

    response = client.post("/scan")
    assert_status(response, 503)
    assert response.json()["detail"] == "ERPNext service unavailable"
