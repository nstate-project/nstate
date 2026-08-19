"""
ONS House Price Statistics pipeline
Source: ONS API v1 beta — no auth required
Licence: OGL v3
Updates: quarterly
Covers: average prices and sales counts by local authority
"""

import duckdb
import httpx
import csv
import io
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")
DATASET_ID = "house-prices-local-authority"


def get_csv_url():
    r = httpx.get(
        f"https://api.beta.ons.gov.uk/v1/datasets/{DATASET_ID}",
        headers={"Accept": "application/json"},
        timeout=30,
    )
    r.raise_for_status()
    latest = r.json()["links"]["latest_version"]["href"]
    r2 = httpx.get(latest, headers={"Accept": "application/json"}, timeout=30)
    r2.raise_for_status()
    data = r2.json()
    return data["downloads"]["csv"]["href"]


def run():
    print(f"[{datetime.utcnow().isoformat()}] Running ONS House Prices pipeline...")
    csv_url = get_csv_url()
    print(f"  CSV: {csv_url}")

    r = httpx.get(csv_url, timeout=180, follow_redirects=True)
    r.raise_for_status()
    rows = list(csv.DictReader(io.StringIO(r.text)))
    print(f"  Raw rows: {len(rows)}")

    source_id = f"ons_house_prices_{datetime.utcnow().strftime('%Y%m')}"
    with duckdb.connect(DB_PATH) as db:
        db.execute(
            """
            INSERT OR REPLACE INTO meta_sources
            (id, country, institution, dataset_name, release_url, licence, loaded_at)
            VALUES (?, 'uk', 'ONS', 'House Price Statistics for Small Areas',
                    'https://api.beta.ons.gov.uk/v1/datasets/house-prices-local-authority',
                    'OGL v3', ?)
        """,
            [source_id, datetime.utcnow().isoformat()],
        )

        db.execute("DELETE FROM uk_ons_house_prices WHERE source_id = ?", [source_id])

        records = []
        for row in rows:
            value_col = row.get("v4_0") or row.get("v4_1") or row.get("v4_2", "")
            if not value_col or value_col.strip() in ("", "x", ".."):
                continue
            try:
                value = float(value_col)
            except ValueError:
                continue
            records.append(
                (
                    row.get("calendar-years") or row.get("Time", ""),
                    row.get("mmm") or row.get("Month", ""),
                    row.get("administrative-geography") or row.get("Geography", ""),
                    row.get("property-type") or row.get("PropertyType", ""),
                    row.get("build-status") or row.get("BuildStatus", ""),
                    row.get("house-sales-and-prices")
                    or row.get("HouseSalesAndPrices", ""),
                    value,
                    source_id,
                )
            )

        db.executemany(
            """
            INSERT INTO uk_ons_house_prices
            (year, month_label, geography_code, property_type, build_status,
             measure, value, source_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            records,
        )
        loaded = len(records)

        db.execute(
            """
            UPDATE meta_datasets SET last_loaded = ?, row_count = ?
            WHERE id = 'uk_ons_house_prices'
        """,
            [datetime.utcnow().isoformat(), loaded],
        )

    print(f"  ✓ Loaded {loaded:,} rows into uk_ons_house_prices")


if __name__ == "__main__":
    run()
