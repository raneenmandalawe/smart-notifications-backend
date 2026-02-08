from fastapi import APIRouter
from app.services.store import get_last_scan


router = APIRouter(prefix="/dashboard")


@router.get("/overdue")
def overdue():
    return {"items": get_last_scan()}


@router.get("/stats")
def stats():
    items = get_last_scan()
    high = [i for i in items if i["risk_level"] == "HIGH"]
    failed = [i for i in items if i["status"] == "failed"]
    return {
        "total": len(items),
        "high_risk": len(high),
        "sent_today": len(items),
        "failed": len(failed),
    }
