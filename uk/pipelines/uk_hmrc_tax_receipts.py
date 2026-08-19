"""
HMRC Tax Receipts pipeline — Receipts_Annually sheet
Source: HMRC Statistics — NS_Table.ods
Licence: OGL v3
Covers: 47 tax categories back to 2006-07, GBP millions
Requires: odfpy
"""

import duckdb
import httpx
import os
import re
import tempfile
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")
ODS_URL = "https://assets.publishing.service.gov.uk/media/6a571e539e63154454413697/NS_Table.ods"

CATEGORY_MAP = {
    "Total HMRC Receipts": "total",
    "Total Paid Over": "total_paid_over",
    "Income Tax": "income_tax",
    "National Insurance Contributions": "national_insurance",
    "Value Added Tax": "vat",
    "Corporation Tax": "corporation_tax",
    "Hydrocarbon Oil (Fuel duties)": "fuel_duties",
    "Stamp Duty Land Tax": "stamp_duties",
    "Stamp Duty Shares": "stamp_duties",
    "Capital Gains Tax": "capital_gains_tax",
    "Inheritance Tax": "inheritance_tax",
    "Tobacco Duties": "tobacco_duties",
    "Beer Duties": "alcohol_duties",
    "Spirits Duties": "alcohol_duties",
    "Wines Duties": "alcohol_duties",
    "Cider Duties": "alcohol_duties",
    "Air Passenger Duty": "air_passenger_duty",
    "Insurance Premium Tax": "insurance_premium_tax",
    "Apprenticeship Levy": "apprenticeship_levy",
    "Digital Services Tax": "digital_services_tax",
}


def cell_val(c):
    from odf.text import P

    try:
        ps = c.getElementsByType(P)
        if not ps:
            return ""
        node = ps[0].firstChild
        return str(node).strip() if node else ""
    except Exception:
        return ""


def parse_year(label: str):
    """'2006 to 2007' → 2007 (fiscal year end)."""
    m = re.findall(r"\d{4}", label)
    return int(m[-1]) if m else None


def _parse_sheet(target) -> list:
    """Return list of (year, measure_label, tax_category, amount) from Receipts_Annually."""
    from odf.table import TableRow, TableCell

    rows = target.getElementsByType(TableRow)
    header_cells = rows[5].getElementsByType(TableCell)
    headers = [cell_val(c) for c in header_cells]
    print(f"  {len(headers)} columns. e.g. {headers[2:5]}")

    records = []
    for row in rows[6:]:
        cells = row.getElementsByType(TableCell)
        vals = [cell_val(c) for c in cells]
        if not vals or not vals[0]:
            continue
        year = parse_year(vals[0])
        if year is None:
            continue
        for col_idx, measure_label in enumerate(headers[1:], start=1):
            if not measure_label or col_idx >= len(vals):
                continue
            raw = vals[col_idx].replace(",", "").replace("£", "").strip()
            if not raw or raw in ("[X]", "-", "..", "n/a", "N/A"):
                continue
            try:
                amount = float(raw)
            except ValueError:
                continue
            records.append(
                (
                    year,
                    measure_label[:200],
                    CATEGORY_MAP.get(measure_label, "other"),
                    amount,
                )
            )
    return records


def _write_to_db(records: list, source_id: str) -> int:
    """Insert records into DuckDB, return count loaded."""
    with duckdb.connect(DB_PATH) as db:
        db.execute(
            """
            INSERT OR REPLACE INTO meta_sources
            (id, country, institution, dataset_name, release_url, licence, loaded_at)
            VALUES (?, 'uk', 'HMRC', 'Tax and NIC Receipts',
                    'https://www.gov.uk/government/statistics/hmrc-tax-and-nics-receipts-for-the-uk',
                    'OGL v3', ?)
        """,
            [source_id, datetime.utcnow().isoformat()],
        )
        db.execute("DELETE FROM uk_hmrc_tax_receipts WHERE source_id = ?", [source_id])
        loaded = 0
        for year, measure_label, tax_category, amount in records:
            try:
                db.execute(
                    """
                    INSERT INTO uk_hmrc_tax_receipts
                    (year, tax_category, measure_label, value_gbpm, source_id)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    [year, tax_category, measure_label, amount, source_id],
                )
                loaded += 1
            except Exception:
                pass
        db.execute(
            """
            UPDATE meta_datasets SET last_loaded = ?, row_count = ?
            WHERE id = 'uk_hmrc_tax_receipts'
        """,
            [datetime.utcnow().isoformat(), loaded],
        )
    return loaded


def run():
    print(f"[{datetime.utcnow().isoformat()}] Running HMRC Tax Receipts pipeline...")

    try:
        from odf.opendocument import load
        from odf.table import Table
    except ImportError:
        print("  ERROR: odfpy not installed. Run: pip install odfpy")
        return

    print("  Downloading ODS from HMRC...")
    r = httpx.get(ODS_URL, timeout=120, follow_redirects=True)
    r.raise_for_status()

    with tempfile.NamedTemporaryFile(suffix=".ods", delete=False) as f:
        f.write(r.content)
        tmp_path = f.name

    doc = load(tmp_path)
    sheets = doc.spreadsheet.getElementsByType(Table)
    sheet_names = [s.getAttribute("name") for s in sheets]
    print(f"  Sheets: {sheet_names}")

    target = next(
        (s for s in sheets if s.getAttribute("name") == "Receipts_Annually"), None
    )
    if target is None:
        print(f"  ERROR: Receipts_Annually not found. Got: {sheet_names}")
        os.unlink(tmp_path)
        return

    records = _parse_sheet(target)
    source_id = f"hmrc_tax_receipts_{datetime.utcnow().strftime('%Y%m')}"
    loaded = _write_to_db(records, source_id)
    os.unlink(tmp_path)
    print(f"  ✓ Loaded {loaded:,} rows into uk_hmrc_tax_receipts")


if __name__ == "__main__":
    run()
