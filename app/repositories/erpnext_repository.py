from app.services.erpnext_client import ERPNextClient


def fetch_overdue_invoices():
    client = ERPNextClient()
    return client.get_overdue_invoices()
