"""
UK Public Sector Finances pipeline — ONS PSF release
Source: ONS monthly PSF bulletin (pusf.csv)
Licence: OGL v3
Extracts: 9 headline fiscal indicators as a tidy time series
"""

import csv
import io
import os
from datetime import datetime, date

import duckdb
import httpx

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")
CSV_URL = (
    "https://www.ons.gov.uk/file?uri="
    "/economy/governmentpublicsectorandtaxes/publicsectorfinance"
    "/datasets/publicsectorfinances/current/pusf.csv"
)

KEY_SERIES = {
    "DZLS": ("PS Net Borrowing excl. banks", "£m"),
    "KSE6": ("PS Net Debt excl. banks", "£m"),
    "HF6X": ("PS Net Debt excl. banks", "% GDP"),
    "J5IJ": ("PS Net Borrowing excl. banks", "% GDP"),
    "ANBT": ("PS Total current receipts", "£m"),
    "EBFT": ("PS Total managed expenditure", "£m"),
    "JW2T": ("PS Current Budget Deficit excl. banks", "£m"),
    "JW2V": ("PS Current Budget Deficit excl. banks", "% GDP"),
    "NNBK": ("General Government Net Lending/Borrowing", "£m"),
}

MONTH_MAP = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}


def _parse_period(label: str):
    parts = label.strip().split()
    if len(parts) == 2 and parts[1] in MONTH_MAP:
        return date(int(parts[0]), MONTH_MAP[parts[1]], 1), True
    if len(parts) == 2 and parts[1].startswith("Q"):
        q = int(parts[1][1])
        return date(int(parts[0]), (q - 1) * 3 + 1, 1), False
    try:
        return date(int(parts[0]), 1, 1), False
    except (ValueError, IndexError):
        return None, False


def _download_rows() -> list:
    r = httpx.get(CSV_URL, timeout=60, follow_redirects=True)
    r.raise_for_status()
    rows = list(csv.reader(io.StringIO(r.text)))
    if len(rows) < 8:
        raise ValueError(f"PSF CSV too short: {len(rows)} rows")
    print(f"  Downloaded {len(r.text):,} chars, {len(rows)} rows")
    return rows


def _parse_records(rows: list) -> list:
    code_idx = {c: i for i, c in enumerate(rows[1])}
    missing = [c for c in KEY_SERIES if c not in code_idx]
    if missing:
        print(f"  Warning: series not found: {missing}")
    wanted = {c: code_idx[c] for c in KEY_SERIES if c in code_idx}

    records = []
    for row in rows[7:]:
        period_label = row[0].strip()
        if not period_label:
            continue
        period_date, is_monthly = _parse_period(period_label)
        if period_date is None:
            continue
        for code, col_idx in wanted.items():
            raw = (row[col_idx] if col_idx < len(row) else "").strip()
            if not raw:
                continue
            try:
                value = float(raw.replace(",", ""))
            except ValueError:
                continue
            name, unit = KEY_SERIES[code]
            records.append(
                (period_label, period_date, is_monthly, code, name, value, unit)
            )
    return records


def _write_to_db(records: list, source_id: str) -> None:
    with duckdb.connect(DB_PATH) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS uk_psf_indicators (
                period_label VARCHAR NOT NULL,
                period_date  DATE NOT NULL,
                is_monthly   BOOLEAN,
                series_code  VARCHAR NOT NULL,
                series_name  VARCHAR,
                value        DECIMAL(18,4),
                unit         VARCHAR,
                source_id    VARCHAR,
                _loaded_at   TIMESTAMP DEFAULT current_timestamp,
                PRIMARY KEY (period_label, series_code)
            )
            """
        )
        db.execute("DELETE FROM uk_psf_indicators")
        rows_with_source = [r + (source_id,) for r in records]
        db.executemany(
            """
            INSERT OR REPLACE INTO uk_psf_indicators
            (period_label, period_date, is_monthly, series_code, series_name, value, unit, source_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows_with_source,
        )
        db.execute(
            """
            INSERT OR REPLACE INTO meta_sources
            (id, country, institution, dataset_name, release_url, licence, loaded_at)
            VALUES (?, 'uk', 'ONS', 'Public Sector Finances', ?, 'OGL v3', ?)
            """,
            [source_id, CSV_URL, datetime.utcnow().isoformat()],
        )
        db.execute(
            "UPDATE meta_datasets SET last_loaded = ?, row_count = ? WHERE id = 'uk_psf'",
            [datetime.utcnow().isoformat(), len(records)],
        )


def run():
    print(f"[{datetime.utcnow().isoformat()}] Running PSF pipeline...")
    rows = _download_rows()
    records = _parse_records(rows)
    print(f"  Parsed {len(records):,} data points")
    _write_to_db(records, f"ons_psf_{datetime.utcnow().strftime('%Y%m%d')}")
    print(f"  ✓ Loaded {len(records):,} rows into uk_psf_indicators")


if __name__ == "__main__":
    run()
