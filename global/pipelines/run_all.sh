#!/bin/bash
# Annual World Bank data refresh. Runs both fiscal + price level pipelines.
# Complements nstate-eu-refresh.timer — run after that one completes.
set -e
VENV=/opt/nstate-venv/bin/python3
GLOBAL=/opt/nstate/global/pipelines

echo "=== Global Pipelines: $(date -u '+%Y-%m-%d %H:%M UTC') ==="
$VENV $GLOBAL/wb_fiscal.py
$VENV $GLOBAL/wb_price_levels.py
echo "=== All done: $(date -u '+%Y-%m-%d %H:%M UTC') ==="
