from datetime import datetime

from app.repositories.scan_store import get_last_scan
from app.services.time_utils import utcnow


def get_overdue_items():
    return get_last_scan()


def get_dashboard_stats():
    items = get_last_scan()
    high = [item for item in items if item["risk_level"] == "HIGH"]
    failed = [item for item in items if item["status"] == "failed"]
    today = utcnow().date()
    sent_today = 0
    for item in items:
        if item.get("status") != "sent":
            continue
        last_notified = item.get("last_notified_at")
        if not last_notified:
            continue
        try:
            notified_date = datetime.fromisoformat(last_notified).date()
        except ValueError:
            continue
        if notified_date == today:
            sent_today += 1
    return {
        "total": len(items),
        "high_risk": len(high),
        "sent_today": sent_today,
        "failed": len(failed),
    }
