# Smart Notifications Backend

FastAPI service that scans ERPNext overdue invoices, computes risk, selects channels, and exposes dashboard endpoints.

## Requirements
- Python 3.10+
- ERPNext running locally (Docker)

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Copy environment file:
   - `cp .env.example .env`
4. Update ERPNext credentials in `.env`.

## Run
- `uvicorn app.main:app --reload --port 8085`

## Endpoints
- `GET /health`
- `POST /scan`
- `GET /dashboard/overdue`
- `GET /dashboard/stats`

## Tests
- Unit tests: `pytest tests/unit`
- Integration tests (ERPNext required): `pytest tests/integration`

## Notes
Integration tests require real ERPNext data (no mocking).
