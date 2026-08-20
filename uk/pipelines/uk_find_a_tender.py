"""
UK Government Contracts pipeline — Contracts Finder (OCDS)
Source: contractsfinder.service.gov.uk
Licence: OGL v3
Fetches: last 500 contract award notices
"""

import duckdb
import httpx
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")
BASE_URL = "https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search"


def _fetch_page(offset: int, client: httpx.Client) -> list:
    params = {
        "limit": 100,
        "start": offset,
        "order": "dt_published desc",
        "stages": "award",
    }
    try:
        r = client.get(BASE_URL, params=params, timeout=30)
        r.raise_for_status()
        return r.json().get("releases", [])
    except Exception as e:
        print(f"  Warning offset {offset}: {e}")
        return []


def _extract_awards(rel: dict, source_id: str) -> list:
    ocid = rel.get("ocid", "")
    date_str = (rel.get("date") or "")[:10]
    buyer_name = rel.get("buyer", {}).get("name", "")
    tender_title = rel.get("tender", {}).get("title", "")
    rows = []
    for award in rel.get("awards", []):
        val = award.get("value") or {}
        suppliers = award.get("suppliers") or []
        rows.append(
            (
                ocid,
                date_str,
                buyer_name,
                suppliers[0].get("name", "") if suppliers else "",
                (award.get("title") or tender_title)[:500],
                val.get("amount"),
                val.get("currency", "GBP"),
                source_id,
            )
        )
    return rows


def run():
    print(f"[{datetime.utcnow().isoformat()}] Running Contracts Finder pipeline...")
    source_id = f"contracts_finder_{datetime.utcnow().strftime('%Y%m%d')}"

    all_releases = []
    with httpx.Client(headers={"Accept": "application/json"}) as client:
        for offset in range(0, 500, 100):
            page = _fetch_page(offset, client)
            all_releases.extend(page)
            print(f"  offset {offset}: {len(page)} releases")
            if len(page) < 100:
                break

    print(f"  Total releases: {len(all_releases)}")

    with duckdb.connect(DB_PATH) as db:
        db.execute(
            """
            INSERT OR REPLACE INTO meta_sources
            (id, country, institution, dataset_name, release_url, licence, loaded_at)
            VALUES (?, 'uk', 'Cabinet Office', 'Contracts Finder',
                    'https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search',
                    'OGL v3', ?)
        """,
            [source_id, datetime.utcnow().isoformat()],
        )

        db.execute("DELETE FROM uk_contracts WHERE source_id = ?", [source_id])
        all_rows = [
            list(row) for rel in all_releases for row in _extract_awards(rel, source_id)
        ]
        if all_rows:
            db.executemany(
                """
                INSERT INTO uk_contracts
                (ocid, award_date, buyer_name, supplier_name,
                 title, value_gbp, currency, source_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                all_rows,
            )
        loaded = len(all_rows)

        db.execute(
            """
            UPDATE meta_datasets SET last_loaded = ?, row_count = ?
            WHERE id = 'uk_contracts'
        """,
            [datetime.utcnow().isoformat(), loaded],
        )

    print(f"  ✓ Loaded {loaded:,} contract awards into uk_contracts")


if __name__ == "__main__":
    run()
