from tests.assertions.api_assertions import assert_json_has_keys, assert_status


def test_dashboard_endpoints_return_data(isolated_store, client, fixed_now):
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
            "last_notified_at": fixed_now.isoformat(),
            "last_email_at": fixed_now.isoformat(),
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
    overdue_response = client.get("/dashboard/overdue")
    assert_status(overdue_response, 200)
    assert overdue_response.json()["items"] == sample_items

    stats_response = client.get("/dashboard/stats")
    assert_status(stats_response, 200)
    payload = stats_response.json()
    assert_json_has_keys(payload, ["total", "high_risk", "sent_today", "failed"])
    assert payload == {
        "total": 2,
        "high_risk": 0,
        "sent_today": 1,
        "failed": 0,
    }
