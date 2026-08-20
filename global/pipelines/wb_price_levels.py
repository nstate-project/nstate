"""
World Bank WDI — Global Price Level Indices (annual, ~170 countries)
Derives Price Level Index (PLI) from PPP conversion factor and official exchange rate.

Method:
  PLI_i = (PA.NUS.PPP_i / PA.NUS.FCRF_i) * 100
  USA is the base: PPP_USA = 1, XR_USA = 1, so PLI_USA = 100.
  PLI > 100 → more expensive than USA; PLI < 100 → cheaper.

Note: Eurostat prc_ppp_ind uses EU27=100. This table uses USA=100. The two are
not directly comparable in absolute terms but both correctly rank countries
by relative price level.

Writes to: wb_price_levels
"""

import duckdb
import os
import urllib.request
import json
from datetime import datetime, timezone

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")
WB_BASE = "https://api.worldbank.org/v2"

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


def fetch_indicator(wb_code: str) -> dict[tuple[str, int], float]:
    url = f"{WB_BASE}/country/all/indicator/{wb_code}?format=json&per_page=30000&mrv=30"
    with urllib.request.urlopen(url, timeout=60) as r:
        payload = json.loads(r.read())
    data = payload[1] if len(payload) > 1 and payload[1] else []
    result = {}
    for row in data:
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
        result[(iso2, year)] = value
    return result


def run():
    print(
        f"[{datetime.now(timezone.utc).isoformat()}] World Bank Price Levels pipeline"
    )
    loaded_at = datetime.now(timezone.utc).isoformat()

    print("  Fetching PPP conversion factors...")
    ppp = fetch_indicator("PA.NUS.PPP")
    print("  Fetching official exchange rates...")
    xr = fetch_indicator("PA.NUS.FCRF")

    count = 0
    with duckdb.connect(DB_PATH) as db:
        for (iso2, year), ppp_val in ppp.items():
            xr_val = xr.get((iso2, year))
            if not xr_val or xr_val == 0:
                continue
            pli = (ppp_val / xr_val) * 100
            db.execute(
                """INSERT OR REPLACE INTO wb_price_levels
                   (country, year, pli, loaded_at)
                   VALUES (?, ?, ?, ?)""",
                [iso2, year, round(pli, 2), loaded_at],
            )
            count += 1

        db.execute(
            """INSERT OR REPLACE INTO meta_datasets
               (id, country, name, description, source_url, licence, priority)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                "wb_price_levels",
                "world",
                "World Bank Price Level Indices",
                "Price Level Index (USA=100) derived from PPP/XR ratio for ~170 countries",
                "https://databank.worldbank.org/source/world-development-indicators",
                "CC BY 4.0",
                3,
            ],
        )
    print(f"  ✓ {count} PLI rows written")
    print("Done.")


if __name__ == "__main__":
    run()
