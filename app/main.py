import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.health import router as health_router
from app.routes.scan import router as scan_router
from app.routes.dashboard import router as dashboard_router
from app.routes.notify import router as notify_router
from app.services.auto_scan import start_auto_scan


app = FastAPI(title="Smart Notifications Backend")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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
