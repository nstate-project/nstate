from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from datetime import datetime, timezone
from collections import defaultdict, deque
import csv
import duckdb
import io
import json
import os
import logging
import time
from agent import answer as agent_answer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nstate")

# In-memory rate limiter: 30 queries/hour per IP
RATE_LIMIT = 30
RATE_WINDOW = 3600  # seconds
_query_log: dict[str, deque] = defaultdict(deque)

GAP_NOTIFY_THRESHOLD = 10  # log admin alert when gap hits this many votes

app = FastAPI(title="nstate API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nstate.org", "http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

DB_PATH = os.getenv("DB_PATH", "/opt/nstate/data/nstate.duckdb")


def get_db():
    return duckdb.connect(DB_PATH, read_only=False)


def rows_to_dicts(cursor) -> list[dict]:
    """Convert DuckDB result to list of dicts without pandas."""
    cols = [d[0] for d in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]


class QueryRequest(BaseModel):
    question: str
    country: str = "uk"


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.get("/datasets")
def list_datasets(country: str = "uk"):
    """List available datasets for a country."""
    with get_db() as db:
        cur = db.execute(
            "SELECT * FROM meta_datasets WHERE country = ? ORDER BY priority", [country]
        )
        return {"country": country, "datasets": rows_to_dicts(cur)}


@app.get("/gaps")
def get_gaps(country: str = "uk", limit: int = 20):
    """Return top data gaps by vote count."""
    with get_db() as db:
        cur = db.execute(
            """SELECT topic, question_example, votes, created_at
               FROM meta_gaps
               WHERE country = ?
               ORDER BY votes DESC
               LIMIT ?""",
            [country, limit],
        )
        return {"gaps": rows_to_dicts(cur)}


@app.post("/gaps/vote")
def vote_gap(topic: str, country: str = "uk"):
    """Vote to prioritise a data gap."""
    with get_db() as db:
        db.execute(
            "UPDATE meta_gaps SET votes = votes + 1 WHERE topic = ? AND country = ?",
            [topic, country],
        )
    return {"ok": True}


@app.get("/findings")
def get_findings(country: str = "uk", status: str = None, limit: int = 20):
    """Return published findings."""
    with get_db() as db:
        where = "WHERE country = ?"
        params = [country]
        if status:
            where += " AND status = ?"
            params.append(status)
        cur = db.execute(
            f"""SELECT id, headline, key_stat_value, key_stat_unit,
                       status, created_at, question
                FROM meta_findings
                {where}
                ORDER BY created_at DESC
                LIMIT ?""",
            params + [limit],
        )
        return {"findings": rows_to_dicts(cur)}


@app.get("/findings/recent")
def get_findings_recent(country: str = "uk", limit: int = 10):
    """Return most recent query findings (alias for /findings)."""
    return get_findings(country=country, limit=limit)


@app.get("/findings/{finding_id}")
def get_finding(finding_id: str):
    """Return a single finding by ID, normalised to match /query response shape."""
    with get_db() as db:
        cur = db.execute("SELECT * FROM meta_findings WHERE id = ?", [finding_id])
        rows = rows_to_dicts(cur)
        if not rows:
            raise HTTPException(status_code=404, detail="Finding not found")
        row = rows[0]
        chart = row.get("chart_spec")
        if isinstance(chart, str):
            try:
                chart = json.loads(chart)
            except Exception:
                chart = None
        return {
            **row,
            "status": "ok",
            "narrative": row.get("explanation") or row.get("headline", ""),
            "sql": row.get("sql_query"),
            "chart_spec": chart,
        }


ADMIN_KEY = os.getenv("NSTATE_ADMIN_KEY", "nstate-admin-2026")


@app.get("/admin/findings")
def admin_findings(key: str, status: str = "automated_finding", limit: int = 50):
    """Admin: list findings pending review."""
    if key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    with get_db() as db:
        cur = db.execute(
            """SELECT id, country, question, headline, key_stat_value, key_stat_unit,
                      status, created_at
               FROM meta_findings
               WHERE status = ?
               ORDER BY created_at DESC
               LIMIT ?""",
            [status, limit],
        )
        return {"findings": rows_to_dicts(cur)}


@app.patch("/findings/{finding_id}/review")
def review_finding(finding_id: str, action: str, key: str):
    """Approve or reject an automated finding. action: 'approve' | 'reject'."""
    if key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    if action not in ("approve", "reject", "mark_posted"):
        raise HTTPException(
            status_code=400, detail="action must be approve | reject | mark_posted"
        )
    new_status = {
        "approve": "reviewed_finding",
        "reject": "rejected",
        "mark_posted": "posted",
    }.get(action, "rejected")
    with get_db() as db:
        db.execute(
            "UPDATE meta_findings SET status = ? WHERE id = ?",
            [new_status, finding_id],
        )
    return {"ok": True, "id": finding_id, "status": new_status}


@app.get("/findings/{finding_id}/export.csv")
def export_finding_csv(finding_id: str):
    """Download finding data as CSV. Re-executes stored SQL to produce fresh rows."""
    with get_db() as db:
        cur = db.execute(
            "SELECT sql_query, question FROM meta_findings WHERE id = ?", [finding_id]
        )
        rows = rows_to_dicts(cur)
        if not rows:
            raise HTTPException(status_code=404, detail="Finding not found")
        sql = rows[0].get("sql_query")
        question = rows[0].get("question", "")

    output = io.StringIO()
    w = csv.writer(output)
    w.writerow(["# nstate finding", finding_id])
    w.writerow(["# source", f"https://nstate.org/f/{finding_id}"])
    w.writerow(["# question", question])
    w.writerow([])

    if sql:
        with get_db() as db:
            data_cur = db.execute(sql)
            cols = [d[0] for d in data_cur.description]
            w.writerow(cols)
            for row in data_cur.fetchall():
                w.writerow(list(row))
    else:
        w.writerow(["question"])
        w.writerow([question])

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="nstate-{finding_id}.csv"',
            "Access-Control-Allow-Origin": "*",
        },
    )


