def assert_decision_schema(decision: dict):
    required = [
        "invoice_id",
        "customer",
        "days_overdue",
        "amount",
        "history_count",
        "risk_level",
        "channels",
        "status",
    ]
    for key in required:
        assert key in decision

    assert isinstance(decision["invoice_id"], str)
    assert isinstance(decision["customer"], str)
    assert isinstance(decision["days_overdue"], int)
    assert isinstance(decision["amount"], (int, float))
    assert isinstance(decision["history_count"], int)
    assert decision["risk_level"] in {"LOW", "MEDIUM", "HIGH"}
    assert isinstance(decision["channels"], list)
    assert decision["status"] in {"sent", "skipped", "failed"}
