# Backend Architecture

## Overview
Smart Notifications Backend is a FastAPI service that augments ERPNext by scanning overdue Sales Invoices, calculating risk, deciding notification channels, and exposing dashboard APIs. The backend follows a modular MVC-inspired structure to keep routing, orchestration, and integration responsibilities separate and testable.

## Layered Design
- **Routers (API layer)**: FastAPI route definitions and HTTP concerns.
- **Controllers (orchestration)**: Handle request orchestration and error handling.
- **Services (domain logic)**: Risk scoring, scan orchestration, notifications.
- **Repositories / Integration**: ERPNext access and scan persistence.

## Data Flow
1. **POST /scan** triggers a real ERPNext query.
2. ERPNext invoices are transformed into risk decisions.
3. Results are stored in local persistence (in-memory + file-backed state).
4. **GET /dashboard/overdue** and **GET /dashboard/stats** return stored scan results.

## Modules
- `app/routes/*`: API endpoints.
- `app/controllers/*`: Orchestration and error handling.
- `app/services/risk_engine.py`: Risk scoring and channel selection logic.
- `app/services/scan_service.py`: Orchestrates ERPNext fetch + risk decisions + state persistence.
- `app/repositories/erpnext_repository.py`: ERPNext access layer.
- `app/repositories/scan_store.py`: Scan persistence wrapper.
- `app/services/erpnext_client.py`: REST client for ERPNext.
- `app/services/store.py`: In-memory + file-backed state for last scan.
- `app/services/auto_scan.py`: Background auto-scan loop.

## ERPNext Integration
- ERPNext is the system of record.
- No mock data is used in integration tests or E2E testing.
- ERPNext access uses REST API with API key/secret.

## Observability
- Request logging middleware records method, path, status, and latency.
- Notification actions log email/SMS send attempts and results.
