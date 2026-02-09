from app.services.store import (
    get_last_scan as _get_last_scan,
    set_last_scan as _set_last_scan,
    get_item as _get_item,
    mark_sent as _mark_sent,
)


def get_last_scan():
    return _get_last_scan()


def set_last_scan(items):
    _set_last_scan(items)


def get_item(invoice_id: str):
    return _get_item(invoice_id)


def mark_sent(invoice_id: str, channel: str):
    return _mark_sent(invoice_id, channel)
