"""Run on VPS to add new tables and dataset registrations."""

import duckdb
import os

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")

TABLES = [
    (
        "uk_ons_cpih",
        """
        CREATE TABLE IF NOT EXISTS uk_ons_cpih (
            period_label    VARCHAR,
            aggregate_code  VARCHAR,
            aggregate_label VARCHAR,
            index_value     DECIMAL(10,4),
            source_id       VARCHAR,
            _loaded_at      TIMESTAMP DEFAULT current_timestamp
        )""",
    ),
    (
        "uk_ons_labour_market",
        """
        CREATE TABLE IF NOT EXISTS uk_ons_labour_market (
            period_label        VARCHAR,
            unit_of_measure     VARCHAR,
            economic_activity   VARCHAR,
            age_group           VARCHAR,
            sex                 VARCHAR,
            seasonal_adjustment VARCHAR,
            value               DECIMAL(18,2),
            source_id           VARCHAR,
            _loaded_at          TIMESTAMP DEFAULT current_timestamp
        )""",
    ),
    (
        "uk_ons_gdp",
        """
        CREATE TABLE IF NOT EXISTS uk_ons_gdp (
            period_label    VARCHAR,
            industry_code   VARCHAR,
            industry_label  VARCHAR,
            index_value     DECIMAL(10,4),
            source_id       VARCHAR,
            _loaded_at      TIMESTAMP DEFAULT current_timestamp
        )""",
    ),
    (
        "uk_ons_house_prices",
        """
        CREATE TABLE IF NOT EXISTS uk_ons_house_prices (
            year            VARCHAR,
            month_label     VARCHAR,
            geography_code  VARCHAR,
            property_type   VARCHAR,
            build_status    VARCHAR,
            measure         VARCHAR,
            value           DECIMAL(18,2),
            source_id       VARCHAR,
            _loaded_at      TIMESTAMP DEFAULT current_timestamp
        )""",
    ),
    (
        "uk_ons_retail_sales",
        """
        CREATE TABLE IF NOT EXISTS uk_ons_retail_sales (
            period_label        VARCHAR,
            sector_code         VARCHAR,
            sector_label        VARCHAR,
            price_type          VARCHAR,
            seasonal_adjustment VARCHAR,
            value               DECIMAL(10,4),
            source_id           VARCHAR,
            _loaded_at          TIMESTAMP DEFAULT current_timestamp
        )""",
    ),
    (
        "uk_ons_wages",
        """
        CREATE TABLE IF NOT EXISTS uk_ons_wages (
            year            VARCHAR,
            geography_code  VARCHAR,
            percentile      VARCHAR,
            sex             VARCHAR,
            working_pattern VARCHAR,
            measure         VARCHAR,
            sector          VARCHAR,
            value           DECIMAL(10,2),
            source_id       VARCHAR,
            _loaded_at      TIMESTAMP DEFAULT current_timestamp
        )""",
    ),
    (
        "uk_hmrc_tax_receipts",
        """
        CREATE TABLE IF NOT EXISTS uk_hmrc_tax_receipts (
            year            INTEGER,
            tax_category    VARCHAR,
            measure_label   VARCHAR,
            value_gbpm      DECIMAL(18,2),
            source_id       VARCHAR,
            _loaded_at      TIMESTAMP DEFAULT current_timestamp
        )""",
    ),
    (
        "uk_pesa_functional",
        """
        CREATE TABLE IF NOT EXISTS uk_pesa_functional (
            year            INTEGER,
            function_name   VARCHAR,
            value_gbpm      DECIMAL(18,2),
            source_id       VARCHAR,
            _loaded_at      TIMESTAMP DEFAULT current_timestamp
        )""",
    ),
    (
        "uk_pesa_departmental",
        """
        CREATE TABLE IF NOT EXISTS uk_pesa_departmental (
            year                INTEGER,
            department_name     VARCHAR,
            expenditure_type    VARCHAR,
            value_gbpm          DECIMAL(18,2),
            source_id           VARCHAR,
            _loaded_at          TIMESTAMP DEFAULT current_timestamp
        )""",
    ),
    (
        "uk_dwp_benefits",
        """
        CREATE TABLE IF NOT EXISTS uk_dwp_benefits (
            year                VARCHAR,
            quarter             VARCHAR,
            benefit_name        VARCHAR,
            claimants           INTEGER,
            annual_cost_gbpm    DECIMAL(18,2),
            notes               VARCHAR,
            source_id           VARCHAR,
            _loaded_at          TIMESTAMP DEFAULT current_timestamp
        )""",
    ),
    (
        "uk_spend_25k",
        """
        CREATE TABLE IF NOT EXISTS uk_spend_25k (
            period_raw      VARCHAR,
            department      VARCHAR,
            supplier        VARCHAR,
            amount_gbp      DECIMAL(18,2),
            expense_type    VARCHAR,
            description     VARCHAR,
            source_url      VARCHAR,
            source_id       VARCHAR,
            _loaded_at      TIMESTAMP DEFAULT current_timestamp
        )""",
    ),
    (
        "uk_contracts",
        """
        CREATE TABLE IF NOT EXISTS uk_contracts (
            ocid            VARCHAR,
            award_date      VARCHAR,
            buyer_name      VARCHAR,
            supplier_name   VARCHAR,
            title           VARCHAR,
            value_gbp       DECIMAL(18,2),
            currency        VARCHAR DEFAULT 'GBP',
            source_id       VARCHAR,
            _loaded_at      TIMESTAMP DEFAULT current_timestamp
        )""",
    ),
]