class FlagRequest(BaseModel):
    flag_type: str
    note: str = ""


@app.post("/findings/{finding_id}/flag")
def flag_finding(finding_id: str, req: FlagRequest):
    """Flag a finding as incorrect, outdated, misleading, or other."""
    if req.flag_type not in ("incorrect", "outdated", "misleading", "other"):
        raise HTTPException(
            status_code=400,
            detail="flag_type must be incorrect|outdated|misleading|other",
        )
    with get_db() as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS meta_finding_flags (
               finding_id VARCHAR NOT NULL,
               flag_type VARCHAR NOT NULL,
               note VARCHAR,
               created_at VARCHAR NOT NULL
            )"""
        )
        db.execute(
            """INSERT INTO meta_finding_flags (finding_id, flag_type, note, created_at)
               VALUES (?, ?, ?, ?)""",
            [
                finding_id,
                req.flag_type,
                req.note[:500],
                datetime.now(timezone.utc).isoformat(),
            ],
        )
    logger.info("Finding flagged: %s as %s", finding_id, req.flag_type)
    return {"ok": True}


def _check_rate_limit(ip: str) -> bool:
    """Return True if the IP is within the rate limit, False if exceeded."""
    now = time.monotonic()
    q = _query_log[ip]
    # Drop timestamps older than the window
    while q and now - q[0] > RATE_WINDOW:
        q.popleft()
    if len(q) >= RATE_LIMIT:
        return False
    q.append(now)
    return True


@app.post("/query")
async def query(req: QueryRequest, request: Request):
    """
    Main query endpoint. Takes a plain-English question,
    returns a cited data result.
    """
    ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(ip):
        return JSONResponse(
            status_code=429,
            content={
                "detail": f"Rate limit exceeded. Max {RATE_LIMIT} queries per hour."
            },
        )

    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question required")

    # Log the query
    logger.info(f"Query [{req.country}]: {question}")

    with get_db() as db:
        # Log to query history
        try:
            db.execute(
                """INSERT INTO meta_queries (question, country, created_at)
                   VALUES (?, ?, ?)""",
                [question, req.country, datetime.now(timezone.utc).isoformat()],
            )
        except Exception:
            pass

        # Check what datasets we have
        cur = db.execute(
            "SELECT name, description FROM meta_datasets WHERE country = ?",
            [req.country],
        )
        datasets = rows_to_dicts(cur)
        has_data = len(datasets) > 0

    if not has_data:
        topic, votes = _log_gap(question, req.country)
        return {
            "status": "gap",
            "question": question,
            "message": "We don't have this data loaded yet.",
            "gap_logged": True,
            "topic": topic,
            "votes": votes,
        }

    # Run the query agent
    try:
        result = agent_answer(question, req.country)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    if result["status"] == "gap":
        topic, votes = _log_gap(question, req.country)
        result["topic"] = topic
        result["votes"] = votes

    # Persist finding if agent returned a result
    if result["status"] == "ok":
        try:
            with get_db() as db:
                db.execute(
                    """INSERT INTO meta_findings
                       (id, country, question, headline, explanation,
                        key_stat_value, key_stat_unit, status, sql_query, chart_spec, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, 'automated_finding', ?, ?, ?)""",
                    [
                        result["id"],
                        req.country,
                        question,
                        result["narrative"][:200],
                        result["narrative"],
                        result.get("key_stat_value"),
                        result.get("key_stat_unit"),
                        result.get("sql"),
                        json.dumps(result["chart_spec"])
                        if result.get("chart_spec")
                        else None,
                        result.get("created_at"),
                    ],
                )
        except Exception as e:
            logger.warning(f"Finding persist failed: {e}")

    return result


COUNTRY_NAMES = {
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
}


@app.get("/country/{code}/stats")
def country_stats(code: str):
    """Return headline stats and time-series for an EU country from Eurostat data."""
    code = code.upper()
    if code not in COUNTRY_NAMES:
        raise HTTPException(status_code=404, detail=f"Country '{code}' not in EU27")
    with get_db() as db:
        # Latest value per indicator
        cur = db.execute(
            """SELECT indicator, value, year FROM eu_government_finance
               WHERE country = ?
               ORDER BY indicator, year DESC""",
            [code],
        )
        rows = rows_to_dicts(cur)
        latest: dict[str, dict] = {}
        for r in rows:
            ind = r["indicator"]
            if ind not in latest:
                latest[ind] = {"value": r["value"], "year": r["year"]}

        # Full debt time series for chart
        cur2 = db.execute(
            """SELECT year, value FROM eu_government_finance
               WHERE country = ? AND indicator = 'debt_pct_gdp'
               ORDER BY year""",
            [code],
        )
        debt_series = rows_to_dicts(cur2)

        # Tax revenue latest
        cur3 = db.execute(
            "SELECT value_pct_gdp, year FROM eu_tax_revenue WHERE country = ? ORDER BY year DESC LIMIT 1",
            [code],
        )
        tax_row = cur3.fetchone()

        # Employment latest
        cur4 = db.execute(
            "SELECT employment_thousands, year FROM eu_public_employment WHERE country = ? ORDER BY year DESC LIMIT 1",
            [code],
        )
        empl_row = cur4.fetchone()

        # EU27 average for comparison (latest matching year)
        latest_year = latest.get("debt_pct_gdp", {}).get("year")
        eu_avg = {}
        if latest_year:
            cur5 = db.execute(
                """SELECT indicator, value FROM eu_government_finance
                   WHERE country = 'EU27_2020' AND year = ?""",
                [latest_year],
            )
            for r in rows_to_dicts(cur5):
                eu_avg[r["indicator"]] = r["value"]

        # Tax breakdown (latest year per indicator)
        cur6 = db.execute(
            """SELECT indicator, value, year FROM eu_tax_breakdown
               WHERE country = ? ORDER BY indicator, year DESC""",
            [code],
        )
        tax_breakdown: dict[str, dict] = {}
        for r in rows_to_dicts(cur6):
            if r["indicator"] not in tax_breakdown:
                tax_breakdown[r["indicator"]] = {"value": r["value"], "year": r["year"]}

        # Labour tax wedge at average wage (latest)
        cur7 = db.execute(
            """SELECT tax_wedge_pct, year FROM eu_labour_tax_wedge
               WHERE country = ? AND income_level = 'AW100'
               ORDER BY year DESC LIMIT 1""",
            [code],
        )
        wedge_row = cur7.fetchone()

        # Statutory tax rates
        cur8 = db.execute(
            "SELECT tax_type, rate FROM eu_tax_rates WHERE country = ? AND year = 2024",
            [code],
        )
        tax_rates = {r["tax_type"]: r["rate"] for r in rows_to_dicts(cur8)}

        # VAT rates
        cur9 = db.execute(
            "SELECT standard_rate, reduced_rate FROM eu_vat_rates WHERE country = ? ORDER BY year DESC LIMIT 1",
            [code],
        )
        vat_row = cur9.fetchone()

    return {
        "country": code,
        "name": COUNTRY_NAMES[code],
        "latest": latest,
        "eu27_avg": eu_avg,
        "eu27_comparison_year": latest_year,
        "debt_series": debt_series,
        "tax_revenue_pct_gdp": tax_row[0] if tax_row else None,
        "tax_revenue_year": tax_row[1] if tax_row else None,
        "public_employment_thousands": empl_row[0] if empl_row else None,
        "public_employment_year": empl_row[1] if empl_row else None,
        "tax_breakdown": tax_breakdown,
        "labour_tax_wedge_pct": wedge_row[0] if wedge_row else None,
        "labour_tax_wedge_year": wedge_row[1] if wedge_row else None,
        "corporate_tax_rate": tax_rates.get("corporate_rate"),
        "personal_top_rate": tax_rates.get("personal_top_rate"),
        "vat_standard_rate": vat_row[0] if vat_row else None,
        "vat_reduced_rate": vat_row[1] if vat_row else None,
    }


@app.get("/country/{code}/prices")
def country_prices(code: str):
    """Return comparative price level indices for an EU country (Eurostat prc_ppp_ind)."""
    code = code.upper()
    if code not in COUNTRY_NAMES:
        raise HTTPException(status_code=404, detail=f"Country '{code}' not in EU27")
    with get_db() as db:
        cur = db.execute(
            """SELECT category, pli, year FROM eu_price_levels
               WHERE country = ?
               ORDER BY category, year DESC""",
            [code],
        )
        rows = rows_to_dicts(cur)
    latest: dict[str, dict] = {}
    for r in rows:
        if r["category"] not in latest:
            latest[r["category"]] = {"pli": r["pli"], "year": r["year"]}
    return {"country": code, "name": COUNTRY_NAMES[code], "price_levels": latest}


def _log_gap(question: str, country: str) -> tuple[str, int]:
    """Log a data gap, notify admin when threshold crossed. Returns (topic, votes)."""
    topic = question[:100]
    try:
        with get_db() as db:
            db.execute(
                """INSERT INTO meta_gaps (topic, question_example, country, votes, created_at)
                   VALUES (?, ?, ?, 1, ?)
                   ON CONFLICT (topic, country) DO UPDATE SET votes = votes + 1""",
                [topic, question, country, datetime.now(timezone.utc).isoformat()],
            )
            cur = db.execute(
                "SELECT votes FROM meta_gaps WHERE topic = ? AND country = ?",
                [topic, country],
            )
            row = cur.fetchone()
            votes = row[0] if row else 1
            if votes >= GAP_NOTIFY_THRESHOLD:
                logger.warning(
                    "ADMIN_ALERT gap_threshold_reached topic=%r country=%s votes=%d",
                    topic,
                    country,
                    votes,
                )
            return topic, votes
    except Exception as e:
        logger.warning(f"Gap log failed: {e}")
        return topic, 1
