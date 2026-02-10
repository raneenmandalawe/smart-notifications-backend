from datetime import date, timedelta

SEED_CUSTOMER = {
    "name": "Aurora Labs",
    "email": "aurora.labs@example.com",
    "phone": "+972500000001",
}

SEED_ITEM = {
    "item_code": "AURORA-TEST-ITEM",
    "item_name": "Aurora Test Item",
    "item_group": "All Item Groups",
    "stock_uom": "Nos",
}

SEED_TAGS = {
    "history_1": "SN-SEED-HISTORY-1",
    "history_2": "SN-SEED-HISTORY-2",
    "main": "SN-SEED-MAIN",
}


def seed_dates(today: date | None = None):
    if today is None:
        today = date.today()
    return {
        "history_1": today - timedelta(days=30),
        "history_2": today - timedelta(days=20),
        "main": today - timedelta(days=15),
    }


SEED_AMOUNTS = {
    "history_1": 600.0,
    "history_2": 1200.0,
    "main": 15000.0,
}
