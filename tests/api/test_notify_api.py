from fastapi.testclient import TestClient

from app.main import app


def test_notify_sms_marks_invoice_sent(isolated_store):
    isolated_store.set_last_scan(
        [
            {
                "invoice_id": "INV-100",
                "customer": "Orbit",
                "days_overdue": 20,
                "amount": 3200.0,
                "history_count": 2,
                "risk_level": "HIGH",
                "channels": [],
                "status": "skipped",
            }
        ]
    )

    client = TestClient(app)
    response = client.post("/notify/INV-100/sms")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "sent"
    assert "sms" in payload["item"]["channels"]
    assert payload["item"]["status"] == "sent"
    assert payload["item"].get("last_sms_at")


def test_notify_sms_missing_invoice_returns_404(isolated_store):
    isolated_store.set_last_scan([])

    client = TestClient(app)
    response = client.post("/notify/INV-404/sms")

    assert response.status_code == 404


def test_auto_toggle_on_off():
    client = TestClient(app)

    enabled = client.post("/notify/auto/on")
    assert enabled.status_code == 200
    assert enabled.json()["enabled"] is True

    disabled = client.post("/notify/auto/off")
    assert disabled.status_code == 200
    assert disabled.json()["enabled"] is False
