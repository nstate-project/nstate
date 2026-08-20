#!/bin/bash
# Runs all Eurostat pipelines. Static-rate pipelines (eu_tax_rates, eu_vat_rates)
# are intentionally excluded — they require manual yearly updates.
set -e
VENV=/opt/nstate-venv/bin/python3
EU=/opt/nstate/eu/pipelines

echo "=== EU Eurostat Pipelines: $(date -u '+%Y-%m-%d %H:%M UTC') ==="
$VENV $EU/eu_government_finance.py
$VENV $EU/eu_tax_revenue.py
$VENV $EU/eu_public_employment.py
$VENV $EU/eu_tax_breakdown.py
$VENV $EU/eu_labour_tax_wedge.py
$VENV $EU/eu_price_levels.py
echo "=== All done: $(date -u '+%Y-%m-%d %H:%M UTC') ==="
