import os

import pytest

from app.main import app
from scripts.seed_erpnext import seed_erpnext
from tests.assertions.api_assertions import assert_json_has_keys, assert_status
from tests.assertions.decision_assertions import assert_decision_schema


def _erpnext_env_ready():
    return os.getenv("ERPNEXT_API_KEY") and os.getenv("ERPNEXT_API_SECRET")


@pytest.fixture(scope="module")
def seeded_erpnext():
    if not _erpnext_env_ready():
        pytest.skip("ERPNext credentials not set")
    return seed_erpnext()


def test_scan_with_real_erpnext(seeded_erpnext):
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.post("/scan")
    assert_status(response, 200)
    data = response.json()
    assert_json_has_keys(data, ["count", "items"])
    assert data["count"] >= 1
    assert_decision_schema(data["items"][0])

    main_invoice_id = seeded_erpnext["main_invoice_id"]
    main = next((item for item in data["items"] if item["invoice_id"] == main_invoice_id), None)
    assert main is not None
    assert main["risk_level"] == "HIGH"
    assert set(main["channels"]) == {"sms", "email"}
