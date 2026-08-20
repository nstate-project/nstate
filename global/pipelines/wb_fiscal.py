"""
World Bank WDI — Central Government Fiscal Data (annual, ~170 countries)
Indicators sourced from IMF Government Finance Statistics via World Bank WDI.

Indicators loaded:
  GC.DOD.TOTL.GD.ZS  → debt_pct_gdp          (central govt gross debt % GDP)
  GC.XPN.TOTL.GD.ZS  → expenditure_pct_gdp   (central govt expense % GDP)
  GC.REV.TOTL.GD.ZS  → revenue_pct_gdp       (central govt revenue % GDP)
  GC.NLD.TOTL.GD.ZS  → surplus_pct_gdp       (net lending + / net borrowing -)

Note: "central government" (not general government) — typically lower than Eurostat
EDP figures which use "general government". Use for cross-country comparison, not
direct comparison with EU Maastricht figures.

Writes to: wb_fiscal, wb_countries
"""

import duckdb
import os
import urllib.request
import json
from datetime import datetime, timezone

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")
WB_BASE = "https://api.worldbank.org/v2"

INDICATORS = {
    "GC.DOD.TOTL.GD.ZS": "debt_pct_gdp",
    "GC.XPN.TOTL.GD.ZS": "expenditure_pct_gdp",
    "GC.REV.TOTL.GD.ZS": "revenue_pct_gdp",
    "GC.NLD.TOTL.GD.ZS": "surplus_pct_gdp",
}

# Aggregate/regional codes to skip
SKIP_ISO2 = {
    "1A",
    "1W",
    "4E",
    "7E",
    "8S",
    "B8",
    "EU",
    "F1",
    "OE",
    "S1",
    "S2",
    "S3",
    "S4",
    "T2",
    "T3",
    "T4",
    "T5",
    "T6",
    "T7",
    "V1",
    "V2",
    "V3",
    "V4",
    "XC",
    "XD",
    "XE",
    "XF",
    "XG",
    "XH",
    "XI",
    "XJ",
    "XL",
    "XM",
    "XN",
    "XO",
    "XP",
    "XQ",
    "XT",
    "XU",
    "XY",
    "Z4",
    "Z7",
    "ZB",
    "ZF",
    "ZG",
    "ZH",
    "ZI",
    "ZJ",
    "ZQ",
    "ZT",
}


def fetch_indicator(wb_code: str) -> list[dict]:
    url = f"{WB_BASE}/country/all/indicator/{wb_code}?format=json&per_page=30000&mrv=30"
    with urllib.request.urlopen(url, timeout=60) as r:
        payload = json.loads(r.read())
    # WB returns [metadata, data_array]
    return payload[1] if len(payload) > 1 and payload[1] else []


def fetch_countries() -> list[dict]:
    url = f"{WB_BASE}/country?format=json&per_page=400"
    with urllib.request.urlopen(url, timeout=30) as r:
        payload = json.loads(r.read())
    return payload[1] if len(payload) > 1 and payload[1] else []


def run():
    print(f"[{datetime.now(timezone.utc).isoformat()}] World Bank Fiscal pipeline")
    loaded_at = datetime.now(timezone.utc).isoformat()

    with duckdb.connect(DB_PATH) as db:
        # Load country metadata
        # WB /country endpoint: id = WB 3-letter code, iso2Code = actual ISO2
        # wb_fiscal uses ISO2 codes, so wb_countries.iso2 must also be ISO2.
        try:
            countries = fetch_countries()
            loaded = 0
            for c in countries:
                iso2 = (c.get("iso2Code") or "").strip()
                if not iso2 or len(iso2) != 2:
                    continue  # skip WB aggregates (no valid ISO2)
                db.execute(
                    """INSERT OR REPLACE INTO wb_countries
                       (iso2, iso3, name, region, income_group, loaded_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    [
                        iso2,
                        c.get("id") or iso2,
                        c.get("name", ""),
                        (c.get("region") or {}).get("value", ""),
                        (c.get("incomeLevel") or {}).get("value", ""),
                        loaded_at,
                    ],
                )
                loaded += 1
            print(f"  ✓ wb_countries: {loaded} country entries")
        except Exception as e:
            print(f"  ✗ countries: {e}")

        # Load fiscal indicators
        for wb_code, indicator in INDICATORS.items():
            try:
                rows = fetch_indicator(wb_code)
                count = 0
                for row in rows:
                    iso2 = (row.get("country") or {}).get("id", "")
                    if not iso2 or iso2 in SKIP_ISO2:
                        continue
                    value = row.get("value")
                    if value is None:
                        continue
                    try:
                        year = int(row["date"])
                    except (ValueError, KeyError):
                        continue
                    db.execute(
                        """INSERT OR REPLACE INTO wb_fiscal
                           (country, year, indicator, value, loaded_at)
                           VALUES (?, ?, ?, ?, ?)""",
                        [iso2, year, indicator, value, loaded_at],
                    )
                    count += 1
                print(f"  ✓ {indicator} ({wb_code}): {count} rows")
            except Exception as e:
                print(f"  ✗ {indicator}: {e}")

        db.execute(
            """INSERT OR REPLACE INTO meta_datasets
               (id, country, name, description, source_url, licence, priority)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                "wb_fiscal",
                "world",
                "World Bank Central Government Fiscal Data",
                "Central govt debt, expenditure, revenue, surplus as % GDP (WDI, ~170 countries)",
                "https://databank.worldbank.org/source/world-development-indicators",
                "CC BY 4.0",
                3,
            ],
        )
    print("Done.")


if __name__ == "__main__":
    run()
