from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.services import store as store_module


@pytest.fixture()
def isolated_store(tmp_path, monkeypatch):
    state_dir = tmp_path / "state"
    state_path = state_dir / "last_scan.json"

    monkeypatch.setattr(store_module, "_STATE_DIR", str(state_dir))
    monkeypatch.setattr(store_module, "_STATE_PATH", str(state_path))
    monkeypatch.setattr(store_module, "_LAST_SCAN", [])

    return store_module


@pytest.fixture()
def client():
    from app.main import app

    return TestClient(app)


@pytest.fixture()
def fixed_now(monkeypatch):
    fixed = datetime(2026, 2, 9, 12, 0, 0)
    
    # Monkeypatch all modules that import utcnow
    from app.services import time_utils, store, scan_service, risk_engine
    from app.controllers import dashboard_controller
    
    monkeypatch.setattr(time_utils, "utcnow", lambda: fixed)
    monkeypatch.setattr(store, "utcnow", lambda: fixed)
    monkeypatch.setattr(scan_service, "utcnow", lambda: fixed)
    monkeypatch.setattr(risk_engine, "utcnow", lambda: fixed)
    monkeypatch.setattr(dashboard_controller, "utcnow", lambda: fixed)
    
    return fixed
