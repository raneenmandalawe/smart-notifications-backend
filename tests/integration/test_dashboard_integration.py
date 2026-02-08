import os
import pytest
from fastapi.testclient import TestClient
from app.main import app


def test_dashboard_after_scan():
    if not os.getenv("ERPNEXT_API_KEY") or not os.getenv("ERPNEXT_API_SECRET"):
        pytest.skip("ERPNext credentials not set")

    client = TestClient(app)
    client.post("/scan")

    response = client.get("/dashboard/overdue")
    assert response.status_code == 200
    assert "items" in response.json()

    stats = client.get("/dashboard/stats")
    assert stats.status_code == 200
    assert "total" in stats.json()
