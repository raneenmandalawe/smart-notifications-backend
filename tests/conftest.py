import pytest

from app.services import store as store_module


@pytest.fixture()
def isolated_store(tmp_path, monkeypatch):
    state_dir = tmp_path / "state"
    state_path = state_dir / "last_scan.json"

    monkeypatch.setattr(store_module, "_STATE_DIR", str(state_dir))
    monkeypatch.setattr(store_module, "_STATE_PATH", str(state_path))
    monkeypatch.setattr(store_module, "_LAST_SCAN", [])

    yield store_module

    monkeypatch.setattr(store_module, "_LAST_SCAN", [])
