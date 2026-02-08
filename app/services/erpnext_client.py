import json
from typing import List, Dict, Any

import requests

from app.config import settings


class ERPNextClient:
    def __init__(self) -> None:
        self.base_url = settings.erpnext_base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(settings.auth_header())

    def get_overdue_invoices(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/api/resource/Sales Invoice"
        filters = [
            ["Sales Invoice", "outstanding_amount", ">", 0],
            ["Sales Invoice", "status", "=", "Overdue"],
        ]
        fields = [
            "name",
            "customer",
            "due_date",
            "posting_date",
            "outstanding_amount",
            "grand_total",
        ]
        params = {
            "fields": json.dumps(fields),
            "filters": json.dumps(filters),
        }
        response = self.session.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
