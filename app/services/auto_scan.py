import asyncio
import logging

from app.config import settings
from app.services.scan_service import run_scan


logger = logging.getLogger(__name__)


async def start_auto_scan():
    if not settings.auto_scan_enabled or settings.auto_scan_seconds <= 0:
        return

    while True:
        try:
            run_scan()
        except Exception as exc:
            logger.warning("Auto scan failed: %s", exc)
        await asyncio.sleep(settings.auto_scan_seconds)
