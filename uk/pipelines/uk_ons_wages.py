"""
ONS Annual Survey of Hours and Earnings (ASHE) — public vs private sector wages
Source: ONS API v1 beta — no auth required
Licence: OGL v3
Updates: annual (November)
"""

import duckdb
import httpx
import csv
import io
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")
DATASET_ID = "ashe-tables-25"


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
    print(f"[{datetime.utcnow().isoformat()}] Running ONS ASHE wages pipeline...")
    csv_url = get_csv_url()
    print(f"  CSV: {csv_url}")

    r = httpx.get(csv_url, timeout=120, follow_redirects=True)
    r.raise_for_status()
    rows = list(csv.DictReader(io.StringIO(r.text)))
    print(f"  Raw rows: {len(rows)}")

    source_id = f"ons_ashe_wages_{datetime.utcnow().strftime('%Y%m')}"
    with duckdb.connect(DB_PATH) as db:
        db.execute(
            """
            INSERT OR REPLACE INTO meta_sources
            (id, country, institution, dataset_name, release_url, licence, loaded_at)
            VALUES (?, 'uk', 'ONS', 'ASHE — Earnings by Region and Sector',
                    'https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-25',
                    'OGL v3', ?)
        """,
            [source_id, datetime.utcnow().isoformat()],
        )

        db.execute("DELETE FROM uk_ons_wages WHERE source_id = ?", [source_id])

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
                    row.get("administrative-geography") or row.get("Geography", ""),
                    row.get("averages-and-percentiles")
                    or row.get("AveragesAndPercentiles", ""),
                    row.get("sex") or row.get("Sex", ""),
                    row.get("working-pattern") or row.get("WorkingPattern", ""),
                    row.get("hours-and-earnings") or row.get("HoursAndEarnings", ""),
                    row.get("sector") or row.get("Sector", ""),
                    value,
                    source_id,
                )
            )

        db.executemany(
            """
            INSERT INTO uk_ons_wages
            (year, geography_code, percentile, sex, working_pattern,
             measure, sector, value, source_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            records,
        )
        loaded = len(records)

        db.execute(
            """
            UPDATE meta_datasets SET last_loaded = ?, row_count = ?
            WHERE id = 'uk_ons_wages'
        """,
            [datetime.utcnow().isoformat(), loaded],
        )

    print(f"  ✓ Loaded {loaded:,} rows into uk_ons_wages")


if __name__ == "__main__":
    run()
