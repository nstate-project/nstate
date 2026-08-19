"""
ONS UK Labour Market pipeline
Source: ONS API v1 beta — no auth required
Licence: OGL v3
Updates: monthly (quarterly 3-month averages)
Key measures: employment, unemployment, economic inactivity
"""

import duckdb
import httpx
import csv
import io
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")
DATASET_ID = "labour-market"


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
    print(f"[{datetime.utcnow().isoformat()}] Running ONS Labour Market pipeline...")
    csv_url = get_csv_url()
    print(f"  CSV: {csv_url}")

    r = httpx.get(csv_url, timeout=120, follow_redirects=True)
    r.raise_for_status()
    rows = list(csv.DictReader(io.StringIO(r.text)))
    print(f"  Raw rows: {len(rows)}")

    source_id = f"ons_labour_market_{datetime.utcnow().strftime('%Y%m')}"
    with duckdb.connect(DB_PATH) as db:
        db.execute(
            """
            INSERT OR REPLACE INTO meta_sources
            (id, country, institution, dataset_name, release_url, licence, loaded_at)
            VALUES (?, 'uk', 'ONS', 'UK Labour Market Statistics',
                    'https://api.beta.ons.gov.uk/v1/datasets/labour-market',
                    'OGL v3', ?)
        """,
            [source_id, datetime.utcnow().isoformat()],
        )

        db.execute("DELETE FROM uk_ons_labour_market WHERE source_id = ?", [source_id])

        loaded = 0
        for row in rows:
            value_col = row.get("v4_0") or row.get("v4_1") or row.get("v4_2", "")
            if not value_col or value_col.strip() in ("", "x", ".."):
                continue
            try:
                value = float(value_col)
            except ValueError:
                continue
            db.execute(
                """
                INSERT INTO uk_ons_labour_market
                (period_label, unit_of_measure, economic_activity, age_group, sex,
                 seasonal_adjustment, value, source_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                [
                    row.get("mmm-mmm-yyyy") or row.get("Time", ""),
                    row.get("UnitOfMeasure", ""),
                    row.get("EconomicActivity", ""),
                    row.get("AgeGroups", ""),
                    row.get("Sex", ""),
                    row.get("SeasonalAdjustment", ""),
                    value,
                    source_id,
                ],
            )
            loaded += 1

        db.execute(
            """
            UPDATE meta_datasets SET last_loaded = ?, row_count = ?
            WHERE id = 'uk_ons_labour_market'
        """,
            [datetime.utcnow().isoformat(), loaded],
        )

    print(f"  ✓ Loaded {loaded:,} rows into uk_ons_labour_market")


if __name__ == "__main__":
    run()
