"""
EU Comparative Price Levels pipeline — Eurostat prc_ppp_ind
Price Level Indices (EU27_2020=100) for 13 expenditure categories.
A value of 85 means 15% cheaper than the EU average for that category.

Covers all 27 EU member states + EU27_2020 aggregate, annually 1995–2024.
Writes to: eu_price_levels
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
    # EEA/EFTA
    "NO",
    "IS",
    "CH",
    "LI",
    # EU candidate countries and other Eurostat PPP participants
    "ME",
    "RS",
    "MK",
    "AL",
    "BA",
    "XK",
    "TR",
    "UK",
]

# Key expenditure categories (top-level COICOP headings)
CATEGORIES = [
    "GDP",  # Overall price level
    "A0101",  # Food and non-alcoholic beverages
    "A0102",  # Alcoholic beverages, tobacco
    "A0103",  # Clothing and footwear
    "A0104",  # Housing, water, electricity, gas
    "A0105",  # Household furnishings and equipment
    "A0106",  # Health
    "A0107",  # Transport
    "A0108",  # Communication
    "A0109",  # Recreation and culture
    "A0110",  # Education
    "A0111",  # Restaurants and hotels
    "A0112",  # Miscellaneous goods and services
]


def fetch_pli() -> list[dict]:
    geo_str = "&".join(f"geo={c}" for c in ALL_EU)
    cat_str = "&".join(f"ppp_cat={c}" for c in CATEGORIES)
    url = (
        f"{BASE}/prc_ppp_ind?format=JSON&lang=EN"
        f"&na_item=PLI_EU27_2020&{cat_str}&{geo_str}"
    )
    with urllib.request.urlopen(url, timeout=60) as r:
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
    print(f"[{datetime.now(timezone.utc).isoformat()}] EU Price Levels pipeline")
    loaded_at = datetime.now(timezone.utc).isoformat()
    rows = fetch_pli()
    print(f"  Fetched {len(rows)} rows from Eurostat")
    count = 0
    with duckdb.connect(DB_PATH) as db:
        for row in rows:
            try:
                year = int(row["time"])
            except (ValueError, KeyError):
                continue
            db.execute(
                """INSERT OR REPLACE INTO eu_price_levels
                   (country, year, category, pli, loaded_at)
                   VALUES (?, ?, ?, ?, ?)""",
                [row.get("geo"), year, row.get("ppp_cat"), row["value"], loaded_at],
            )
            count += 1
        db.execute(
            """INSERT OR REPLACE INTO meta_datasets
               (id, country, name, description, source_url, licence, priority)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                "eu_price_levels",
                "eu",
                "Eurostat Comparative Price Levels",
                "Price level indices (EU27=100) for 13 expenditure categories, all EU27, 1995–2024",
                "https://ec.europa.eu/eurostat/web/purchasing-power-parities",
                "Eurostat reuse policy",
                2,
            ],
        )
    print(f"  ✓ {count} rows loaded")
    print("Done.")


if __name__ == "__main__":
    run()
