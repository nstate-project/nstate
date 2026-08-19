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
  period_label VARCHAR      -- e.g. 'Jan-26'
  aggregate_code VARCHAR    -- ONS category code e.g. 'CP01'
  aggregate_label VARCHAR   -- e.g. '01 Food and non-alcoholic beverages'
  index_value DECIMAL       -- index value (2015=100)

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
  year VARCHAR           -- e.g. '2024'
  month_label VARCHAR    -- e.g. 'September'
  geography_code VARCHAR -- ONS area code e.g. 'E08000028'
  property_type VARCHAR  -- 'All', 'Detached', 'Semi-detached', 'Terraced', 'Flat'
  build_status VARCHAR   -- 'All', 'New build', 'Existing'
  measure VARCHAR        -- 'sales' (count) or 'mean-price', 'median-price'
  value DECIMAL          -- count or GBP price

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
  year VARCHAR           -- e.g. '2024'
  geography_code VARCHAR -- region code
  percentile VARCHAR     -- '10', '25', '50', '75', '90', 'mean'
  sex VARCHAR            -- 'All', 'Male', 'Female'
  working_pattern VARCHAR -- 'Full-Time', 'Part-Time'
  measure VARCHAR        -- 'gross-weekly-pay', 'hourly-pay-excl-overtime' etc.
  sector VARCHAR         -- 'Public sector', 'Private sector'
  value DECIMAL          -- GBP amount

-- HMRC TAX RECEIPTS (HMRC, annual back to 1999) --
uk_hmrc_tax_receipts
  year INTEGER            -- financial year e.g. 2024
  tax_category VARCHAR    -- income_tax|national_insurance|vat|corporation_tax|fuel_duties|stamp_duties|total
  measure_label VARCHAR   -- row label from HMRC table e.g. 'Total Income Tax'
  value_gbpm DECIMAL      -- GBP millions

-- GOVERNMENT SPENDING BY FUNCTION (PESA 2025, HM Treasury) --
uk_pesa_functional
  year INTEGER            -- financial year (2014–2027 inc. plans)
  function_name VARCHAR   -- e.g. 'Health', 'Education', 'Defence', 'Social protection'
  value_gbpm DECIMAL      -- Total Managed Expenditure, GBP millions

-- GOVERNMENT SPENDING BY DEPARTMENT (PESA 2025, HM Treasury) --
uk_pesa_departmental
  year INTEGER              -- financial year
  department_name VARCHAR   -- e.g. 'NHS England', 'Ministry of Defence', 'DWP'
  expenditure_type VARCHAR  -- sheet name e.g. 'DEL', 'AME', 'TME'
  value_gbpm DECIMAL        -- GBP millions

-- DWP BENEFIT CLAIMANTS (quarterly) --
uk_dwp_benefits
  year VARCHAR              -- e.g. '2024'
  quarter VARCHAR           -- 'Q1'–'Q4'
  benefit_name VARCHAR      -- UC|PIP|Housing Benefit|State Pension|ESA
  claimants INTEGER         -- number of claimants
  annual_cost_gbpm DECIMAL  -- annual cost GBP millions (where available)

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
                    "Rules: SELECT only (no INSERT/UPDATE/DELETE/DROP). "
                    "Return max 50 rows. Use LIMIT. "
                    "For totals use 'All departments' in the department column. "
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
                    "Do not invent any numbers. Cite the source as 'Cabinet Office' or 'OBR' as appropriate. "
                    "Be direct and factual. No fluff."
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
