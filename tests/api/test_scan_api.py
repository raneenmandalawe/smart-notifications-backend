from fastapi.testclient import TestClient

from app.main import app


def test_scan_endpoint_returns_items(monkeypatch):
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

    monkeypatch.setattr("app.routes.scan.run_scan", fake_run_scan)

    client = TestClient(app)
    response = client.post("/scan")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 1
    assert payload["items"][0]["invoice_id"] == "INV-200"


def test_scan_endpoint_handles_errors(monkeypatch):
    def raise_error():
        raise RuntimeError("ERPNext unavailable")

    monkeypatch.setattr("app.routes.scan.run_scan", raise_error)

    client = TestClient(app)
    response = client.post("/scan")

    assert response.status_code == 503
    assert response.json()["detail"] == "ERPNext service unavailable"
