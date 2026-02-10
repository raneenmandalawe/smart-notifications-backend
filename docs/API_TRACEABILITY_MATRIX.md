# API Traceability Matrix

| Requirement | Endpoint | Test Type | Expected Result |
|---|---|---|---|
| Health check | `GET /health` | API | 200 + `{status: ok}` |
| Scan overdue invoices | `POST /scan` | Integration (ERPNext) | 200 + list of decisions |
| Dashboard overdue list | `GET /dashboard/overdue` | API/Integration | Items returned after scan |
| Dashboard stats | `GET /dashboard/stats` | API/Integration | Aggregated counters |
| Send email notification | `POST /notify/{invoice_id}/email` | API | 200, audit fields updated |
| Send SMS notification | `POST /notify/{invoice_id}/sms` | API | 200, audit fields updated |
| Auto scan status | `GET /notify/auto` | API | Returns enabled + interval |
| Auto scan toggle | `POST /notify/auto/{state}` | API | Enabled toggled |

Notes:
- Integration rows must use real ERPNext data.
- All tests must be deterministic.
