"""
EU Labour Tax Wedge pipeline — Eurostat earn_nt_taxrate
Effective % of gross labour cost going to income tax + social contributions
for a single person without children, at three income levels.

Writes to: eu_labour_tax_wedge
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
    # EEA/EFTA — earn_nt_taxrate covers these
    "NO",
    "IS",
    "CH",
]

# ecase code → human-readable income level label
INCOME_LEVELS = [
    ("P1_NCH_AW67", "AW67", "67% of average wage"),
    ("P1_NCH_AW100", "AW100", "100% of average wage"),
    ("P1_NCH_AW125", "AW125", "125% of average wage"),
]


def fetch_wedge(ecase: str) -> list[dict]:
    geo_str = "&".join(f"geo={c}" for c in ALL_EU)
    url = f"{BASE}/earn_nt_taxrate?format=JSON&lang=EN&ecase={ecase}&{geo_str}"
    with urllib.request.urlopen(url, timeout=30) as r:
        d = json.loads(r.read())
    dims, sizes = d["id"], d["size"]
    dim_labels = {
        dd: {v: k for k, v in d["dimension"][dd]["category"]["index"].items()}
        for dd in dims
    }
    rows = []
    for key_str, value in d.get("value", {}).items():
        k = int(key_str)
        idxs = []
        for sz in reversed(sizes):
            idxs.append(k % sz)
            k //= sz
        row = {dd: dim_labels[dd][i] for dd, i in zip(dims, reversed(idxs))}
        row["value"] = value
        rows.append(row)
    return rows


def run():
    print(f"[{datetime.now(timezone.utc).isoformat()}] EU Labour Tax Wedge pipeline")
    loaded_at = datetime.now(timezone.utc).isoformat()
    with duckdb.connect(DB_PATH) as db:
        for ecase, level, label in INCOME_LEVELS:
            try:
                rows = fetch_wedge(ecase)
                count = 0
                for row in rows:
                    try:
                        year = int(row["time"])
                    except (ValueError, KeyError):
                        continue
                    db.execute(
                        """INSERT OR REPLACE INTO eu_labour_tax_wedge
                           (country, year, income_level, tax_wedge_pct, loaded_at)
                           VALUES (?, ?, ?, ?, ?)""",
                        [row.get("geo"), year, level, row["value"], loaded_at],
                    )
                    count += 1
                print(f"  ✓ {label}: {count} rows")
            except Exception as e:
                print(f"  ✗ {label}: {e}")
        db.execute(
            """INSERT OR REPLACE INTO meta_datasets
               (id, country, name, description, source_url, licence, priority)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                "eu_labour_tax_wedge",
                "eu",
                "Eurostat Labour Tax Wedge",
                "Effective % of gross labour cost going to tax for single person (annual)",
                "https://ec.europa.eu/eurostat/web/labour-market/earnings",
                "Eurostat reuse policy",
                2,
            ],
        )
    print("Done.")


if __name__ == "__main__":
    run()
