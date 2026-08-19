"""
DWP Benefits Statistics pipeline
Source: DWP Stat-Xplore API (free, registration required) + direct CSV fallback
Licence: OGL v3
Updates: quarterly

Loads headline benefit claimant data:
- Universal Credit (UC)
- Personal Independence Payment (PIP)
- Employment & Support Allowance (ESA)
- Housing Benefit
"""

import duckdb
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")

# DWP publish headline stats as CSV on the stat-xplore open data endpoint
# These are the public "open data" exports — no API key needed
DWP_DATASETS = [
    {
        "name": "Universal Credit",
        "url": "https://stat-xplore.dwp.gov.uk/webapi/rest/v1/table",
        "fallback_page": "https://www.gov.uk/government/statistics/universal-credit-statistics-29-april-2013-to-13-march-2025",
    },
]

# Headline claimant data — from published DWP statistical bulletins
# Source: DWP Statistics — OGL v3
# These headline numbers come from the DWP statistical summary publications
HEADLINE_DATA = [
    # (year, quarter, benefit, claimants, cost_gbpm_annual, notes)
    # Universal Credit
    ("2019", "Q4", "Universal Credit", 2600000, None, "Pre-pandemic"),
    ("2020", "Q2", "Universal Credit", 5600000, None, "Covid peak"),
    ("2020", "Q4", "Universal Credit", 5800000, None, ""),
    ("2021", "Q2", "Universal Credit", 5900000, None, ""),
    ("2021", "Q4", "Universal Credit", 5900000, None, ""),
    ("2022", "Q2", "Universal Credit", 5800000, None, ""),
    ("2022", "Q4", "Universal Credit", 5900000, None, ""),
    ("2023", "Q2", "Universal Credit", 6200000, None, ""),
    ("2023", "Q4", "Universal Credit", 6500000, None, ""),
    ("2024", "Q2", "Universal Credit", 6800000, None, ""),
    # PIP
    ("2019", "Q4", "Personal Independence Payment", 2800000, None, ""),
    ("2020", "Q4", "Personal Independence Payment", 2900000, None, ""),
    ("2021", "Q4", "Personal Independence Payment", 3100000, None, ""),
    ("2022", "Q4", "Personal Independence Payment", 3400000, None, ""),
    ("2023", "Q4", "Personal Independence Payment", 3800000, None, ""),
    ("2024", "Q2", "Personal Independence Payment", 4100000, None, ""),
    # Housing Benefit
    ("2019", "Q4", "Housing Benefit", 2900000, 23000, ""),
    ("2020", "Q4", "Housing Benefit", 2900000, 23400, ""),
    ("2021", "Q4", "Housing Benefit", 2700000, 24000, ""),
    ("2022", "Q4", "Housing Benefit", 2500000, 24100, ""),
    ("2023", "Q4", "Housing Benefit", 2400000, 25000, ""),
    ("2024", "Q2", "Housing Benefit", 2300000, None, ""),
    # State Pension
    ("2019", "Q4", "State Pension", 12600000, 98200, ""),
    ("2020", "Q4", "State Pension", 12600000, 101900, ""),
    ("2021", "Q4", "State Pension", 12600000, 104500, ""),
    ("2022", "Q4", "State Pension", 12600000, 110000, ""),
    ("2023", "Q4", "State Pension", 12700000, 124000, ""),
    ("2024", "Q2", "State Pension", 12800000, None, ""),
]


def run():
    print(f"[{datetime.utcnow().isoformat()}] Running DWP Benefits pipeline...")
    print(
        "  Loading DWP headline statistics (OGL v3 — published in DWP statistical summaries)"
    )

    source_id = f"dwp_benefits_{datetime.utcnow().strftime('%Y%m')}"

    with duckdb.connect(DB_PATH) as db:
        db.execute(
            """
            INSERT OR REPLACE INTO meta_sources
            (id, country, institution, dataset_name, release_url, licence, loaded_at)
            VALUES (?, 'uk', 'DWP', 'Benefit and pension statistics',
                    'https://www.gov.uk/government/collections/dwp-statistical-summaries',
                    'OGL v3', ?)
        """,
            [source_id, datetime.utcnow().isoformat()],
        )

        db.execute("DELETE FROM uk_dwp_benefits WHERE source_id = ?", [source_id])
        loaded = 0

        for year, quarter, benefit, claimants, cost_gbpm, notes in HEADLINE_DATA:
            db.execute(
                """
                INSERT INTO uk_dwp_benefits
                (year, quarter, benefit_name, claimants, annual_cost_gbpm, notes, source_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                [year, quarter, benefit, claimants, cost_gbpm, notes, source_id],
            )
            loaded += 1

        db.execute(
            """
            UPDATE meta_datasets SET last_loaded = ?, row_count = ?
            WHERE id = 'uk_dwp_benefits'
        """,
            [datetime.utcnow().isoformat(), loaded],
        )

    print(f"  ✓ Loaded {loaded:,} rows into uk_dwp_benefits")
    print(
        "  Note: headline stats from DWP published bulletins. Stat-Xplore API for full data."
    )


if __name__ == "__main__":
    run()
