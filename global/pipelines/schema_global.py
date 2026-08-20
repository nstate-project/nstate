"""Create global (non-Eurostat) tables. Run once on VPS before pipelines."""

import duckdb
import os

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")

TABLES = [
    """CREATE TABLE IF NOT EXISTS wb_fiscal (
        country   VARCHAR,
        year      INTEGER,
        indicator VARCHAR,
        value     DOUBLE,
        loaded_at VARCHAR,
        PRIMARY KEY (country, year, indicator)
    )""",
    """CREATE TABLE IF NOT EXISTS wb_price_levels (
        country  VARCHAR,
        year     INTEGER,
        pli      DOUBLE,
        loaded_at VARCHAR,
        PRIMARY KEY (country, year)
    )""",
    """CREATE TABLE IF NOT EXISTS wb_countries (
        iso2     VARCHAR PRIMARY KEY,
        iso3     VARCHAR,
        name     VARCHAR,
        region   VARCHAR,
        income_group VARCHAR,
        loaded_at VARCHAR
    )""",
]

with duckdb.connect(DB_PATH) as db:
    for ddl in TABLES:
        db.execute(ddl)
        name = ddl.split("IF NOT EXISTS")[1].split("(")[0].strip()
        print(f"  ✓ {name}")
print("Global schema ready.")
