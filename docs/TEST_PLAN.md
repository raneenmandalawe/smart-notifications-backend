# Backend Test Plan

| ID | Layer | Endpoint / Function | Preconditions | Steps | Expected Result |
|---|---|---|---|---|---|
| UT-01 | Unit | `compute_days_overdue()` | None | Call with `None`, empty, invalid date | Returns `0` (no crash) |
| UT-02 | Unit | `decide_channels()` | None | Pass high/medium/low values | Channel list matches rules |
| UT-03 | Unit | `compute_risk_level()` | None | Pass high/medium/low values | Risk level matches rules |
| UT-04 | Unit | `merge_previous_decisions()` | None | Merge current + previous decisions | Channels merged, status preserved, timestamps kept |
| UT-05 | Unit | `store.mark_sent()` | Store initialized | Call `mark_sent()` | Status set to `sent`, timestamps set |
| API-01 | API | `POST /scan` | Service mocked | Call endpoint | 200 + `count/items` schema |
| API-02 | API | `POST /scan` error | Service raises exception | Call endpoint | 503 with error detail |
| API-03 | API | `GET /dashboard/overdue` | Store seeded | Call endpoint | 200 + items list |
| API-04 | API | `GET /dashboard/stats` | Store seeded | Call endpoint | 200 + stats keys (`total/high_risk/sent_today/failed`) |
| API-05 | API | `POST /notify/{id}/sms` | Store seeded | Call endpoint | 200, item marked sent |
| API-06 | API | `GET /health` | None | Call endpoint | 200 + `{status: ok}` |
| INT-01 | Integration | ERPNext seed script | ERPNext credentials set | Run seed | Customer + 3 invoices created or reused |
| INT-02 | Integration | `POST /scan` | Seeded ERPNext data | Call endpoint | At least 1 decision; main invoice HIGH + sms+email |
| INT-03 | Integration | `GET /dashboard/overdue` | Seeded + scan | Call endpoint | Items include main invoice |
| INT-04 | Integration | `GET /dashboard/stats` | Seeded + scan | Call endpoint | Stats keys present |
