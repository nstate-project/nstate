#!/bin/bash
# Run all nstate UK data pipelines
# Logs to /opt/nstate/logs/pipeline_YYYYMMDD.log

set -e
LOG=/opt/nstate/logs/pipeline_$(date +%Y%m%d_%H%M%S).log
mkdir -p /opt/nstate/logs

export DB_PATH=/opt/nstate/data/nstate.duckdb
export DATA_DIR=/opt/nstate/data/parquet
VENV=/opt/nstate-venv/bin/python
PIPE=/opt/nstate/data/pipelines

echo "=== nstate pipeline run $(date -u) ===" | tee -a "$LOG"

run_pipeline() {
    local name=$1
    local script=$2
    echo "" | tee -a "$LOG"
    echo "--- $name ---" | tee -a "$LOG"
    if $VENV "$script" 2>&1 | tee -a "$LOG"; then
        echo "  [OK] $name" | tee -a "$LOG"
    else
        echo "  [FAIL] $name — check $LOG" | tee -a "$LOG"
    fi
}

# Tier 1: ONS API (no extra deps)
run_pipeline "Civil Service (Cabinet Office)"   "$PIPE/uk_civil_service.py"
run_pipeline "ONS CPIH Inflation"               "$PIPE/uk_ons_cpih.py"
run_pipeline "ONS Labour Market"                "$PIPE/uk_ons_labour_market.py"
run_pipeline "ONS GDP Monthly"                  "$PIPE/uk_ons_gdp.py"
run_pipeline "ONS Retail Sales"                 "$PIPE/uk_ons_retail_sales.py"
run_pipeline "ONS ASHE Wages"                   "$PIPE/uk_ons_wages.py"

# House prices is large — run last of the ONS batch
run_pipeline "ONS House Prices"                 "$PIPE/uk_ons_house_prices.py"

# Tier 2: Excel/ODS (need odfpy + openpyxl)
run_pipeline "HMRC Tax Receipts"                "$PIPE/uk_hmrc_tax_receipts.py"
run_pipeline "PESA Expenditure"                 "$PIPE/uk_pesa.py"
run_pipeline "DWP Benefits"                     "$PIPE/uk_dwp_benefits.py"

# Tier 3: APIs and scraped CSVs
run_pipeline "Public Sector Finances (ONS)"     "$PIPE/uk_psf.py"
run_pipeline "Find a Tender (contracts)"        "$PIPE/uk_find_a_tender.py"
run_pipeline "Spend Over £25k"                  "$PIPE/uk_spend_25k.py"

echo "" | tee -a "$LOG"
echo "=== All pipelines complete $(date -u) ===" | tee -a "$LOG"

# Print summary row counts
$VENV - << 'EOF'
import duckdb, os
db = duckdb.connect(os.environ["DB_PATH"])
rows = db.execute("""
    SELECT id, name, row_count, last_loaded
    FROM meta_datasets WHERE country='uk'
    ORDER BY priority, id
""").fetchall()
print("\n=== Dataset summary ===")
for r in rows:
    loaded = str(r[3])[:16] if r[3] else "not loaded"
    count = f"{r[2]:,}" if r[2] else "0"
    print(f"  {r[0]:<30} {count:>10} rows  {loaded}")
EOF
