"""
EU Tax Breakdown pipeline — Eurostat gov_10a_taxag
Loads VAT, personal income tax, corporate income tax and social contributions
as % of GDP for all EU27 countries, annually 1995–2025.

Writes to: eu_tax_breakdown
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
    # EEA/EFTA — gov_10a_taxag covers VAT + excise for these; D51A/D51B may be sparse
    "NO",
    "IS",
]

INDICATORS = [
    ("D211", "vat_pct_gdp", "Value added tax (VAT)"),
    ("D51A", "personal_income_tax_pct_gdp", "Personal income tax"),
    ("D51B", "corporate_tax_pct_gdp", "Corporate income tax"),
    ("D613CE", "employee_social_contrib_pct_gdp", "Employee social contributions"),
    ("D611C", "employer_social_contrib_pct_gdp", "Employer social contributions"),
    ("D214A", "excise_duties_pct_gdp", "Excise duties"),
]


def fetch_eurostat(na_item: str) -> list[dict]:
    geo_str = "&".join(f"geo={c}" for c in ALL_EU)
    url = (
        f"{BASE}/gov_10a_taxag?format=JSON&lang=EN"
        f"&na_item={na_item}&unit=PC_GDP&sector=S13&freq=A&{geo_str}"
    )
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
    print(f"[{datetime.now(timezone.utc).isoformat()}] EU Tax Breakdown pipeline")
    loaded_at = datetime.now(timezone.utc).isoformat()
    with duckdb.connect(DB_PATH) as db:
        for na_item, indicator, label in INDICATORS:
            try:
                rows = fetch_eurostat(na_item)
                count = 0
                for row in rows:
                    try:
                        year = int(row["time"])
                    except (ValueError, KeyError):
                        continue
                    db.execute(
                        """INSERT OR REPLACE INTO eu_tax_breakdown
                           (country, year, indicator, value, loaded_at)
                           VALUES (?, ?, ?, ?, ?)""",
                        [row.get("geo"), year, indicator, row["value"], loaded_at],
                    )
                    count += 1
                print(f"  ✓ {label} ({indicator}): {count} rows")
            except Exception as e:
                print(f"  ✗ {label}: {e}")
        db.execute(
            """INSERT OR REPLACE INTO meta_datasets
               (id, country, name, description, source_url, licence, priority)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                "eu_tax_breakdown",
                "eu",
                "Eurostat Tax Breakdown",
                "VAT, income tax, corporate tax, social contributions as % GDP for EU27 (annual)",
                "https://ec.europa.eu/eurostat/web/government-finance-statistics",
                "Eurostat reuse policy",
                2,
            ],
        )
    print("Done.")


if __name__ == "__main__":
    run()
