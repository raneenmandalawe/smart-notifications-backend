from app.repositories.erpnext_repository import fetch_overdue_invoices
from app.repositories.scan_store import get_last_scan, set_last_scan
from app.services.risk_engine import build_decisions
from app.services.time_utils import utcnow


def merge_previous_decisions(decisions, previous_items, now_iso: str):
    previous = {item["invoice_id"]: item for item in previous_items}
    merged = []
    for item in decisions:
        current = dict(item)
        prior = previous.get(current["invoice_id"])
        if prior:
            if prior.get("channels"):
                current["channels"] = list({*current["channels"], *prior["channels"]})
            if prior.get("status") == "sent":
                current["status"] = "sent"
            if prior.get("last_notified_at"):
                current["last_notified_at"] = prior["last_notified_at"]
            if prior.get("last_email_at"):
                current["last_email_at"] = prior["last_email_at"]
            if prior.get("last_sms_at"):
                current["last_sms_at"] = prior["last_sms_at"]
        if current["status"] == "sent" and not current.get("last_notified_at"):
            current["last_notified_at"] = now_iso
        merged.append(current)
    return merged


def run_scan():
    invoices = fetch_overdue_invoices()
    decisions = build_decisions(invoices)
    now_iso = utcnow().isoformat()
    merged = merge_previous_decisions(decisions, get_last_scan(), now_iso)
    set_last_scan(merged)
    return merged
