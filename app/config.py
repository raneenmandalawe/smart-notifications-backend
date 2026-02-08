import os

from dotenv import load_dotenv


_ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(_ENV_PATH)


class Settings:
    def __init__(self) -> None:
        self.erpnext_base_url = os.getenv("ERPNEXT_BASE_URL", "http://localhost:8080")
        self.erpnext_api_key = os.getenv("ERPNEXT_API_KEY", "")
        self.erpnext_api_secret = os.getenv("ERPNEXT_API_SECRET", "")
        self.high_amount = float(os.getenv("HIGH_AMOUNT", "10000"))
        self.days_threshold_high = int(os.getenv("DAYS_THRESHOLD_HIGH", "14"))
        self.days_threshold_medium = int(os.getenv("DAYS_THRESHOLD_MEDIUM", "7"))
        self.auto_scan_seconds = int(os.getenv("AUTO_SCAN_SECONDS", "60"))
        self.auto_scan_enabled = os.getenv("AUTO_SCAN_ENABLED", "true").lower() == "true"
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "465"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_app_password = os.getenv("SMTP_APP_PASSWORD", "")
        self.smtp_from_email = os.getenv("SMTP_FROM_EMAIL", self.smtp_user)
        self.smtp_to_email = os.getenv("SMTP_TO_EMAIL", "")

    def auth_header(self) -> dict:
        if self.erpnext_api_key and self.erpnext_api_secret:
            token = f"{self.erpnext_api_key}:{self.erpnext_api_secret}"
            return {"Authorization": f"token {token}"}
        return {}


settings = Settings()
