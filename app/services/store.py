import json
import os

from app.services.time_utils import utcnow

_STATE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", ".data")
_STATE_PATH = os.path.join(_STATE_DIR, "last_scan.json")


def _load_state():
    if not os.path.exists(_STATE_PATH):
        return []
    try:
        with open(_STATE_PATH, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return []


def _save_state(items):
    os.makedirs(_STATE_DIR, exist_ok=True)
    with open(_STATE_PATH, "w", encoding="utf-8") as handle:
        json.dump(items, handle)


_LAST_SCAN = _load_state()


def set_last_scan(items):
    global _LAST_SCAN
    _LAST_SCAN = items
    _save_state(_LAST_SCAN)


def get_last_scan():
    return list(_LAST_SCAN)


def get_item(invoice_id: str):
    for item in _LAST_SCAN:
        if item["invoice_id"] == invoice_id:
            return item
    return None


def mark_sent(invoice_id: str, channel: str):
    now = utcnow().isoformat()
    for item in _LAST_SCAN:
        if item["invoice_id"] == invoice_id:
            if channel not in item["channels"]:
                item["channels"].append(channel)
            item["status"] = "sent"
            item["last_notified_at"] = now
            if channel == "email":
                item["last_email_at"] = now
            if channel == "sms":
                item["last_sms_at"] = now
            _save_state(_LAST_SCAN)
            return item
    return None
