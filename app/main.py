import asyncio
import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.health import router as health_router
from app.routes.scan import router as scan_router
from app.routes.dashboard import router as dashboard_router
from app.routes.notify import router as notify_router
from app.services.auto_scan import start_auto_scan


logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("app")

app = FastAPI(title="Smart Notifications Backend")


@app.middleware("http")
async def request_logger(request, call_next):
	start_time = time.perf_counter()
	response = await call_next(request)
	process_time_ms = (time.perf_counter() - start_time) * 1000
	logger.info(
		"%s %s -> %s (%.1fms)",
		request.method,
		request.url.path,
		response.status_code,
		process_time_ms,
	)
	return response

app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"http://localhost:3000",
		"http://127.0.0.1:3000",
		"http://localhost:3001",
		"http://127.0.0.1:3001",
	],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(scan_router)
app.include_router(dashboard_router)
app.include_router(notify_router)


@app.on_event("startup")
async def startup_event():
	asyncio.create_task(start_auto_scan())
