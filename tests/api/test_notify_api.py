from unittest.mock import patch

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


def test_notify_email_success(isolated_store, client, fixed_now):
    isolated_store.set_last_scan(
        [
            {
                "invoice_id": "INV-200",
                "customer": "Test Corp",
                "days_overdue": 15,
                "amount": 5000.0,
                "history_count": 1,
                "risk_level": "MEDIUM",
                "channels": [],
                "status": "skipped",
            }
        ]
    )

    with patch("app.controllers.notify_controller.smtp_send_email") as mock_smtp, patch(
        "app.controllers.notify_controller.settings"
    ) as mock_settings:
        mock_settings.smtp_to_email = "admin@example.com"

        response = client.post("/notify/INV-200/email")
        assert_status(response, 200)
        payload = response.json()
        assert payload["status"] == "sent"
        assert "email" in payload["item"]["channels"]
        assert payload["item"]["status"] == "sent"
        assert payload["item"].get("last_email_at") == fixed_now.isoformat()
        mock_smtp.assert_called_once()


def test_notify_email_missing_invoice_returns_404(isolated_store, client):
    with patch("app.controllers.notify_controller.settings") as mock_settings:
        mock_settings.smtp_to_email = "admin@example.com"

        isolated_store.set_last_scan([])
        response = client.post("/notify/INV-404/email")
        assert_status(response, 404)


def test_notify_email_missing_smtp_config(isolated_store, client):
    isolated_store.set_last_scan(
        [
            {
                "invoice_id": "INV-300",
                "customer": "Test",
                "days_overdue": 5,
                "amount": 1000.0,
                "history_count": 0,
                "risk_level": "LOW",
                "channels": [],
                "status": "skipped",
            }
        ]
    )

    with patch("app.controllers.notify_controller.settings") as mock_settings:
        mock_settings.smtp_to_email = None

        response = client.post("/notify/INV-300/email")
        assert_status(response, 400)
        payload = response.json()
        assert "SMTP_TO_EMAIL" in payload["detail"]


def test_notify_email_send_failure(isolated_store, client):
    isolated_store.set_last_scan(
        [
            {
                "invoice_id": "INV-400",
                "customer": "Test",
                "days_overdue": 10,
                "amount": 2000.0,
                "history_count": 1,
                "risk_level": "MEDIUM",
                "channels": [],
                "status": "skipped",
            }
        ]
    )

    with patch("app.controllers.notify_controller.smtp_send_email") as mock_smtp, patch(
        "app.controllers.notify_controller.settings"
    ) as mock_settings:
        mock_settings.smtp_to_email = "admin@example.com"
        mock_smtp.side_effect = Exception("SMTP Error")

        response = client.post("/notify/INV-400/email")
        assert_status(response, 500)
        payload = response.json()
        assert "Email send failed" in payload["detail"]


def test_auto_toggle_on_off(client):
    enabled = client.post("/notify/auto/on")
    assert_status(enabled, 200)
    assert enabled.json()["enabled"] is True

    disabled = client.post("/notify/auto/off")
    assert_status(disabled, 200)
    assert disabled.json()["enabled"] is False


def test_get_auto_status(client):
    with patch("app.controllers.notify_controller.settings") as mock_settings:
        mock_settings.auto_scan_enabled = True
        mock_settings.auto_scan_seconds = 600

        response = client.get("/notify/auto")
        assert_status(response, 200)
        payload = response.json()
        assert payload["enabled"] is True
        assert payload["interval_seconds"] == 600
