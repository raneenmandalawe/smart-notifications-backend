import smtplib
from email.message import EmailMessage

from app.config import settings


def send_email(to_address: str, subject: str, body: str, html_body: str | None = None) -> None:
    if not settings.smtp_user or not settings.smtp_app_password:
        raise RuntimeError("SMTP credentials not configured")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from_email
    msg["To"] = to_address
    msg.set_content(body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
        server.login(settings.smtp_user, settings.smtp_app_password)
        server.send_message(msg)