DATASETS = [
    (
        "uk_ons_cpih",
        "uk",
        "ONS CPIH Inflation",
        "Monthly Consumer Prices Index including owner occupiers' housing costs",
        "https://api.beta.ons.gov.uk/v1/datasets/cpih01",
        3,
    ),
    (
        "uk_ons_labour_market",
        "uk",
        "ONS Labour Market",
        "UK employment, unemployment and economic inactivity statistics",
        "https://api.beta.ons.gov.uk/v1/datasets/labour-market",
        3,
    ),
    (
        "uk_ons_gdp",
        "uk",
        "ONS GDP Monthly",
        "UK GDP monthly estimate by industry (index, 2019=100)",
        "https://api.beta.ons.gov.uk/v1/datasets/gdp-to-four-decimal-places",
        3,
    ),
    (
        "uk_ons_house_prices",
        "uk",
        "ONS House Prices",
        "House prices and sales by local authority and property type",
        "https://api.beta.ons.gov.uk/v1/datasets/house-prices-local-authority",
        4,
    ),
    (
        "uk_ons_retail_sales",
        "uk",
        "ONS Retail Sales Index",
        "Monthly retail sales volumes and values by sector",
        "https://api.beta.ons.gov.uk/v1/datasets/retail-sales-index",
        4,
    ),
    (
        "uk_ons_wages",
        "uk",
        "ONS ASHE — Wages",
        "Annual earnings by region, public vs private sector, percentiles",
        "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-25",
        4,
    ),
    (
        "uk_hmrc_tax_receipts",
        "uk",
        "HMRC Tax Receipts",
        "UK tax and NIC receipts by category back to 1999 (GBP millions)",
        "https://www.gov.uk/government/statistics/hmrc-tax-and-nics-receipts-for-the-uk",
        2,
    ),
    (
        "uk_pesa_functional",
        "uk",
        "PESA — Functional Expenditure",
        "Total managed expenditure by function (NHS, defence, education etc) — PESA 2025",
        "https://www.gov.uk/government/statistics/public-expenditure-statistical-analyses-2025",
        2,
    ),
    (
        "uk_pesa_departmental",
        "uk",
        "PESA — Departmental Expenditure",
        "DEL and AME expenditure by government department — PESA 2025",
        "https://www.gov.uk/government/statistics/public-expenditure-statistical-analyses-2025",
        2,
    ),
    (
        "uk_dwp_benefits",
        "uk",
        "DWP Benefits Statistics",
        "Claimant counts for UC, PIP, Housing Benefit, State Pension by quarter",
        "https://www.gov.uk/government/collections/dwp-statistical-summaries",
        2,
    ),
    (
        "uk_spend_25k",
        "uk",
        "Government Spend Over £25,000",
        "Individual transactions over £25,000 by dept, supplier and date",
        "https://www.gov.uk/government/collections/spending-transparency",
        2,
    ),
    (
        "uk_contracts",
        "uk",
        "Government Contracts (FTS)",
        "Contract award notices from Find a Tender Service — buyer, supplier, value",
        "https://www.find-tender.service.gov.uk/api/1.0/ocds/",
        3,
    ),
]

with duckdb.connect(DB_PATH) as db:
    for table_name, ddl in TABLES:
        db.execute(ddl)
        print(f"  ✓ {table_name}")

    for row in DATASETS:
        db.execute(
            """
            INSERT OR IGNORE INTO meta_datasets
            (id, country, name, description, source_url, licence, priority)
            VALUES (?, ?, ?, ?, ?, 'OGL v3', ?)
        """,
            list(row),
        )

    all_tables = [t[0] for t in db.execute("SHOW TABLES").fetchall()]
    all_datasets = db.execute(
        "SELECT id FROM meta_datasets WHERE country='uk'"
    ).fetchall()
    print(f"\nTotal tables: {len(all_tables)}")
    print(f"UK datasets registered: {len(all_datasets)}")
