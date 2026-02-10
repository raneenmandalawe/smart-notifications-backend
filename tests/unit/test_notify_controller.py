from unittest.mock import patch

import pytest

from app.controllers.notify_controller import (
    get_auto_status,
    send_email_notification,
    send_sms_notification,
    set_auto_state,
)


def test_send_sms_notification_success():
    with patch("app.controllers.notify_controller.mark_sent") as mock_mark:
        mock_mark.return_value = {"invoice_id": "INV-001", "customer": "Test Customer"}

        result = send_sms_notification("INV-001")

        mock_mark.assert_called_once_with("INV-001", "sms")
        assert result == {"invoice_id": "INV-001", "customer": "Test Customer"}


def test_send_sms_notification_not_found():
    with patch("app.controllers.notify_controller.mark_sent") as mock_mark:
        mock_mark.return_value = None

        result = send_sms_notification("INV-999")

        assert result is None


def test_send_email_notification_missing_smtp():
    with patch("app.controllers.notify_controller.settings") as mock_settings:
        mock_settings.smtp_to_email = None

        result = send_email_notification("INV-001")

        assert result == "missing_smtp"


def test_send_email_notification_invoice_not_found():
    with patch("app.controllers.notify_controller.settings") as mock_settings, patch(
        "app.controllers.notify_controller.get_item"
    ) as mock_get:
        mock_settings.smtp_to_email = "admin@example.com"
        mock_get.return_value = None

        result = send_email_notification("INV-999")

        assert result is None


def test_send_email_notification_success():
    with patch("app.controllers.notify_controller.settings") as mock_settings, patch(
        "app.controllers.notify_controller.get_item"
    ) as mock_get, patch(
        "app.controllers.notify_controller.smtp_send_email"
    ) as mock_smtp, patch(
        "app.controllers.notify_controller.mark_sent"
    ) as mock_mark:
        mock_settings.smtp_to_email = "admin@example.com"
        mock_get.return_value = {
            "invoice_id": "INV-001",
            "customer": "Test Customer",
            "days_overdue": 5,
            "amount": 1000,
        }
        mock_mark.return_value = {
            "invoice_id": "INV-001",
            "customer": "Test Customer",
            "channels": ["email"],
        }

        result = send_email_notification("INV-001")

        mock_smtp.assert_called_once()
        args, kwargs = mock_smtp.call_args
        assert kwargs["subject"] == "Invoice Payment Overdue: INV-001"
        assert "Test Customer" in kwargs["body"]
        assert "5" in kwargs["body"]
        mock_mark.assert_called_with("INV-001", "email")
        assert result == {
            "invoice_id": "INV-001",
            "customer": "Test Customer",
            "channels": ["email"],
        }


def test_send_email_notification_smtp_failure():
    with patch("app.controllers.notify_controller.settings") as mock_settings, patch(
        "app.controllers.notify_controller.get_item"
    ) as mock_get, patch(
        "app.controllers.notify_controller.smtp_send_email"
    ) as mock_smtp:
        mock_settings.smtp_to_email = "admin@example.com"
        mock_get.return_value = {
            "invoice_id": "INV-001",
            "customer": "Test Customer",
            "days_overdue": 5,
            "amount": 1000,
        }
        mock_smtp.side_effect = Exception("SMTP error")

        result = send_email_notification("INV-001")

        assert result == "send_failed"


def test_get_auto_status():
    with patch("app.controllers.notify_controller.settings") as mock_settings:
        mock_settings.auto_scan_enabled = True
        mock_settings.auto_scan_seconds = 300

        result = get_auto_status()

        assert result == {"enabled": True, "interval_seconds": 300}


def test_set_auto_state_on():
    with patch("app.controllers.notify_controller.settings") as mock_settings:
        mock_settings.auto_scan_enabled = False

        result = set_auto_state("on")

        assert mock_settings.auto_scan_enabled is True
        assert result == {"enabled": True}


def test_set_auto_state_off():
    with patch("app.controllers.notify_controller.settings") as mock_settings:
        mock_settings.auto_scan_enabled = True

        result = set_auto_state("off")

        assert mock_settings.auto_scan_enabled is False
        assert result == {"enabled": False}
