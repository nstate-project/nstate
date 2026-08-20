"""
UK Government Spend Over £25,000 — transparency data
Source: data.gov.uk CKAN API → GOV.UK asset CSVs
Licence: OGL v3
Updates: monthly
"""

import duckdb
import httpx
import csv
import io
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")
CKAN_SEARCH = "https://www.data.gov.uk/api/3/action/package_search"

# Search queries → department label
DEPT_QUERIES = {
    "Cabinet Office": "cabinet office spending over 25000",
    "HMRC": "hmrc spending over 25000",
    "DWP": "dwp spending over 25000",
    "Home Office": "home office spending over 25000",
    "HM Treasury": "hm treasury spending over 25000",
    "NHS England": "nhs england spending over 25000",
    "MoD": "mod spending over 25000",
}
ROWS_PER_DEPT = 4


def _ckan_csv_urls(query: str) -> list[str]:
    """Query data.gov.uk CKAN and return CSV resource URLs, newest first."""
    params = {"q": query, "rows": ROWS_PER_DEPT, "sort": "metadata_modified desc"}
    try:
        r = httpx.get(CKAN_SEARCH, params=params, timeout=20, follow_redirects=True)
        r.raise_for_status()
        packages = r.json().get("result", {}).get("results", [])
    except Exception as e:
        print(f"    CKAN search failed: {e}")
        return []
    urls = []
    for pkg in packages:
        for res in pkg.get("resources", []):
            fmt = (res.get("format") or "").upper()
            url = res.get("url", "")
            if fmt == "CSV" and url.endswith(".csv"):
                urls.append(url)
    return urls


def _parse_amount(val: str):
    if not val:
        return None
    val = val.replace("£", "").replace(",", "").strip()
    try:
        return float(val)
    except ValueError:
        return None


def _insert_rows(db, rows, dept_name, csv_url, source_id) -> int:
    loaded = 0
    for row in rows:
        keys = {k.lower().strip(): v for k, v in row.items()}
        amount = _parse_amount(
            keys.get("amount")
            or keys.get("amount (£)")
            or keys.get("amount(£)")
            or keys.get("net amount")
            or ""
        )
        if amount is None or amount < 25000:
            continue
        period_raw = (
            keys.get("date") or keys.get("payment date") or keys.get("month") or ""
        )[:10]
        supplier = (
            keys.get("supplier")
            or keys.get("supplier name")
            or keys.get("vendor name")
            or ""
        )[:300]
        expense_type = (
            keys.get("expense type") or keys.get("type") or keys.get("category") or ""
        )[:200]
        description = (
            keys.get("description")
            or keys.get("expense area")
            or keys.get("project code")
            or ""
        )[:500]
        try:
            db.execute(
                """
                INSERT INTO uk_spend_25k
                (period_raw, department, supplier, amount_gbp,
                 expense_type, description, source_url, source_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                [
                    period_raw,
                    dept_name,
                    supplier,
                    amount,
                    expense_type,
                    description,
                    csv_url,
                    source_id,
                ],
            )
            loaded += 1
        except Exception:
            pass
    return loaded


def _load_csv(db, dept_name: str, csv_url: str) -> int:
    try:
        r = httpx.get(csv_url, timeout=60, follow_redirects=True)
        r.raise_for_status()
        content = r.content.decode(r.apparent_encoding or "utf-8", errors="replace")
        rows = list(csv.DictReader(io.StringIO(content)))
        if not rows:
            return 0
        source_id = (
            f"spend25k_{dept_name[:10].replace(' ', '_')}_"
            f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        )
        db.execute(
            """
            INSERT OR REPLACE INTO meta_sources
            (id, country, institution, dataset_name, release_url, licence, loaded_at)
            VALUES (?, 'uk', ?, 'Spend Over £25,000', ?, 'OGL v3', ?)
        """,
            [source_id, dept_name, csv_url, datetime.utcnow().isoformat()],
        )
        return _insert_rows(db, rows, dept_name, csv_url, source_id)
    except Exception as e:
        print(f"    ✗ {csv_url[-60:]}: {e}")
        return 0


def run():
    print(f"[{datetime.utcnow().isoformat()}] Running Spend Over £25k pipeline...")
    with duckdb.connect(DB_PATH) as db:
        total = 0
        for dept_name, query in DEPT_QUERIES.items():
            print(f"\n  [{dept_name}]")
            csv_urls = _ckan_csv_urls(query)
            print(f"  Found {len(csv_urls)} CSV(s) via CKAN")
            for url in csv_urls:
                n = _load_csv(db, dept_name, url)
                print(f"    ✓ {n:,} rows from {url[-50:]}")
                total += n

        db.execute(
            """
            UPDATE meta_datasets SET last_loaded = ?, row_count = ?
            WHERE id = 'uk_spend_25k'
        """,
            [datetime.utcnow().isoformat(), total],
        )
    print(f"\n  ✓ Total: {total:,} rows into uk_spend_25k")


if __name__ == "__main__":
    run()
