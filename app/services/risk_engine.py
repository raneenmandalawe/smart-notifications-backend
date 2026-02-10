from datetime import datetime
from typing import List, Dict, Any, Optional

from app.config import settings
from app.services.time_utils import utcnow


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def compute_days_overdue(due_date: Optional[str]) -> int:
    due = parse_date(due_date)
    if not due:
        return 0
    return max((utcnow() - due).days, 0)


def decide_channels(days_overdue: int, amount: float, history_count: int) -> List[str]:
    if days_overdue >= settings.days_threshold_high and amount >= settings.high_amount and history_count >= 2:
        return ["sms", "email"]
    if days_overdue >= settings.days_threshold_medium:
        return ["email"]
    return []


def compute_risk_level(days_overdue: int, amount: float, history_count: int) -> str:
    if days_overdue >= settings.days_threshold_high and amount >= settings.high_amount and history_count >= 2:
        return "HIGH"
    if days_overdue >= settings.days_threshold_medium:
        return "MEDIUM"
    return "LOW"


def build_decisions(invoices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    history_map = {}
    for inv in invoices:
        history_map[inv["customer"]] = history_map.get(inv["customer"], 0) + 1

    decisions = []
    for inv in invoices:
        days_overdue = compute_days_overdue(inv["due_date"])
        amount = float(inv.get("outstanding_amount") or inv.get("grand_total") or 0)
        history_count = max(history_map.get(inv["customer"], 0) - 1, 0)
        channels = decide_channels(days_overdue, amount, history_count)
        decisions.append(
            {
                "invoice_id": inv["name"],
                "customer": inv["customer"],
                "days_overdue": days_overdue,
                "amount": amount,
                "history_count": history_count,
                "risk_level": compute_risk_level(days_overdue, amount, history_count),
                "channels": channels,
                "status": "sent" if channels else "skipped",
            }
        )
    return decisions
