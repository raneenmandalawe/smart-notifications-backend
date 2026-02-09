from app.services import store


def test_store_set_and_get_item(isolated_store):
    sample = [
        {
            "invoice_id": "INV-300",
            "customer": "Delta",
            "days_overdue": 5,
            "amount": 300.0,
            "history_count": 0,
            "risk_level": "LOW",
            "channels": [],
            "status": "skipped",
        }
    ]
    isolated_store.set_last_scan(sample)

    assert isolated_store.get_last_scan() == sample
    assert isolated_store.get_item("INV-300") == sample[0]
    assert isolated_store.get_item("INV-404") is None


def test_store_mark_sent_updates_channels(isolated_store):
    isolated_store.set_last_scan(
        [
            {
                "invoice_id": "INV-301",
                "customer": "Delta",
                "days_overdue": 10,
                "amount": 1000.0,
                "history_count": 1,
                "risk_level": "MEDIUM",
                "channels": [],
                "status": "skipped",
            }
        ]
    )

    updated = isolated_store.mark_sent("INV-301", "email")

    assert updated is not None
    assert updated["status"] == "sent"
    assert "email" in updated["channels"]
    assert updated.get("last_email_at")
