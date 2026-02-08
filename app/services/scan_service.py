from datetime import datetime

from app.services.erpnext_client import ERPNextClient
from app.services.risk_engine import build_decisions
from app.services.store import get_last_scan, set_last_scan


def run_scan():
    client = ERPNextClient()
    invoices = client.get_overdue_invoices()
    decisions = build_decisions(invoices)
    previous = {item["invoice_id"]: item for item in get_last_scan()}

    now = datetime.utcnow().isoformat()
    for item in decisions:
        prior = previous.get(item["invoice_id"])
        if prior:
            if prior.get("channels"):
                item["channels"] = list({*item["channels"], *prior["channels"]})
            if prior.get("status") == "sent":
                item["status"] = "sent"
            if prior.get("last_notified_at"):
                item["last_notified_at"] = prior["last_notified_at"]
            if prior.get("last_email_at"):
                item["last_email_at"] = prior["last_email_at"]
            if prior.get("last_sms_at"):
                item["last_sms_at"] = prior["last_sms_at"]
        if item["status"] == "sent" and not item.get("last_notified_at"):
            item["last_notified_at"] = now

    set_last_scan(decisions)
    return decisions
