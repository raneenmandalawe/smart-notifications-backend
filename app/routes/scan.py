from fastapi import APIRouter, HTTPException
from app.services.scan_service import run_scan


router = APIRouter()


@router.post("/scan")
def scan():
    try:
        decisions = run_scan()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="ERPNext service unavailable") from exc

    return {"count": len(decisions), "items": decisions}
