"""Run on VPS to create EU tables. Execute once before running EU pipelines."""

import duckdb
import os

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")

TABLES = [
    """CREATE TABLE IF NOT EXISTS eu_government_finance (
        country   VARCHAR,
        year      INTEGER,
        indicator VARCHAR,
        value     DOUBLE,
        loaded_at VARCHAR,
        PRIMARY KEY (country, year, indicator)
    )""",
    """CREATE TABLE IF NOT EXISTS eu_tax_revenue (
        country      VARCHAR,
        year         INTEGER,
        value_pct_gdp DOUBLE,
        loaded_at    VARCHAR,
        PRIMARY KEY (country, year)
    )""",
    """CREATE TABLE IF NOT EXISTS eu_public_employment (
        country               VARCHAR,
        year                  INTEGER,
        employment_thousands  DOUBLE,
        loaded_at             VARCHAR,
        PRIMARY KEY (country, year)
    )""",
    """CREATE TABLE IF NOT EXISTS eu_tax_breakdown (
        country   VARCHAR,
        year      INTEGER,
        indicator VARCHAR,
        value     DOUBLE,
        loaded_at VARCHAR,
        PRIMARY KEY (country, year, indicator)
    )""",
    """CREATE TABLE IF NOT EXISTS eu_labour_tax_wedge (
        country      VARCHAR,
        year         INTEGER,
        income_level VARCHAR,
        tax_wedge_pct DOUBLE,
        loaded_at    VARCHAR,
        PRIMARY KEY (country, year, income_level)
    )""",
    """CREATE TABLE IF NOT EXISTS eu_tax_rates (
        country  VARCHAR,
        tax_type VARCHAR,
        rate     DOUBLE,
        year     INTEGER,
        source   VARCHAR,
        loaded_at VARCHAR,
        PRIMARY KEY (country, tax_type, year)
    )""",
    """CREATE TABLE IF NOT EXISTS eu_vat_rates (
        country       VARCHAR,
        standard_rate DOUBLE,
        reduced_rate  DOUBLE,
        year          INTEGER,
        source        VARCHAR,
        loaded_at     VARCHAR,
        PRIMARY KEY (country, year)
    )""",
]

with duckdb.connect(DB_PATH) as db:
    for ddl in TABLES:
        db.execute(ddl)
        name = ddl.split("IF NOT EXISTS")[1].split("(")[0].strip()
        print(f"  ✓ {name}")
print("EU schema ready.")
