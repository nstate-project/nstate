"""
EU VAT Rates — static lookup table
Standard and primary reduced VAT rates per EU member state.
Source: EC VAT Rates Applied in the Member States 2024.
https://taxation-customs.ec.europa.eu/taxation-1/value-added-tax-vat_en

VAT rates change rarely. Refresh when EC publishes its annual update.
Writes to: eu_vat_rates
"""

import duckdb
import os
from datetime import datetime, timezone

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")

# Standard rate, primary reduced rate (2024)
# Source: EC "VAT rates applied in the Member States of the European Union"
# HU has the highest standard rate in the EU (27%)
# LU has the lowest (17%)
# FI raised to 25.5% in Sept 2024
VAT_RATES = {
    #  code  standard  reduced
    "AT": (20.0, 10.0),
    "BE": (21.0, 6.0),
    "BG": (20.0, 9.0),
    "CY": (19.0, 5.0),
    "CZ": (21.0, 12.0),
    "DE": (19.0, 7.0),
    "DK": (25.0, 0.0),  # Denmark has no reduced rate
    "EE": (22.0, 9.0),
    "EL": (24.0, 13.0),
    "ES": (21.0, 10.0),
    "FI": (25.5, 14.0),
    "FR": (20.0, 10.0),
    "HR": (25.0, 13.0),
    "HU": (27.0, 5.0),
    "IE": (23.0, 13.5),
    "IT": (22.0, 10.0),
    "LT": (21.0, 9.0),
    "LU": (17.0, 8.0),
    "LV": (21.0, 12.0),
    "MT": (18.0, 7.0),
    "NL": (21.0, 9.0),
    "PL": (23.0, 8.0),
    "PT": (23.0, 13.0),
    "RO": (19.0, 9.0),
    "SE": (25.0, 12.0),
    "SI": (22.0, 9.5),
    "SK": (20.0, 10.0),
    # EEA/EFTA — not EU members but relevant for cross-country comparison
    "NO": (25.0, 15.0),  # Norway: standard 25%, reduced 15% (food)
    "IS": (24.0, 11.0),  # Iceland: standard 24%, reduced 11% (food, accommodation)
    "CH": (
        8.1,
        2.6,
    ),  # Switzerland: standard 8.1%, reduced 2.6% (food, books); raised Aug 2024
    "LI": (8.1, 2.6),  # Liechtenstein: in VAT union with Switzerland
}

DATA_YEAR = 2024
SOURCE = "EC VAT Rates Applied in the Member States of the European Union 2024"


def run():
    print(f"[{datetime.now(timezone.utc).isoformat()}] EU VAT Rates pipeline")
    loaded_at = datetime.now(timezone.utc).isoformat()
    count = 0
    with duckdb.connect(DB_PATH) as db:
        for country, (standard, reduced) in VAT_RATES.items():
            db.execute(
                """INSERT OR REPLACE INTO eu_vat_rates
                   (country, standard_rate, reduced_rate, year, source, loaded_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                [
                    country,
                    standard,
                    reduced if reduced > 0 else None,
                    DATA_YEAR,
                    SOURCE,
                    loaded_at,
                ],
            )
            count += 1
        db.execute(
            """INSERT OR REPLACE INTO meta_datasets
               (id, country, name, description, source_url, licence, priority)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                "eu_vat_rates",
                "eu",
                "EU VAT Rates",
                "Standard and reduced VAT rates per EU member state (2024)",
                "https://taxation-customs.ec.europa.eu/taxation-1/value-added-tax-vat_en",
                "EC reuse policy",
                2,
            ],
        )
    print(f"  ✓ {count} countries loaded")
    print("Done.")


if __name__ == "__main__":
    run()
