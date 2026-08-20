from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import duckdb
import json
import os
import logging
from agent import answer as agent_answer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nstate")

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
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


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


@app.post("/query")
async def query(req: QueryRequest, request: Request):
    """
    Main query endpoint. Takes a plain-English question,
    returns a cited data result.
    Phase 0: returns structured response showing what we have.
    Phase 1: adds LLM query agent.
    """
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
                [question, req.country, datetime.utcnow().isoformat()],
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
        _log_gap(question, req.country)
        return {
            "status": "gap",
            "question": question,
            "message": "We don't have this data loaded yet.",
            "gap_logged": True,
        }

    # Run the query agent
    try:
        result = agent_answer(question, req.country)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    if result["status"] == "gap":
        _log_gap(question, req.country)

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


def _log_gap(question: str, country: str):
    """Log a data gap from a failed query."""
    try:
        with get_db() as db:
            db.execute(
                """INSERT INTO meta_gaps (topic, question_example, country, votes, created_at)
                   VALUES (?, ?, ?, 1, ?)
                   ON CONFLICT (topic, country) DO UPDATE SET votes = votes + 1""",
                [question[:100], question, country, datetime.utcnow().isoformat()],
            )
    except Exception as e:
        logger.warning(f"Gap log failed: {e}")
