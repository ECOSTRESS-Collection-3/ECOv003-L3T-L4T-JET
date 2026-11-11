#!/usr/bin/env bash
# Inline smoke test runner for quick validation
# This script can be used to run smoke tests without building Docker

set -e

echo "=========================================="
echo "ECOv003-L3T-L4T-JET Local Smoke Test"
echo "=========================================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python version: $PYTHON_VERSION"
echo ""

# Check minimum Python version
REQUIRED_VERSION="3.11"
if [[ $(echo "$PYTHON_VERSION < $REQUIRED_VERSION" | bc) -eq 1 ]]; then
    echo "ERROR: Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

echo "Checking package installation..."
python3 -c "import ECOv003_L3T_L4T_JET; print('✓ ECOv003_L3T_L4T_JET package imported successfully')" || {
    echo "ERROR: Failed to import ECOv003_L3T_L4T_JET"
    echo "Make sure to install the package first:"
    echo "  pip install -e .[dev]"
    exit 1
}

echo ""
echo "Running smoke test..."
python3 -c "import ECOv003_L3T_L4T_JET; success = ECOv003_L3T_L4T_JET.test(); exit(0 if success else 1)" || {
    echo ""
    echo "=========================================="
    echo "✗ Smoke Test Failed"
    echo "=========================================="
    exit 1
}

echo ""
echo "=========================================="
echo "✓ All Smoke Tests Passed"
echo "=========================================="
exit 0
