"""
nstate query agent
Flow: question → intent (Haiku) → SQL (Sonnet) → DuckDB → narrative (Haiku)
Numbers come from DuckDB rows only. LLM writes prose around injected values.
"""

import os
import re
import json
import uuid
import httpx
import duckdb
import logging
from datetime import datetime

logger = logging.getLogger("nstate.agent")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HAIKU = "anthropic/claude-haiku-4-5"
SONNET = "anthropic/claude-sonnet-4-5"

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")

SCHEMA_SUMMARY = """
Available UK tables (all values OGL v3, sources cited in meta_sources):

-- CIVIL SERVICE (Cabinet Office, annual March) --
uk_civil_service_headcount
  period DATE          -- 31 March each year (2010–2024)
  department VARCHAR   -- 'All departments' for UK total
  headcount INTEGER    -- headcount of civil servants
  fte DECIMAL          -- full-time equivalent

-- INFLATION (ONS, monthly) --
uk_ons_cpih
  period_label VARCHAR      -- format: 'Mon-YY' e.g. 'Jan-26'. Latest: 'Jan-26'. Range: Apr-00 to Jan-26.
  aggregate_code VARCHAR    -- 'CP00' = Overall Index (headline CPIH). 'CP01'='Food'. 'CP04'='Housing'. etc.
  aggregate_label VARCHAR   -- e.g. 'Overall Index', '01 Food and non-alcoholic beverages'
  index_value DECIMAL       -- index value (2015=100). Year-on-year % change must be calculated manually.
  -- WORKING EXAMPLE (inflation rate year-on-year for Jan 2026):
  --   SELECT curr.period_label, curr.index_value, prev.index_value AS prev_year,
  --     ROUND(((curr.index_value-prev.index_value)/prev.index_value)*100,1) AS yoy_pct
  --   FROM uk_ons_cpih curr JOIN uk_ons_cpih prev
  --     ON prev.aggregate_code='CP00' AND prev.period_label='Jan-25'
  --   WHERE curr.aggregate_code='CP00' AND curr.period_label='Jan-26'
  -- NOTE: DO NOT use ORDER BY period_label — text sort is wrong. Filter by exact label like 'Jan-26','Dec-25'.

-- LABOUR MARKET (ONS, monthly) --
uk_ons_labour_market
  period_label VARCHAR        -- e.g. 'Feb-Apr 2025'
  unit_of_measure VARCHAR     -- 'Levels' or 'Rates'
  economic_activity VARCHAR   -- 'Economically Active', 'In Employment', 'Unemployed', 'Economically Inactive'
  age_group VARCHAR           -- e.g. '16-64', '16-24', '65+'
  sex VARCHAR                 -- 'All', 'Men', 'Women'
  seasonal_adjustment VARCHAR -- 'Seasonally Adjusted' or 'Not Seasonally Adjusted'
  value DECIMAL               -- count (levels) or percentage (rates)

-- GDP (ONS, monthly index) --
uk_ons_gdp
  period_label VARCHAR   -- e.g. 'Mar-26'
  industry_code VARCHAR  -- SIC letter e.g. 'A', 'B', 'total-output'
  industry_label VARCHAR -- e.g. 'A : Agriculture, forestry and fishing'
  index_value DECIMAL    -- GDP index (2019=100)

-- HOUSE PRICES (ONS, by local authority) --
uk_ons_house_prices
  year VARCHAR           -- LATEST AVAILABLE: '2022'. Range: '2012'–'2022'. Do NOT query year='2024' or '2023' — no data.
  month_label VARCHAR    -- abbreviated: 'mar', 'jun', 'sep', 'dec'
  geography_code VARCHAR -- local authority ONS code e.g. 'E08000028' (331 LAs, no UK-wide row)
  property_type VARCHAR  -- 'all', 'detached', 'semi-detached', 'terraced', 'flat-maisonette'
  build_status VARCHAR   -- 'all', 'newly-built', 'existing'
  measure VARCHAR        -- 'mean', 'median', 'lower-quartile', 'tenth-percentile', 'sales'
  value DECIMAL          -- GBP price (for price measures) or count (for 'sales')
  -- NOTE: to get a UK-wide average, use AVG(value) across all geography_codes
  -- WORKING EXAMPLE (UK average house price, latest data):
  --   SELECT ROUND(AVG(value),0) AS avg_price FROM uk_ons_house_prices
  --   WHERE measure='mean' AND year='2022' AND property_type='all' AND build_status='all'

-- RETAIL SALES (ONS, monthly) --
uk_ons_retail_sales
  period_label VARCHAR        -- e.g. 'Jan-26'
  sector_code VARCHAR         -- e.g. 'food-stores', 'non-store-retailing'
  sector_label VARCHAR
  price_type VARCHAR          -- 'Value of retail sales at current prices' or % change
  seasonal_adjustment VARCHAR
  value DECIMAL               -- index value or % change

-- PUBLIC/PRIVATE SECTOR WAGES (ONS ASHE, annual) --
uk_ons_wages
  year VARCHAR           -- e.g. '2023' (latest)
  geography_code VARCHAR -- ONS region code e.g. 'E12000001' to 'E12000009' for English regions
  percentile VARCHAR     -- EXACT VALUES: 'median', '10', '20', '25', '30', '40', '60', '70', '75', '80'
  sex VARCHAR            -- EXACT VALUES: 'all', 'male', 'female' (lowercase)
  working_pattern VARCHAR -- EXACT VALUES: 'full-time', 'part-time' (hyphenated lowercase)
  measure VARCHAR        -- one of: 'weekly-pay-gross' | 'hourly-pay-gross' | 'annual-pay-gross' | 'hourly-pay-excluding-overtime'
  sector VARCHAR         -- one of: 'all' | 'public-sector' | 'private-sector'  (lowercase, hyphenated — NOT title-case)
  value DECIMAL          -- GBP amount
-- WORKING EXAMPLE (copy the exact values):
--   SELECT AVG(value) FROM uk_ons_wages
--   WHERE sector='private-sector' AND measure='weekly-pay-gross'
--     AND percentile='median' AND sex='all' AND working_pattern='full-time' AND year='2023'

-- HMRC TAX RECEIPTS (HMRC, annual back to 1999) --
uk_hmrc_tax_receipts
  year INTEGER            -- fiscal year END: 2026 = April 2025 – March 2026 (most recent complete year). Latest: 2026.
  tax_category VARCHAR    -- filter by this: 'income_tax','national_insurance','vat','corporation_tax','fuel_duties','stamp_duties','total'
  measure_label VARCHAR   -- do NOT filter on this; use tax_category instead
  value_gbpm DECIMAL      -- GBP millions (historical outturn, NOT a projection)
  -- EXAMPLE: SELECT year, value_gbpm FROM uk_hmrc_tax_receipts WHERE tax_category='income_tax' ORDER BY year DESC LIMIT 1
  -- NOTE: year=2026 means fiscal 2025-26. This is real collected tax, not a forecast.

-- GOVERNMENT SPENDING BY FUNCTION (PESA 2025, HM Treasury) --
uk_pesa_functional
  year INTEGER            -- ALWAYS filter year <= 2025 for real data. 2026-2029 are forward plans only.
  function_name VARCHAR   -- EXACT: 'Health and Social Care','Education','Defence','Transport','Work and Pensions','Total Managed Expenditure'. Use ILIKE '%health%' if unsure.
  value_gbpm DECIMAL      -- GBP millions
  -- WORKING EXAMPLE (health spending latest outturn — always add year<=2025 to avoid plan years):
  --   SELECT year, function_name, value_gbpm FROM uk_pesa_functional
  --   WHERE function_name='Health and Social Care' AND year<=2025 ORDER BY year DESC LIMIT 1

-- GOVERNMENT SPENDING BY DEPARTMENT (PESA 2025, HM Treasury) --
uk_pesa_departmental
  year INTEGER              -- financial year
  department_name VARCHAR   -- e.g. 'NHS England', 'Ministry of Defence', 'DWP'
  expenditure_type VARCHAR  -- sheet name e.g. 'DEL', 'AME', 'TME'
  value_gbpm DECIMAL        -- GBP millions

-- DWP BENEFIT CLAIMANTS (quarterly) --
uk_dwp_benefits
  year VARCHAR              -- e.g. '2024'
  quarter VARCHAR           -- 'Q1','Q2','Q3','Q4'
  benefit_name VARCHAR      -- EXACT: 'Universal Credit','Personal Independence Payment','State Pension','Housing Benefit'
  claimants INTEGER         -- number of claimants
  annual_cost_gbpm DECIMAL  -- annual cost GBP millions (where available)
  -- EXAMPLE: SELECT year, quarter, claimants FROM uk_dwp_benefits WHERE benefit_name='Universal Credit' ORDER BY year DESC, quarter DESC LIMIT 1

-- GOVERNMENT SPEND OVER £25,000 (monthly, transparency data) --
uk_spend_25k
  period_raw VARCHAR    -- date string from source CSV
  department VARCHAR    -- 'Cabinet Office', 'HMRC', 'DWP', 'Home Office', etc.
  supplier VARCHAR      -- company or individual receiving payment
  amount_gbp DECIMAL    -- transaction amount in GBP
  expense_type VARCHAR  -- category label from dept
  description VARCHAR   -- free text description

-- GOVERNMENT CONTRACTS (Find a Tender, real-time) --
uk_contracts
  ocid VARCHAR         -- Open Contracting ID
  award_date VARCHAR   -- date awarded
  buyer_name VARCHAR   -- government body
  supplier_name VARCHAR
  title VARCHAR        -- contract description
  value_gbp DECIMAL    -- contract value GBP

meta_datasets -- list of all loaded datasets with row counts
meta_findings -- published nstate findings
"""


