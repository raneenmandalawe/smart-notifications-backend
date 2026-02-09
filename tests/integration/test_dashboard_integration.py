import os

import pytest

from app.main import app
from scripts.seed_erpnext import seed_erpnext
from tests.assertions.api_assertions import assert_json_has_keys, assert_status


def _erpnext_env_ready():
    return os.getenv("ERPNEXT_API_KEY") and os.getenv("ERPNEXT_API_SECRET")


@pytest.fixture(scope="module")
def seeded_erpnext():
    if not _erpnext_env_ready():
        pytest.skip("ERPNext credentials not set")
    return seed_erpnext()


def test_dashboard_after_scan(seeded_erpnext):
    from fastapi.testclient import TestClient

    client = TestClient(app)
    client.post("/scan")

    response = client.get("/dashboard/overdue")
    assert_status(response, 200)
    payload = response.json()
    assert_json_has_keys(payload, ["items"])
    assert any(item["invoice_id"] == seeded_erpnext["main_invoice_id"] for item in payload["items"])

    stats = client.get("/dashboard/stats")
    assert_status(stats, 200)
    stats_payload = stats.json()
    assert_json_has_keys(stats_payload, ["total", "high_risk", "sent_today", "failed"])
