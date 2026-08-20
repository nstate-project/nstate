"""
EU Government Finance pipeline — Eurostat
Datasets: gov_10a_exp (expenditure), gov_10dd_edpt1 (deficit + debt)
Licence:  Eurostat reuse policy (free, attribution required)
Updates:  Annually (September/October release)
Writes to: eu_government_finance
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


def fetch_eurostat(dataset: str, params: dict) -> dict:
    geo_params = "&".join(f"geo={c}" for c in ALL_EU)
    base_params = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{BASE}/{dataset}?format=JSON&lang=EN&{base_params}&{geo_params}"
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


def load_indicator(db, rows: list[dict], indicator: str, loaded_at: str):
    for row in rows:
        try:
            year = int(row["time"])
        except (ValueError, KeyError):
            continue
        db.execute(
            """INSERT OR REPLACE INTO eu_government_finance
               (country, year, indicator, value, loaded_at)
               VALUES (?, ?, ?, ?, ?)""",
            [row.get("geo"), year, indicator, row["value"], loaded_at],
        )


EXPENDITURE_PARAMS = {
    "na_item": "TE",
    "unit": "PC_GDP",
    "sector": "S13",
    "freq": "A",
    "cofog99": "TOTAL",
}
DEFICIT_PARAMS = {"na_item": "B9", "unit": "PC_GDP", "sector": "S13", "freq": "A"}
DEBT_PARAMS = {"na_item": "GD", "unit": "PC_GDP", "sector": "S13", "freq": "A"}

FETCHES = [
    ("gov_10a_exp", EXPENDITURE_PARAMS, "expenditure_pct_gdp"),
    ("gov_10dd_edpt1", DEFICIT_PARAMS, "deficit_pct_gdp"),
    ("gov_10dd_edpt1", DEBT_PARAMS, "debt_pct_gdp"),
]

DATASET_META = (
    "eu_government_finance",
    "eu",
    "Eurostat Government Finance",
    "Total expenditure, deficit and debt as % GDP for EU27 (annual)",
    "https://ec.europa.eu/eurostat/web/government-finance-statistics",
    "Eurostat reuse policy",
    1,
)


def fetch_and_load(db, dataset: str, params: dict, indicator: str, loaded_at: str):
    data = fetch_eurostat(dataset, params)
    rows = parse_sdmx(data)
    load_indicator(db, rows, indicator, loaded_at)
    print(f"  ✓ {indicator}: {len(rows)} rows")


def run():
    print(f"[{datetime.now(timezone.utc).isoformat()}] EU Government Finance pipeline")
    loaded_at = datetime.now(timezone.utc).isoformat()
    with duckdb.connect(DB_PATH) as db:
        for dataset, params, indicator in FETCHES:
            try:
                fetch_and_load(db, dataset, params, indicator, loaded_at)
            except Exception as e:
                print(f"  ✗ {indicator}: {e}")
        db.execute(
            """INSERT OR REPLACE INTO meta_datasets
               (id, country, name, description, source_url, licence, priority)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            list(DATASET_META),
        )
    print("Done.")


if __name__ == "__main__":
    run()
