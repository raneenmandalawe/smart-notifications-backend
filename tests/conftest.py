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
    from app.services import store

    fixed = datetime(2026, 2, 9, 12, 0, 0)
    monkeypatch.setattr(store, "utcnow", lambda: fixed)
    return fixed

    monkeypatch.setattr(store_module, "_LAST_SCAN", [])
