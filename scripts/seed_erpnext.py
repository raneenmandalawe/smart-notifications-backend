import json
import os
from datetime import date, timedelta
from typing import Any, Dict

import requests

from tests.fixtures.seed_data import SEED_AMOUNTS, SEED_CUSTOMER, SEED_ITEM, SEED_TAGS, seed_dates


def _get_env(name: str, default: str = "") -> str:
    value = os.getenv(name)
    return value if value is not None else default


def _auth_header() -> Dict[str, str]:
    key = _get_env("ERPNEXT_API_KEY")
    secret = _get_env("ERPNEXT_API_SECRET")
    if not key or not secret:
        raise RuntimeError("ERPNext credentials not set")
    return {"Authorization": f"token {key}:{secret}"}


def _session(base_url: str) -> requests.Session:
    session = requests.Session()
    session.headers.update(_auth_header())
    session.headers.update({"Content-Type": "application/json"})
    session.base_url = base_url.rstrip("/")
    return session


def _get_list(session: requests.Session, resource: str, filters=None, fields=None):
    url = f"{session.base_url}/api/resource/{resource}"
    params = {}
    if filters is not None:
        params["filters"] = json.dumps(filters)
    if fields is not None:
        params["fields"] = json.dumps(fields)
    response = session.get(url, params=params, timeout=20)
    response.raise_for_status()
    return response.json().get("data", [])


def _get_doc(session: requests.Session, resource: str, name: str):
    url = f"{session.base_url}/api/resource/{resource}/{name}"
    response = session.get(url, timeout=20)
    response.raise_for_status()
    return response.json().get("data")


def _create_doc(session: requests.Session, resource: str, payload: dict):
    url = f"{session.base_url}/api/resource/{resource}"
    response = session.post(url, data=json.dumps(payload), timeout=20)
    response.raise_for_status()
    return response.json().get("data")


def _submit_doc(session: requests.Session, doc: dict):
    url = f"{session.base_url}/api/method/frappe.client.submit"
    response = session.post(url, data=json.dumps({"doc": doc}), timeout=20)
    response.raise_for_status()
    return response.json().get("message")


def _ensure_customer(session: requests.Session) -> str:
    customer_name = SEED_CUSTOMER["name"]
    existing = _get_list(
        session,
        "Customer",
        filters=[["Customer", "name", "=", customer_name]],
        fields=["name"],
    )
    if existing:
        return existing[0]["name"]

    payload = {
        "customer_name": customer_name,
        "customer_type": "Company",
        "customer_group": "All Customer Groups",
        "territory": "All Territories",
        "email_id": SEED_CUSTOMER["email"],
        "mobile_no": SEED_CUSTOMER["phone"],
    }
    created = _create_doc(session, "Customer", payload)
    return created["name"]


def _ensure_item(session: requests.Session) -> str:
    item_code = SEED_ITEM["item_code"]
    existing = _get_list(
        session,
        "Item",
        filters=[["Item", "item_code", "=", item_code]],
        fields=["name"],
    )
    if existing:
        return existing[0]["name"]

    payload = {
        "item_code": item_code,
        "item_name": SEED_ITEM["item_name"],
        "item_group": SEED_ITEM["item_group"],
        "stock_uom": SEED_ITEM["stock_uom"],
        "is_stock_item": 0,
    }
    created = _create_doc(session, "Item", payload)
    return created["name"]


def _ensure_invoice(
    session: requests.Session,
    customer_name: str,
    item_code: str,
    tag: str,
    due_date: date,
    amount: float,
) -> str:
    existing = _get_list(
        session,
        "Sales Invoice",
        filters=[["Sales Invoice", "remarks", "=", tag]],
        fields=["name"],
    )
    if existing:
        return existing[0]["name"]

    posting_date = due_date - timedelta(days=5)
    payload = {
        "customer": customer_name,
        "posting_date": posting_date.isoformat(),
        "due_date": due_date.isoformat(),
        "remarks": tag,
        "items": [
            {
                "item_code": item_code,
                "qty": 1,
                "rate": amount,
            }
        ],
    }
    created = _create_doc(session, "Sales Invoice", payload)
    name = created["name"]

    doc = _get_doc(session, "Sales Invoice", name)
    try:
        _submit_doc(session, doc)
    except requests.HTTPError:
        pass
    return name


def seed_erpnext() -> Dict[str, Any]:
    base_url = _get_env("ERPNEXT_BASE_URL", "http://localhost:8080").rstrip("/")
    session = _session(base_url)

    customer_name = _ensure_customer(session)
    item_code = _ensure_item(session)

    dates = seed_dates()
    history_1 = _ensure_invoice(
        session,
        customer_name,
        item_code,
        SEED_TAGS["history_1"],
        dates["history_1"],
        SEED_AMOUNTS["history_1"],
    )
    history_2 = _ensure_invoice(
        session,
        customer_name,
        item_code,
        SEED_TAGS["history_2"],
        dates["history_2"],
        SEED_AMOUNTS["history_2"],
    )
    main = _ensure_invoice(
        session,
        customer_name,
        item_code,
        SEED_TAGS["main"],
        dates["main"],
        SEED_AMOUNTS["main"],
    )

    return {
        "customer_name": customer_name,
        "item_code": item_code,
        "history_invoice_ids": [history_1, history_2],
        "main_invoice_id": main,
    }


if __name__ == "__main__":
    result = seed_erpnext()
    print(json.dumps(result, indent=2))
