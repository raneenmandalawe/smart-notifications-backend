from fastapi import APIRouter, HTTPException
from app.controllers.scan_controller import scan_overdue


router = APIRouter()


@router.post("/scan")
def scan():
    try:
        decisions = scan_overdue()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="ERPNext service unavailable") from exc

    return {"count": len(decisions), "items": decisions}
