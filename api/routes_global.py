"""Global country routes — World Bank WDI fiscal + price data."""

from fastapi import APIRouter, HTTPException
import duckdb
import os

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")

router = APIRouter()

# EU27 names for fallback when WB country name is unavailable
EU_COUNTRY_NAMES = {
    "AT": "Austria",
    "BE": "Belgium",
    "BG": "Bulgaria",
    "CY": "Cyprus",
    "CZ": "Czechia",
    "DE": "Germany",
    "DK": "Denmark",
    "EE": "Estonia",
    "EL": "Greece",
    "ES": "Spain",
    "FI": "Finland",
    "FR": "France",
    "HR": "Croatia",
    "HU": "Hungary",
    "IE": "Ireland",
    "IT": "Italy",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "MT": "Malta",
    "NL": "Netherlands",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "SE": "Sweden",
    "SI": "Slovenia",
    "SK": "Slovakia",
    "NO": "Norway",
    "IS": "Iceland",
    "CH": "Switzerland",
    "LI": "Liechtenstein",
}


def get_db():
    return duckdb.connect(DB_PATH, read_only=False)


def rows_to_dicts(cursor) -> list[dict]:
    cols = [d[0] for d in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


@router.get("/country/{code}/global-stats")
def country_global_stats(code: str):
    """Fiscal + price data for any country: World Bank WDI + Eurostat where available."""
    code = code.upper()
    with get_db() as db:
        cur = db.execute("SELECT name FROM wb_countries WHERE iso2 = ?", [code])
        name_row = cur.fetchone()
        name = name_row[0] if name_row else EU_COUNTRY_NAMES.get(code, code)

        cur = db.execute(
            "SELECT indicator, value, year FROM wb_fiscal WHERE country = ? ORDER BY indicator, year DESC",
            [code],
        )
        fiscal_raw = rows_to_dicts(cur)
        fiscal: dict[str, dict] = {}
        for r in fiscal_raw:
            if r["indicator"] not in fiscal:
                fiscal[r["indicator"]] = {"value": r["value"], "year": r["year"]}

        cur2 = db.execute(
            "SELECT year, value FROM wb_fiscal WHERE country = ? AND indicator = 'debt_pct_gdp' ORDER BY year",
            [code],
        )
        debt_series = rows_to_dicts(cur2)

        cur3 = db.execute(
            "SELECT pli, year FROM wb_price_levels WHERE country = ? ORDER BY year DESC LIMIT 1",
            [code],
        )
        pli_row = cur3.fetchone()

        cur4 = db.execute(
            "SELECT tax_wedge_pct, year FROM eu_labour_tax_wedge WHERE country = ? AND income_level = 'AW100' ORDER BY year DESC LIMIT 1",
            [code],
        )
        wedge_row = cur4.fetchone()

        cur5 = db.execute(
            "SELECT tax_type, rate FROM eu_tax_rates WHERE country = ? AND year = 2024",
            [code],
        )
        tax_rates = {r["tax_type"]: r["rate"] for r in rows_to_dicts(cur5)}

        cur6 = db.execute(
            "SELECT standard_rate, reduced_rate FROM eu_vat_rates WHERE country = ? ORDER BY year DESC LIMIT 1",
            [code],
        )
        vat_row = cur6.fetchone()

    if not name_row and not fiscal and not pli_row:
        raise HTTPException(
            status_code=404, detail=f"No data found for country '{code}'"
        )

    return {
        "country": code,
        "name": name,
        "fiscal": fiscal,
        "debt_series": debt_series,
        "price_level_pli": pli_row[0] if pli_row else None,
        "price_level_year": pli_row[1] if pli_row else None,
        "price_level_base": "USA=100",
        "labour_tax_wedge_pct": wedge_row[0] if wedge_row else None,
        "labour_tax_wedge_year": wedge_row[1] if wedge_row else None,
        "corporate_tax_rate": tax_rates.get("corporate_rate"),
        "personal_top_rate": tax_rates.get("personal_top_rate"),
        "vat_standard_rate": vat_row[0] if vat_row else None,
        "vat_reduced_rate": vat_row[1] if vat_row else None,
    }


@router.get("/countries/list")
def countries_list():
    """All countries with at least one World Bank fiscal data point."""
    with get_db() as db:
        cur = db.execute(
            """SELECT DISTINCT f.country, c.name, c.region, c.income_group
               FROM wb_fiscal f
               LEFT JOIN wb_countries c ON c.iso2 = f.country
               WHERE c.name IS NOT NULL
               ORDER BY c.name"""
        )
        rows = rows_to_dicts(cur)
    return {"countries": rows}
