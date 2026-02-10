from fastapi import APIRouter
from app.controllers.dashboard_controller import get_overdue_items, get_dashboard_stats


router = APIRouter(prefix="/dashboard")


@router.get("/overdue")
def overdue():
    return {"items": get_overdue_items()}


@router.get("/stats")
def stats():
    return get_dashboard_stats()
