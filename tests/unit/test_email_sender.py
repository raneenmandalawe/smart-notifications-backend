from unittest.mock import MagicMock, patch

import pytest

from app.services.email_sender import send_email


def test_send_email_success():
    with patch("app.services.email_sender.smtplib.SMTP_SSL") as mock_smtp, patch(
        "app.services.email_sender.settings"
    ) as mock_settings:
        mock_settings.smtp_user = "test@example.com"
        mock_settings.smtp_app_password = "test_password"
        mock_settings.smtp_from_email = "from@example.com"
        mock_settings.smtp_host = "smtp.gmail.com"
        mock_settings.smtp_port = 465

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_email(
            to_address="recipient@example.com",
            subject="Test Subject",
            body="Plain text body",
            html_body="<p>HTML body</p>",
        )

        mock_smtp.assert_called_once_with("smtp.gmail.com", 465)
        mock_server.login.assert_called_once_with("test@example.com", "test_password")
        mock_server.send_message.assert_called_once()


def test_send_email_without_html():
    with patch("app.services.email_sender.smtplib.SMTP_SSL") as mock_smtp, patch(
        "app.services.email_sender.settings"
    ) as mock_settings:
        mock_settings.smtp_user = "test@example.com"
        mock_settings.smtp_app_password = "test_password"
        mock_settings.smtp_from_email = "from@example.com"
        mock_settings.smtp_host = "smtp.gmail.com"
        mock_settings.smtp_port = 465

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_email(
            to_address="recipient@example.com",
            subject="Test Subject",
            body="Plain text only",
        )

        mock_server.send_message.assert_called_once()


def test_send_email_missing_credentials():
    with patch("app.services.email_sender.settings") as mock_settings:
        mock_settings.smtp_user = None
        mock_settings.smtp_app_password = None

        with pytest.raises(RuntimeError, match="SMTP credentials not configured"):
            send_email(
                to_address="recipient@example.com",
                subject="Test",
                body="Body",
            )


def test_send_email_smtp_connection_failure():
    with patch("app.services.email_sender.smtplib.SMTP_SSL") as mock_smtp, patch(
        "app.services.email_sender.settings"
    ) as mock_settings:
        mock_settings.smtp_user = "test@example.com"
        mock_settings.smtp_app_password = "test_password"
        mock_settings.smtp_from_email = "from@example.com"
        mock_settings.smtp_host = "smtp.gmail.com"
        mock_settings.smtp_port = 465

        mock_smtp.side_effect = Exception("SMTP connection failed")

        with pytest.raises(Exception, match="SMTP connection failed"):
            send_email(
                to_address="recipient@example.com",
                subject="Test",
                body="Body",
            )