def _call(model: str, messages: list, temperature: float = 0.1) -> str:
    resp = httpx.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://nstate.org",
            "X-Title": "nstate",
        },
        json={
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1024,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def _intent(question: str, country: str) -> dict:
    """Classify question and identify relevant tables."""
    content = _call(
        HAIKU,
        [
            {
                "role": "system",
                "content": (
                    "You are a data routing assistant for nstate, a government transparency platform. "
                    "Given a question about UK government data, return JSON with keys: "
                    '"answerable" (bool), "tables" (list of table names from the schema), '
                    '"reason" (one sentence). '
                    "Only set answerable=true if the data is likely in the schema. "
                    "Return raw JSON only, no markdown."
                ),
            },
            {
                "role": "user",
                "content": f"Schema:\n{SCHEMA_SUMMARY}\n\nQuestion: {question}",
            },
        ],
    )
    try:
        cleaned = re.sub(r"```(?:json)?\s*", "", content).strip().rstrip("`").strip()
        return json.loads(cleaned)
    except Exception:
        return {"answerable": False, "tables": [], "reason": content}


_SQL_VALUE_MAP = [
    # uk_ons_wages sector (title-case → hyphenated-lowercase)
    ("'Private sector'", "'private-sector'"),
    ("'Public sector'", "'public-sector'"),
    ("'Private Sector'", "'private-sector'"),
    ("'Public Sector'", "'public-sector'"),
    # uk_ons_wages measure (old name → new name)
    ("'gross-weekly-pay'", "'weekly-pay-gross'"),
    ("'gross-hourly-pay'", "'hourly-pay-gross'"),
    ("'weekly-pay-excl-overtime'", "'weekly-pay-excluding-overtime'"),
    ("'hourly-pay-excl-overtime'", "'hourly-pay-excluding-overtime'"),
    # uk_ons_wages sex
    ("sex = 'All'", "sex = 'all'"),
    ("sex = 'Male'", "sex = 'male'"),
    ("sex = 'Female'", "sex = 'female'"),
    # uk_ons_wages working_pattern
    ("'Full-Time'", "'full-time'"),
    ("'Part-Time'", "'part-time'"),
    ("'Full-time'", "'full-time'"),
    ("'Part-time'", "'part-time'"),
    # uk_ons_wages percentile — 'mean' doesn't exist; 'median' is closest
    ("percentile = 'mean'", "percentile = 'median'"),
    ("percentile = 'Mean'", "percentile = 'median'"),
    # uk_ons_house_prices measure
    ("'mean-price'", "'mean'"),
    ("'median-price'", "'median'"),
    # uk_ons_house_prices month_label
    ("month_label = 'September'", "month_label = 'sep'"),
    ("month_label = 'March'", "month_label = 'mar'"),
    ("month_label = 'June'", "month_label = 'jun'"),
    ("month_label = 'December'", "month_label = 'dec'"),
]


def _normalise_sql_values(sql: str) -> str:
    for wrong, right in _SQL_VALUE_MAP:
        sql = sql.replace(wrong, right)
    return sql


def _generate_sql(question: str, tables: list) -> str:
    """Generate a safe read-only SQL query."""
    table_list = ", ".join(tables) if tables else "uk_civil_service_headcount"
    content = _call(
        SONNET,
        [
            {
                "role": "system",
                "content": (
                    "You are a SQL expert for DuckDB. Generate a single SELECT query to answer the question. "
                    "Rules: SELECT only (no INSERT/UPDATE/DELETE/DROP). Return max 50 rows. Use LIMIT. "
                    "CRITICAL: Use ONLY the exact string values shown in the schema — copy them character-for-character. "
                    "Column values are hyphenated-lowercase (e.g. 'private-sector', 'weekly-pay-gross', 'full-time'). "
                    "Never capitalise or reformat column values. "
                    "Return raw SQL only, no markdown fences, no explanation."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Schema:\n{SCHEMA_SUMMARY}\n\n"
                    f"Focus on tables: {table_list}\n\n"
                    f"Question: {question}"
                ),
            },
        ],
    )
    # Strip markdown fences if model adds them anyway
    sql = re.sub(r"```sql\s*", "", content)
    sql = re.sub(r"```\s*", "", sql).strip()
    sql = _normalise_sql_values(sql)
    # Hard block any mutating statements
    if re.search(r"\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b", sql, re.I):
        raise ValueError("Mutating SQL blocked")
    return sql


def _run_sql(sql: str) -> tuple[list[dict], list[str]]:
    """Execute SQL, return (rows, columns)."""
    with duckdb.connect(DB_PATH, read_only=True) as db:
        cur = db.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, row)) for row in cur.fetchmany(50)]
    return rows, cols


