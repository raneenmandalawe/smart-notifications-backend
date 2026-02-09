# API Test Plan

## Scope
Endpoints:
- `GET /health`
- `POST /scan`
- `GET /dashboard/overdue`
- `GET /dashboard/stats`
- `POST /notify/{invoice_id}/email`
- `POST /notify/{invoice_id}/sms`
- `GET /notify/auto`
- `POST /notify/auto/{state}`

## Test Types
### Unit/API Tests (FastAPI TestClient)
- Validate response codes and payload shapes.
- Validate error handling for invalid inputs.

#### Assertion Style (Course-Aligned)
```python
self.assertEqual(response.status_code, 200)
self.assertEqual(response.json()["status"], "ok")
```

### Integration Tests (Real ERPNext)
- Run `/scan` against live ERPNext.
- Confirm overdue invoices are returned.
- Validate dashboard aggregation after scan.

## Coverage Goals
- Full endpoint coverage.
- Error paths for missing resources and ERPNext connectivity issues.

## Non-Goals
- Mocking ERPNext for integration paths.
- UI rendering tests.

## Preconditions
- ERPNext running and accessible.
- API key/secret set in environment variables.

## Exit Criteria
- All endpoint tests pass.
- Integration tests pass with seeded ERPNext data.
- Allure report generated.
