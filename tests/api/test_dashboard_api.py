from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_endpoints_return_data(isolated_store):
    sample_items = [
        {
            "invoice_id": "INV-001",
            "customer": "Acme",
            "days_overdue": 12,
            "amount": 1500.0,
            "history_count": 1,
            "risk_level": "MEDIUM",
            "channels": ["email"],
            "status": "sent",
            "last_notified_at": "2026-02-08T10:00:00",
            "last_email_at": "2026-02-08T10:00:00",
        },
        {
            "invoice_id": "INV-002",
            "customer": "Beta",
            "days_overdue": 3,
            "amount": 250.0,
            "history_count": 0,
            "risk_level": "LOW",
            "channels": [],
            "status": "skipped",
        },
    ]
    isolated_store.set_last_scan(sample_items)

    client = TestClient(app)

    overdue_response = client.get("/dashboard/overdue")
    assert overdue_response.status_code == 200
    assert overdue_response.json()["items"] == sample_items

    stats_response = client.get("/dashboard/stats")
    assert stats_response.status_code == 200
    assert stats_response.json() == {
        "total": 2,
        "high_risk": 0,
        "sent_today": 2,
        "failed": 0,
    }
