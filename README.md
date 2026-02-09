# Smart Notifications Backend

FastAPI service that scans ERPNext overdue Sales Invoices, computes risk, selects channels (Email/SMS), and exposes dashboard endpoints.

## Requirements
- Python 3.10+
- ERPNext running and reachable

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Copy environment file:
   - `cp .env.example .env`
4. Update ERPNext credentials and SMTP settings in `.env`.

## Run
```bash
/Users/raneenmandalawi/Desktop/smart-notifications-erpnext/.venv/bin/python -m uvicorn app.main:app --app-dir /Users/raneenmandalawi/Desktop/smart-notifications-erpnext/smart-notifications-backend --reload --port 8091
```

## Endpoints
- `GET /health`
- `POST /scan`
- `GET /dashboard/overdue`
- `GET /dashboard/stats`
- `POST /notify/{invoice_id}/email`
- `POST /notify/{invoice_id}/sms`

## Testing
- Unit tests for pure logic.
- Integration tests run against real ERPNext data (no mocks).

## Documentation
- `docs/ARCHITECTURE.md`
- `docs/TEST_STRATEGY.md`
- `docs/API_TEST_PLAN.md`
- `docs/API_TRACEABILITY_MATRIX.md`
- `docs/CI_PIPELINE.md`
- `docs/RUNBOOK.md`
