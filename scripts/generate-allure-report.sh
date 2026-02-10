#!/bin/bash
# Generate static Allure HTML report

set -e

# Check if allure is installed
if ! command -v allure &> /dev/null; then
    echo "❌ Allure not found!"
    echo "📦 Install with: brew install allure"
    echo "📖 Or see: https://allurereport.org/docs/v3/install/"
    exit 1
fi

# Check if results exist
if [ ! -d "allure-results" ]; then
    echo "❌ No allure-results directory found!"
    echo "💡 Run tests first: pytest tests/"
    exit 1
fi

# Generate report
echo "📊 Generating Allure HTML report..."
rm -rf allure-report
allure generate allure-results -o allure-report --clean

echo "✅ Report generated!"
echo "🌐 Open: allure-report/index.html"
