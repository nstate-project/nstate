"""
EU Statutory Tax Rates — static lookup table
Top marginal personal income tax rate and headline corporate tax rate per country.
Source: OECD Taxing Wages 2024, EC Taxation Trends in the European Union 2024.

These change rarely (once/year at most). Refresh when EC publishes annual survey.
Writes to: eu_tax_rates
"""

import duckdb
import os
from datetime import datetime, timezone

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")

# Top marginal personal income tax rate (state + sub-central statutory rate, 2024)
# Source: OECD Taxing Wages 2024 / EC Taxation Trends 2024
PERSONAL_TOP_RATES = {
    "AT": 50.0,
    "BE": 50.0,
    "BG": 10.0,
    "CY": 35.0,
    "CZ": 23.0,
    "DE": 45.0,
    "DK": 55.9,
    "EE": 22.0,
    "EL": 44.0,
    "ES": 47.0,
    "FI": 51.4,
    "FR": 45.0,
    "HR": 30.0,
    "HU": 15.0,
    "IE": 40.0,
    "IT": 43.0,
    "LT": 32.0,
    "LU": 42.0,
    "LV": 31.0,
    "MT": 35.0,
    "NL": 49.5,
    "PL": 32.0,
    "PT": 48.0,
    "RO": 10.0,
    "SE": 52.3,
    "SI": 50.0,
    "SK": 25.0,
    # EEA/EFTA — OECD Taxing Wages 2024
    "NO": 47.4,  # 22% bracket + 17.4% surtax top rate
    "IS": 46.25,  # combined state + municipal
    "CH": 40.0,  # federal 11.5% + cantonal, Zurich reference; varies widely by canton
    "LI": 22.4,  # Liechtenstein (low flat-rate system)
}

# Headline corporate income tax rate (2024)
# Source: EC Taxation Trends 2024 / OECD CIT rates
CORPORATE_RATES = {
    "AT": 24.0,
    "BE": 25.0,
    "BG": 10.0,
    "CY": 12.5,
    "CZ": 21.0,
    "DE": 29.9,
    "DK": 22.0,
    "EE": 22.0,
    "EL": 22.0,
    "ES": 25.0,
    "FI": 20.0,
    "FR": 25.0,
    "HR": 18.0,
    "HU": 9.0,
    "IE": 12.5,
    "IT": 27.9,
    "LT": 16.0,
    "LU": 24.9,
    "LV": 20.0,
    "MT": 35.0,
    "NL": 25.8,
    "PL": 19.0,
    "PT": 21.0,
    "RO": 16.0,
    "SE": 20.6,
    "SI": 19.0,
    "SK": 21.0,
    # EEA/EFTA — OECD CIT rates 2024
    "NO": 22.0,  # standard CIT rate
    "IS": 20.0,
    "CH": 19.7,  # combined federal (8.5%) + typical cantonal; varies by canton
    "LI": 12.5,
}

DATA_YEAR = 2024
SOURCE = "OECD Taxing Wages 2024; EC Taxation Trends in the European Union 2024"


def run():
    print(f"[{datetime.now(timezone.utc).isoformat()}] EU Statutory Tax Rates pipeline")
    loaded_at = datetime.now(timezone.utc).isoformat()
    count = 0
    with duckdb.connect(DB_PATH) as db:
        for country, rate in PERSONAL_TOP_RATES.items():
            db.execute(
                """INSERT OR REPLACE INTO eu_tax_rates
                   (country, tax_type, rate, year, source, loaded_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                [country, "personal_top_rate", rate, DATA_YEAR, SOURCE, loaded_at],
            )
            count += 1
        for country, rate in CORPORATE_RATES.items():
            db.execute(
                """INSERT OR REPLACE INTO eu_tax_rates
                   (country, tax_type, rate, year, source, loaded_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                [country, "corporate_rate", rate, DATA_YEAR, SOURCE, loaded_at],
            )
            count += 1
        db.execute(
            """INSERT OR REPLACE INTO meta_datasets
               (id, country, name, description, source_url, licence, priority)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                "eu_tax_rates",
                "eu",
                "EU Statutory Tax Rates",
                "Top marginal personal income tax rate and corporate tax rate per country (2024)",
                "https://taxation-customs.ec.europa.eu/taxation-1/economic-analysis-taxation/taxation-trends-european-union_en",
                "EC reuse policy",
                2,
            ],
        )
    print(f"  ✓ {count} rate rows loaded")
    print("Done.")


if __name__ == "__main__":
    run()
