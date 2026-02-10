# Allure Test Reports

Beautiful test reports with interactive graphs and statistics.

## 📊 What is Allure?

Allure generates beautiful HTML reports with:
- 📈 **Interactive graphs** - pie charts, trends, timelines
- 📊 **Statistics** - pass/fail rates, execution time
- 🔍 **Detailed results** - steps, attachments, logs
- 📝 **Historical trends** - track performance over time

## 🌐 View Reports on GitHub Pages (CI)

After pushing to your PR, the CI automatically:
1. Runs tests with Allure adapter
2. Generates HTML report with graphs
3. Publishes to GitHub Pages
4. Comments on PR with link

### Setup GitHub Pages (One-time)

1. Go to: https://github.com/raneenmandalawe/smart-notifications-backend/settings/pages
2. Under **Source**, select:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
3. Click **Save**

Your report will be at:
```
https://raneenmandalawe.github.io/smart-notifications-backend
```

## 💻 View Reports Locally

### Install Allure CLI (macOS)
```bash
brew install allure
```

For other platforms: https://allurereport.org/docs/v3/install/

### Generate and View Report

```bash
# Run tests (--alluredir is configured in pytest.ini)
pytest tests/

# View interactive report (opens browser)
./scripts/view-allure-report.sh

# OR generate static HTML
./scripts/generate-allure-report.sh
open allure-report/index.html
```

## 📝 Adding Test Metadata

Enhance your tests with decorators:

```python
import allure
from allure import severity_level

@allure.severity(severity_level.CRITICAL)
@allure.testcase("TMS-123")
def test_health_endpoint():
    """Test the /health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
```

## 🔧 Environment Information

The CI automatically creates `environment.properties` with:
- App version
- Python version
- Test execution date
- Git branch and commit

## 🔗 Links

- [Allure Documentation](https://allurereport.org/docs/)
- [Allure Pytest Plugin](https://github.com/allure-framework/allure-python)
- [Our Reports](https://raneenmandalawe.github.io/smart-notifications-backend)
