"""
UK Government Spend Over £25,000 — transparency data
Source: data.gov.uk / GOV.UK direct CSV links
Licence: OGL v3
Updates: monthly
Departments: Cabinet Office, HMRC, DWP, Home Office, DfE, MoD, NHS, HM Treasury
"""

import duckdb
import httpx
import csv
import io
import os
import re
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")

# Direct CSV URLs — latest available months for key departments
# Pattern: https://assets.publishing.service.gov.uk/media/.../spend-data-YYYY-MM.csv
# These are scraped from each dept's transparency collection page
DEPARTMENT_PAGES = {
    "Cabinet Office": "https://www.gov.uk/government/collections/cabinet-office-spending-over-25-000",
    "HMRC": "https://www.gov.uk/government/collections/hm-revenue-customs-spending-over-25-000",
    "DWP": "https://www.gov.uk/government/collections/dwp-and-agencies-spending-over-25-000",
    "Home Office": "https://www.gov.uk/government/collections/home-office-spending-over-25-000",
    "HM Treasury": "https://www.gov.uk/government/collections/hm-treasury-spending-over-25-000",
    "NHS England": "https://www.gov.uk/government/collections/nhs-england-spending-over-25-000",
    "MoD": "https://www.gov.uk/government/collections/mod-spending-over-25-000",
}


def scrape_csv_urls(dept_name: str, page_url: str, limit: int = 6) -> list[str]:
    """Scrape the latest N CSV download URLs from a department collection page."""
    try:
        r = httpx.get(page_url, timeout=20, follow_redirects=True)
        r.raise_for_status()
        # Find publication links, then get CSV from each
        pub_links = re.findall(
            r'href=["\'](/government/publications/[^"\']+spend[^"\']*)["\']',
            r.text,
            re.I,
        )
        pub_links = list(dict.fromkeys(pub_links))[:limit]  # dedupe, take first N

        csv_urls = []
        for pub in pub_links:
            try:
                r2 = httpx.get(
                    f"https://www.gov.uk{pub}", timeout=15, follow_redirects=True
                )
                found = re.findall(
                    r'href=["\']( https://assets\.publishing[^"\']+\.csv)["\']',
                    r2.text,
                    re.I,
                )
                found += re.findall(
                    r'href=["\'](https://assets\.publishing[^"\']+\.csv)["\']',
                    r2.text,
                    re.I,
                )
                if found:
                    csv_urls.append(found[0].strip())
            except Exception:
                pass
        return csv_urls
    except Exception as e:
        print(f"  Warning: could not scrape {dept_name}: {e}")
        return []


def parse_amount(val: str) -> float | None:
    if not val:
        return None
    val = val.replace("£", "").replace(",", "").strip()
    try:
        return float(val)
    except ValueError:
        return None


def run():
    print(f"[{datetime.utcnow().isoformat()}] Running Spend Over £25k pipeline...")

    with duckdb.connect(DB_PATH) as db:
        loaded_total = 0

        for dept_name, page_url in DEPARTMENT_PAGES.items():
            print(f"\n  [{dept_name}] Scraping CSV URLs...")
            csv_urls = scrape_csv_urls(dept_name, page_url, limit=3)
            print(f"  Found {len(csv_urls)} CSV files")

            for csv_url in csv_urls:
                print(f"    Fetching: {csv_url[-60:]}")
                try:
                    r = httpx.get(csv_url, timeout=60, follow_redirects=True)
                    r.raise_for_status()
                    content = r.text

                    # Try multiple encodings
                    if not content or len(content) < 10:
                        content = r.content.decode("latin-1", errors="replace")

                    rows = list(csv.DictReader(io.StringIO(content)))
                    if not rows:
                        continue

                    source_id = f"spend25k_{dept_name[:10].replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

                    db.execute(
                        """
                        INSERT OR REPLACE INTO meta_sources
                        (id, country, institution, dataset_name, release_url, licence, loaded_at)
                        VALUES (?, 'uk', ?, 'Spend Over £25,000', ?, 'OGL v3', ?)
                    """,
                        [source_id, dept_name, csv_url, datetime.utcnow().isoformat()],
                    )

                    loaded = 0
                    for row in rows:
                        # Normalise column names (they vary by dept)
                        keys = {k.lower().strip(): v for k, v in row.items()}
                        amount = parse_amount(
                            keys.get("amount")
                            or keys.get("amount (£)")
                            or keys.get("amount(£)")
                            or keys.get("net amount")
                            or ""
                        )
                        if amount is None or amount < 25000:
                            continue

                        period_raw = (
                            keys.get("date")
                            or keys.get("payment date")
                            or keys.get("month")
                            or ""
                        )[:10]
                        supplier = (
                            keys.get("supplier")
                            or keys.get("supplier name")
                            or keys.get("vendor name")
                            or ""
                        )[:300]
                        expense_type = (
                            keys.get("expense type")
                            or keys.get("type")
                            or keys.get("category")
                            or ""
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

                    print(f"    ✓ {loaded:,} rows from {dept_name}")
                    loaded_total += loaded

                except Exception as e:
                    print(f"    ✗ Failed: {e}")

        db.execute(
            """
            UPDATE meta_datasets SET last_loaded = ?, row_count = ?
            WHERE id = 'uk_spend_25k'
        """,
            [datetime.utcnow().isoformat(), loaded_total],
        )

    print(f"\n  ✓ Total: {loaded_total:,} rows into uk_spend_25k")


if __name__ == "__main__":
    run()
