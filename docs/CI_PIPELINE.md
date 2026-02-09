# Backend CI Pipeline

## Overview
The backend CI pipeline validates the FastAPI service, runs tests, and publishes Allure artifacts. The workflow file is `ci.yml`.

## Stages
1. **Checkout**
2. **Set up Python**
3. **Install dependencies**
4. **Run unit tests**
5. **Run integration tests** (only when ERPNext is reachable)
6. **Generate Allure results**
7. **Upload Allure artifacts**

## Environment Variables
- `ERPNEXT_API_KEY`
- `ERPNEXT_API_SECRET`
- `ERPNEXT_BASE_URL`

## Allure
- Allure results are generated from pytest runs.
- Artifacts are uploaded and can be published to GitHub Pages if enabled.

## Notes
- Integration tests must use real ERPNext data.
- CI should skip integration tests if ERPNext is unreachable.
