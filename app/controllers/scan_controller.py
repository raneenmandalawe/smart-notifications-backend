from app.services.scan_service import run_scan


def scan_overdue():
    return run_scan()
