# Backend Runbook

## Prerequisites
- Python 3.10+
- ERPNext running and accessible
- `.env` configured with ERPNext credentials and SMTP

## Start Backend
```bash
/Users/raneenmandalawi/Desktop/smart-notifications-erpnext/.venv/bin/python -m uvicorn app.main:app --app-dir /Users/raneenmandalawi/Desktop/smart-notifications-erpnext/smart-notifications-backend --reload --port 8091
```

## Health Check
```bash
curl -s http://127.0.0.1:8091/health
```

## Common Issues
- **Port in use**: free port 8091 or change to another port.
- **ERPNext unavailable**: verify `ERPNEXT_BASE_URL` and credentials.
- **No data in dashboard**: run `POST /scan` to refresh results.

## Observability
- Request logs appear in the same terminal running uvicorn.
- Email/SMS notifications are logged with invoice ID and recipient.
