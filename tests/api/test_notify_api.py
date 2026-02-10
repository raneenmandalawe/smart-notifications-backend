from tests.assertions.api_assertions import assert_status


def test_notify_sms_marks_invoice_sent(isolated_store, client, fixed_now):
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

    response = client.post("/notify/INV-100/sms")
    assert_status(response, 200)
    payload = response.json()
    assert payload["status"] == "sent"
    assert "sms" in payload["item"]["channels"]
    assert payload["item"]["status"] == "sent"
    assert payload["item"].get("last_sms_at") == fixed_now.isoformat()


def test_notify_sms_missing_invoice_returns_404(isolated_store, client):
    isolated_store.set_last_scan([])
    response = client.post("/notify/INV-404/sms")
    assert_status(response, 404)


def test_auto_toggle_on_off(client):
    enabled = client.post("/notify/auto/on")
    assert_status(enabled, 200)
    assert enabled.json()["enabled"] is True

    disabled = client.post("/notify/auto/off")
    assert_status(disabled, 200)
    assert disabled.json()["enabled"] is False
