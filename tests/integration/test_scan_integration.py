import os
import pytest
from fastapi.testclient import TestClient
from app.main import app


def test_scan_with_real_erpnext():
    if not os.getenv("ERPNEXT_API_KEY") or not os.getenv("ERPNEXT_API_SECRET"):
        pytest.skip("ERPNext credentials not set")

    client = TestClient(app)
    response = client.post("/scan")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "items" in data
