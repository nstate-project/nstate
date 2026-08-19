"""
ONS Annual Survey of Hours and Earnings (ASHE) — public vs private sector wages
Source: ONS API v1 beta — no auth required
Licence: OGL v3
Updates: annual (November)
"""

import csv
import io
import os
from datetime import datetime

import duckdb
import httpx

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")
DATASET_ID = "ashe-tables-25"
CHUNK = 50_000

INSERT_SQL = """
    INSERT INTO uk_ons_wages
    (year, geography_code, percentile, sex, working_pattern, measure, sector, value, source_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


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
    return r2.json()["downloads"]["csv"]["href"]


def _build_records(rows):
    records = []
    for row in rows:
        # ONS CSVs use V4_N (uppercase) or v4_n (lowercase) depending on dataset
        value_col = (
            row.get("V4_0")
            or row.get("V4_1")
            or row.get("V4_2")
            or row.get("v4_0")
            or row.get("v4_1")
            or row.get("v4_2", "")
        )
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
                None,  # source_id filled below
            )
        )
    return records


def run():
    print(f"[{datetime.utcnow().isoformat()}] Running ONS ASHE wages pipeline...")
    csv_url = get_csv_url()
    print(f"  CSV: {csv_url}")

    r = httpx.get(csv_url, timeout=180, follow_redirects=True)
    r.raise_for_status()
    rows = list(csv.DictReader(io.StringIO(r.text)))
    print(f"  Raw rows: {len(rows)}")

    source_id = f"ons_ashe_wages_{datetime.utcnow().strftime('%Y%m')}"
    records = _build_records(rows)
    for rec in records:
        rec = list(rec)
        rec[8] = source_id  # patch source_id — but tuples are immutable

    # Rebuild with source_id
    records = [r[:8] + (source_id,) for r in records]
    print(f"  Records to insert: {len(records):,}")

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
        db.execute("BEGIN TRANSACTION")
        for i in range(0, len(records), CHUNK):
            db.executemany(INSERT_SQL, records[i : i + CHUNK])
            print(f"  inserted {min(i + CHUNK, len(records)):,}/{len(records):,}")
        db.execute("COMMIT")

        db.execute(
            """
            UPDATE meta_datasets SET last_loaded = ?, row_count = ?
            WHERE id = 'uk_ons_wages'
        """,
            [datetime.utcnow().isoformat(), len(records)],
        )

    print(f"  ✓ Loaded {len(records):,} rows into uk_ons_wages")


if __name__ == "__main__":
    run()
