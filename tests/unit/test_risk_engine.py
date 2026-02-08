from app.services.risk_engine import decide_channels, compute_risk_level


def test_high_risk_channels():
    channels = decide_channels(days_overdue=20, amount=15000, history_count=2)
    assert "sms" in channels
    assert "email" in channels


def test_medium_risk_channels():
    channels = decide_channels(days_overdue=10, amount=500, history_count=0)
    assert channels == ["email"]


def test_low_risk_channels():
    channels = decide_channels(days_overdue=2, amount=500, history_count=0)
    assert channels == []


def test_risk_levels():
    assert compute_risk_level(20, 15000, 2) == "HIGH"
    assert compute_risk_level(10, 500, 0) == "MEDIUM"
    assert compute_risk_level(2, 500, 0) == "LOW"
