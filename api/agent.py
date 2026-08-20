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

from schema import SCHEMA_SUMMARY  # noqa: E402


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
                    "Given a question, return JSON with keys: "
                    '"answerable" (bool), "tables" (list of table names from the schema), '
                    '"reason" (one sentence). '
                    "Only set answerable=true if the data is likely in the schema.\n\n"
                    "ROUTING RULES:\n"
                    "- For UK-only questions: use uk_* tables.\n"
                    "- For questions about EU countries (any of AT,BE,BG,CY,CZ,DE,DK,EE,EL,ES,FI,FR,HR,HU,IE,IT,LT,LU,LV,MT,NL,PL,PT,RO,SE,SI,SK): "
                    "  use eu_government_finance, eu_tax_revenue, eu_public_employment, eu_tax_breakdown, eu_labour_tax_wedge, eu_tax_rates, eu_vat_rates, eu_price_levels as relevant.\n"
                    "- For EFTA/EEA countries (Norway, Iceland, Switzerland, Liechtenstein): "
                    "  use eu_tax_rates, eu_vat_rates, eu_labour_tax_wedge for tax data; use wb_fiscal for debt/expenditure.\n"
                    "- For global questions (any non-EU country, e.g. US, Japan, China, India, Brazil, Canada, Australia), "
                    "  OR questions asking 'which country has the highest/lowest...', 'globally', 'across countries', 'world ranking': "
                    "  use wb_fiscal (debt/expenditure/revenue/surplus), wb_price_levels (cost of living vs USA), "
                    "  and/or wb_countries (country names/regions/income groups).\n"
                    "- For G7, G20, OECD, or global rankings: use wb_fiscal and/or wb_price_levels.\n"
                    "- For cross-country comparisons mixing UK with non-EU countries: include uk_hmrc_tax_receipts or uk_pesa_functional AND wb_fiscal.\n"
                    "- EU country codes: PT=Portugal, DE=Germany, FR=France, ES=Spain, IT=Italy, "
                    "  NL=Netherlands, BE=Belgium, AT=Austria, DK=Denmark, SE=Sweden, PL=Poland, EL=Greece.\n"
                    "- Global ISO2 codes: US=USA, GB=UK, JP=Japan, CN=China, IN=India, BR=Brazil, CA=Canada, AU=Australia.\n"
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
                    "You are a journalist writing for nstate, a government transparency platform covering UK, EU, and global data. "
                    "Write 2-3 sentences answering the question using ONLY the numbers in the data. "
                    "Do not invent any numbers. Be direct and factual. No fluff.\n"
                    "IMPORTANT conventions:\n"
                    "- HMRC year integers are fiscal year END: year=2026 means April 2025–March 2026. "
                    "  This is real collected tax revenue, NOT a projection or forecast.\n"
                    "- House price data is latest available (2022). Acknowledge this if asked about recent years.\n"
                    "- World Bank fiscal data (wb_fiscal) is CENTRAL government, not general government — "
                    "  figures are typically lower than EU Maastricht/Eurostat general government figures.\n"
                    "- wb_price_levels uses USA=100 base; eu_price_levels uses EU27=100 — note the base when citing.\n"
                    "- If data is present in the rows, answer the question — do not say 'I cannot answer'.\n"
                    "- Cite source as 'HMRC' for tax data, 'ONS' for economic/wage/price data, "
                    "'Cabinet Office' for civil service, 'DWP' for benefits, 'HM Treasury' for spending, "
                    "'Eurostat' for EU/EFTA data, 'World Bank WDI' for global data."
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

    NON_DATA = {"department", "source_id", "indicator", "loaded_at"}
    has_country = "country" in cols
    has_year = "year" in cols

    # Cross-country bar chart: country column present, no year (or same year)
    if has_country and not has_year:
        num_cols = [
            c
            for c in cols
            if c not in NON_DATA | {"country"}
            and isinstance(rows[0].get(c), (int, float))
        ]
        if num_cols:
            y_col = num_cols[0]
            return {
                "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
                "mark": "bar",
                "encoding": {
                    "x": {
                        "field": "country",
                        "type": "nominal",
                        "sort": "-y",
                        "title": "Country",
                    },
                    "y": {
                        "field": y_col,
                        "type": "quantitative",
                        "title": y_col.replace("_", " ").title(),
                    },
                },
                "data": {"values": rows},
            }

    # Multi-country time series: both country and year present
    if has_country and has_year:
        num_cols = [
            c
            for c in cols
            if c not in NON_DATA | {"country", "year"}
            and isinstance(rows[0].get(c), (int, float))
        ]
        if num_cols:
            y_col = num_cols[0]
            return {
                "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
                "mark": "line",
                "encoding": {
                    "x": {"field": "year", "type": "quantitative", "title": "Year"},
                    "y": {
                        "field": y_col,
                        "type": "quantitative",
                        "title": y_col.replace("_", " ").title(),
                    },
                    "color": {"field": "country", "type": "nominal"},
                },
                "data": {"values": rows},
            }

    # Single-country time series
    date_col = next((c for c in cols if c in ("period", "date", "year")), None)
    num_cols = [
        c
        for c in cols
        if c not in NON_DATA | {date_col, "department", "source_id", "country"}
        and c is not None
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


def _source_attribution(tables: list) -> str:
    sources = []
    if any(t.startswith("uk_") for t in tables):
        sources.append("ONS / HMRC / Cabinet Office · OGL v3")
    if any(t.startswith("eu_") for t in tables):
        sources.append("Eurostat · Eurostat reuse policy")
    if any(t.startswith("wb_") for t in tables):
        sources.append("World Bank WDI · CC BY 4.0")
    return " | ".join(sources) if sources else "nstate"


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
        "source": _source_attribution(intent.get("tables", [])),
        "created_at": datetime.utcnow().isoformat(),
    }
