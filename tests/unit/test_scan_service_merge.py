from app.services.scan_service import merge_previous_decisions


def test_merge_preserves_sent_status_and_channels(fixed_now):
    decisions = [
        {
            "invoice_id": "INV-1",
            "customer": "Aurora",
            "days_overdue": 15,
            "amount": 15000.0,
            "history_count": 2,
            "risk_level": "HIGH",
            "channels": ["email"],
            "status": "sent",
        }
    ]
    previous = [
        {
            "invoice_id": "INV-1",
            "customer": "Aurora",
            "days_overdue": 14,
            "amount": 15000.0,
            "history_count": 1,
            "risk_level": "HIGH",
            "channels": ["sms"],
            "status": "sent",
            "last_notified_at": "2026-02-08T10:00:00",
            "last_sms_at": "2026-02-08T10:00:00",
        }
    ]

    merged = merge_previous_decisions(decisions, previous, fixed_now.isoformat())

    assert len(merged) == 1
    item = merged[0]
    assert item["status"] == "sent"
    assert set(item["channels"]) == {"email", "sms"}
    assert item["last_notified_at"] == "2026-02-08T10:00:00"
    assert item["last_sms_at"] == "2026-02-08T10:00:00"


def test_merge_sets_last_notified_when_missing(fixed_now):
    decisions = [
        {
            "invoice_id": "INV-2",
            "customer": "Nova",
            "days_overdue": 9,
            "amount": 900.0,
            "history_count": 0,
            "risk_level": "MEDIUM",
            "channels": ["email"],
            "status": "sent",
        }
    ]

    merged = merge_previous_decisions(decisions, [], fixed_now.isoformat())

    assert merged[0]["last_notified_at"] == fixed_now.isoformat()