def _narrative(question: str, rows: list[dict], cols: list[str]) -> str:
    """Write a plain-English answer. Numbers injected from rows — LLM must not invent any."""
    data_str = json.dumps(rows[:10], default=str, indent=2)
    content = _call(
        HAIKU,
        [
            {
                "role": "system",
                "content": (
                    "You are a journalist writing for nstate, a UK government transparency platform. "
                    "Write 2-3 sentences answering the question using ONLY the numbers in the data. "
                    "Do not invent any numbers. Be direct and factual. No fluff.\n"
                    "IMPORTANT conventions:\n"
                    "- HMRC year integers are fiscal year END: year=2026 means April 2025–March 2026. "
                    "  This is real collected tax revenue, NOT a projection or forecast.\n"
                    "- House price data is latest available (2022). Acknowledge this if asked about recent years.\n"
                    "- If data is present in the rows, answer the question — do not say 'I cannot answer'.\n"
                    "- Cite source as 'HMRC' for tax data, 'ONS' for economic/wage/price data, "
                    "'Cabinet Office' for civil service, 'DWP' for benefits, 'HM Treasury' for spending."
                ),
            },
            {"role": "user", "content": f"Question: {question}\n\nData:\n{data_str}"},
        ],
        temperature=0.3,
    )
    return content


