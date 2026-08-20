"""
Background anomaly detector — runs as a systemd timer (daily).

For each numeric column in each uk_* table, computes:
  - rolling mean and standard deviation over all available rows
  - flags the latest value if |z-score| > THRESHOLD
  - writes flagged anomalies as automated_finding rows in meta_findings
"""

import duckdb
import json
import logging
import os
import statistics
import uuid
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("anomaly_detector")

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")
THRESHOLD = 2.0  # z-score threshold
MIN_ROWS = 5  # need at least this many values to compute meaningful stats


def get_uk_tables(db) -> list[str]:
    cur = db.execute("SHOW TABLES")
    return [r[0] for r in cur.fetchall() if r[0].startswith("uk_")]


def get_numeric_columns(db, table: str) -> list[str]:
    cur = db.execute(f"DESCRIBE {table}")
    return [
        r[0]
        for r in cur.fetchall()
        if r[1].upper()
        in ("BIGINT", "INTEGER", "DOUBLE", "FLOAT", "HUGEINT", "DECIMAL")
    ]


def detect_anomalies(db, table: str, col: str) -> list[dict]:
    """Return anomaly dicts for the latest row if z-score > THRESHOLD."""
    cur = db.execute(
        f"SELECT {col} FROM {table} WHERE {col} IS NOT NULL ORDER BY rowid"
    )
    values = [r[0] for r in cur.fetchall()]
    if len(values) < MIN_ROWS:
        return []

    mean = statistics.mean(values)
    try:
        stdev = statistics.stdev(values)
    except statistics.StatisticsError:
        return []
    if stdev == 0:
        return []

    latest = values[-1]
    z = (latest - mean) / stdev
    if abs(z) < THRESHOLD:
        return []

    direction = "above" if z > 0 else "below"
    headline = (
        f"{table}.{col} is {abs(z):.1f}σ {direction} historical average "
        f"(latest: {latest:,.1f}, mean: {mean:,.1f})"
    )
    return [
        {
            "id": str(uuid.uuid4()),
            "country": "uk",
            "question": f"Is {col.replace('_', ' ')} in {table.replace('_', ' ')} anomalous?",
            "headline": headline[:200],
            "explanation": (
                f"The latest value of {col} in {table} is {latest:,.2f}, "
                f"which is {abs(z):.2f} standard deviations {direction} the "
                f"historical mean of {mean:,.2f} (σ={stdev:,.2f}, n={len(values)})."
            ),
            "key_stat_value": round(latest, 2),
            "key_stat_unit": col.replace("_", " "),
            "chart_spec": None,
            "sql_query": f"SELECT {col} FROM {table} ORDER BY rowid",
            "status": "automated_finding",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    ]


def run():
    logger.info("Anomaly detector starting")
    with duckdb.connect(DB_PATH, read_only=False) as db:
        tables = get_uk_tables(db)
        logger.info("Tables to scan: %s", tables)

        findings = []
        for table in tables:
            cols = get_numeric_columns(db, table)
            for col in cols:
                try:
                    anomalies = detect_anomalies(db, table, col)
                    findings.extend(anomalies)
                except Exception as e:
                    logger.warning("Error scanning %s.%s: %s", table, col, e)

        logger.info("Found %d anomalies", len(findings))

        for f in findings:
            try:
                db.execute(
                    """INSERT INTO meta_findings
                       (id, country, question, headline, explanation,
                        key_stat_value, key_stat_unit, status, sql_query, chart_spec, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    [
                        f["id"],
                        f["country"],
                        f["question"],
                        f["headline"],
                        f["explanation"],
                        f["key_stat_value"],
                        f["key_stat_unit"],
                        f["status"],
                        f["sql_query"],
                        json.dumps(f["chart_spec"]) if f["chart_spec"] else None,
                        f["created_at"],
                    ],
                )
                logger.info("Inserted finding: %s", f["headline"])
            except Exception as e:
                logger.warning("Failed to insert finding: %s", e)

    logger.info("Anomaly detector complete")


if __name__ == "__main__":
    run()
