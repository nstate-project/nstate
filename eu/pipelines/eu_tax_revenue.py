"""
EU Tax Revenue pipeline — Eurostat gov_10a_taxag
Licence:  Eurostat reuse policy (free, attribution required)
Updates:  Annually
Writes to: eu_tax_revenue
"""

import duckdb
import os
import urllib.request
import json
from datetime import datetime, timezone

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")
BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"

ALL_EU = [
    "AT",
    "BE",
    "BG",
    "CY",
    "CZ",
    "DE",
    "DK",
    "EE",
    "EL",
    "ES",
    "FI",
    "FR",
    "HR",
    "HU",
    "IE",
    "IT",
    "LT",
    "LU",
    "LV",
    "MT",
    "NL",
    "PL",
    "PT",
    "RO",
    "SE",
    "SI",
    "SK",
    "EU27_2020",
]

TAX_PARAMS = {"na_item": "D2", "unit": "PC_GDP", "sector": "S13", "freq": "A"}

DATASET_META = (
    "eu_tax_revenue",
    "eu",
    "Eurostat Tax Revenue",
    "Taxes and social contributions as % GDP for EU27 countries (annual)",
    "https://ec.europa.eu/eurostat/web/government-finance-statistics",
    "Eurostat reuse policy",
    1,
)


def fetch_eurostat(params: dict) -> dict:
    geo_params = "&".join(f"geo={c}" for c in ALL_EU)
    base_params = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{BASE}/gov_10a_taxag?format=JSON&lang=EN&{base_params}&{geo_params}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read())


def parse_sdmx(data: dict) -> list[dict]:
    dims, sizes = data["id"], data["size"]
    dim_labels = {
        d: {v: k for k, v in data["dimension"][d]["category"]["index"].items()}
        for d in dims
    }
    rows = []
    for key_str, value in data.get("value", {}).items():
        k = int(key_str)
        indices = []
        for size in reversed(sizes):
            indices.append(k % size)
            k //= size
        row = {d: dim_labels[d][i] for d, i in zip(dims, reversed(indices))}
        row["value"] = value
        rows.append(row)
    return rows


def load_rows(db, rows: list[dict], loaded_at: str):
    for row in rows:
        try:
            year = int(row["time"])
        except (ValueError, KeyError):
            continue
        db.execute(
            """INSERT OR REPLACE INTO eu_tax_revenue
               (country, year, value_pct_gdp, loaded_at)
               VALUES (?, ?, ?, ?)""",
            [row.get("geo"), year, row["value"], loaded_at],
        )


def run():
    print(f"[{datetime.now(timezone.utc).isoformat()}] EU Tax Revenue pipeline")
    loaded_at = datetime.now(timezone.utc).isoformat()
    with duckdb.connect(DB_PATH) as db:
        try:
            data = fetch_eurostat(TAX_PARAMS)
            rows = parse_sdmx(data)
            load_rows(db, rows, loaded_at)
            print(f"  ✓ tax_revenue_pct_gdp: {len(rows)} rows")
        except Exception as e:
            print(f"  ✗ fetch failed: {e}")
        db.execute(
            """INSERT OR REPLACE INTO meta_datasets
               (id, country, name, description, source_url, licence, priority)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            list(DATASET_META),
        )
    print("Done.")


if __name__ == "__main__":
    run()
