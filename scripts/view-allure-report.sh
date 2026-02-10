#!/bin/bash
# Generate and view Allure report in browser

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

# Serve report
echo "📊 Opening Allure report in browser..."
allure serve allure-results
