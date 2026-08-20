#!/bin/bash
set -e
VENV=/opt/nstate-venv/bin/python
API=/opt/nstate/api
EU=/opt/nstate/eu/pipelines

echo "=== EU Pipelines ==="
$VENV $EU/eu_government_finance.py
$VENV $EU/eu_tax_revenue.py
$VENV $EU/eu_public_employment.py
echo "=== Done ==="