def _chart_spec(question: str, rows: list[dict], cols: list[str]) -> dict | None:
    """Return a minimal Vega-Lite spec, or None if not chartable."""
    if not rows or len(rows) < 2:
        return None
    # Detect time series: has a date/period column + numeric column
    date_col = next((c for c in cols if c in ("period", "date", "year")), None)
    num_cols = [
        c for c in cols if c not in (date_col, "department", "source_id", "country")
    ]
    if not date_col or not num_cols:
        return None
    y_col = num_cols[0]
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "mark": "line",
        "encoding": {
            "x": {"field": date_col, "type": "temporal", "title": "Year"},
            "y": {
                "field": y_col,
                "type": "quantitative",
                "title": y_col.replace("_", " ").title(),
            },
        },
        "data": {
            "values": [
                {k: str(v) if hasattr(v, "isoformat") else v for k, v in r.items()}
                for r in rows
            ]
        },
    }


def _key_stat(rows: list[dict], cols: list[str]) -> tuple:
    """Return (value, unit) for the first numeric column in the first row."""
    for col in cols:
        v = rows[0].get(col)
        if isinstance(v, (int, float)) and v is not None:
            return v, col.replace("_", " ")
    return None, None


def _gap(question: str, reason: str) -> dict:
    return {"status": "gap", "question": question, "reason": reason}


def answer(question: str, country: str = "uk") -> dict:
    """Full query pipeline. Returns a result dict."""
    logger.info(f"Agent answering: {question}")

    intent = _intent(question, country)
    logger.info(f"Intent: {intent}")

    if not intent.get("answerable"):
        return _gap(question, intent.get("reason", "Data not available"))

    sql = _generate_sql(question, intent.get("tables", []))
    logger.info(f"SQL: {sql}")

    rows, cols = _run_sql(sql)
    if not rows:
        return _gap(question, "Query returned no rows — data may not be loaded yet.")

    key_val, key_unit = _key_stat(rows, cols)

    return {
        "status": "ok",
        "id": str(uuid.uuid4()),
        "question": question,
        "country": country,
        "narrative": _narrative(question, rows, cols),
        "key_stat_value": key_val,
        "key_stat_unit": key_unit,
        "chart_spec": _chart_spec(question, rows, cols),
        "sql": sql,
        "rows": rows,
        "columns": cols,
        "source": "Cabinet Office / OBR · OGL v3",
        "created_at": datetime.utcnow().isoformat(),
    }
