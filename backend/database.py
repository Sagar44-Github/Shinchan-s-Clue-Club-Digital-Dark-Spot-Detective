from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path(os.getenv("DATABASE_PATH", str(ROOT / "data" / "kasukabe.db")))
if not DB_PATH.is_absolute():
    DB_PATH = (Path(__file__).resolve().parent / DB_PATH).resolve()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


@contextmanager
def connect():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS cases (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            question TEXT NOT NULL,
            context TEXT NOT NULL DEFAULT '',
            jurisdiction TEXT NOT NULL DEFAULT '',
            decision_date TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'active',
            requirements_json TEXT NOT NULL DEFAULT '[]',
            play_mode TEXT NOT NULL DEFAULT 'custom',
            challenge_json TEXT NOT NULL DEFAULT '{}',
            challenge_attempts INTEGER NOT NULL DEFAULT 0,
            challenge_solved_at TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sources (
            id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            url TEXT NOT NULL DEFAULT '',
            publisher TEXT NOT NULL DEFAULT '',
            published_date TEXT NOT NULL DEFAULT '',
            retrieved_at TEXT NOT NULL,
            source_type TEXT NOT NULL,
            text TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            original_filename TEXT NOT NULL DEFAULT '',
            extraction_note TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS analysis_runs (
            id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
            created_at TEXT NOT NULL,
            method TEXT NOT NULL,
            result_json TEXT NOT NULL,
            source_ids_json TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS verification_tasks (
            id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
            run_id TEXT NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
            finding_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            notes TEXT NOT NULL DEFAULT '',
            evidence_json TEXT NOT NULL DEFAULT '[]',
            sort_order INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_sources_case ON sources(case_id);
        CREATE INDEX IF NOT EXISTS idx_runs_case ON analysis_runs(case_id);
        CREATE INDEX IF NOT EXISTS idx_tasks_case ON verification_tasks(case_id, sort_order);
        """)
        columns = {row[1] for row in db.execute("PRAGMA table_info(cases)").fetchall()}
        migrations = {
            "play_mode": "ALTER TABLE cases ADD COLUMN play_mode TEXT NOT NULL DEFAULT 'custom'",
            "challenge_json": "ALTER TABLE cases ADD COLUMN challenge_json TEXT NOT NULL DEFAULT '{}'",
            "challenge_attempts": "ALTER TABLE cases ADD COLUMN challenge_attempts INTEGER NOT NULL DEFAULT 0",
            "challenge_solved_at": "ALTER TABLE cases ADD COLUMN challenge_solved_at TEXT NOT NULL DEFAULT ''",
        }
        for name, statement in migrations.items():
            if name not in columns:
                db.execute(statement)


def dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def load(value: str, fallback: Any) -> Any:
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return fallback


def create_case(data: dict[str, Any]) -> dict[str, Any]:
    case_id, stamp = uid("case"), now_iso()
    requirements = data.get("requirements") or []
    with connect() as db:
        db.execute("INSERT INTO cases(id,title,question,context,jurisdiction,decision_date,status,requirements_json,play_mode,challenge_json,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (
            case_id, data.get("title") or "Untitled research case", data["question"], data.get("context", ""),
            data.get("jurisdiction", ""), data.get("decision_date", ""), data.get("status", "active"), dump(requirements),
            data.get("play_mode", "custom"), dump(data.get("challenge") or {}), stamp, stamp,
        ))
    return get_case(case_id)


def update_case(case_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
    allowed = {"title", "question", "context", "jurisdiction", "decision_date", "status", "requirements"}
    fields = {k: v for k, v in patch.items() if k in allowed}
    if not fields:
        return get_case(case_id)
    cols, values = [], []
    for key, value in fields.items():
        col = "requirements_json" if key == "requirements" else key
        cols.append(f"{col}=?")
        values.append(dump(value) if key == "requirements" else value)
    cols.append("updated_at=?")
    values.extend([now_iso(), case_id])
    with connect() as db:
        cur = db.execute(f"UPDATE cases SET {', '.join(cols)} WHERE id=?", values)
        if cur.rowcount == 0:
            return None
    return get_case(case_id)


def list_cases() -> list[dict[str, Any]]:
    with connect() as db:
        rows = db.execute("SELECT * FROM cases ORDER BY updated_at DESC").fetchall()
    result = []
    for row in rows:
        case = dict(row)
        case["requirements"] = load(case.pop("requirements_json"), [])
        challenge = load(case.pop("challenge_json", "{}"), {})
        case["challenge"] = public_challenge(challenge, reveal=case.get("status") == "solved")
        with connect() as db:
            case["source_count"] = db.execute("SELECT COUNT(*) FROM sources WHERE case_id=?", (case["id"],)).fetchone()[0]
            run = db.execute("SELECT created_at,method FROM analysis_runs WHERE case_id=? ORDER BY created_at DESC LIMIT 1", (case["id"],)).fetchone()
        case["last_analysis"] = dict(run) if run else None
        result.append(case)
    return result


def get_case(case_id: str) -> dict[str, Any] | None:
    with connect() as db:
        row = db.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
        if not row:
            return None
        case = dict(row)
        case["requirements"] = load(case.pop("requirements_json"), [])
        challenge = load(case.pop("challenge_json", "{}"), {})
        case["challenge"] = public_challenge(challenge, reveal=case.get("status") == "solved")
        case["sources"] = [dict(r) for r in db.execute("SELECT * FROM sources WHERE case_id=? ORDER BY retrieved_at", (case_id,)).fetchall()]
        runs = db.execute("SELECT * FROM analysis_runs WHERE case_id=? ORDER BY created_at DESC", (case_id,)).fetchall()
        case["analysis_runs"] = [{**dict(r), "result": load(r["result_json"], {})} for r in runs]
        tasks = db.execute("SELECT * FROM verification_tasks WHERE case_id=? ORDER BY sort_order,updated_at", (case_id,)).fetchall()
        case["tasks"] = [{**dict(t), "evidence": load(t["evidence_json"], [])} for t in tasks]
    return case


def public_challenge(challenge: dict[str, Any], reveal: bool = False) -> dict[str, Any] | None:
    if not challenge:
        return None
    hidden = {"hints"} if reveal else {"answer_id", "resolution", "hints", "hint"}
    return {key: value for key, value in challenge.items() if key not in hidden}


def answer_challenge(case_id: str, answer_id: str) -> dict[str, Any] | None:
    stamp = now_iso()
    with connect() as db:
        row = db.execute("SELECT play_mode,challenge_json,challenge_attempts,status,challenge_solved_at FROM cases WHERE id=?", (case_id,)).fetchone()
        if not row or row["play_mode"] != "challenge":
            return None
        challenge = load(row["challenge_json"], {})
        if row["status"] == "solved":
            return {"correct": True, "attempts": row["challenge_attempts"], "solved_at": row["challenge_solved_at"], "resolution": challenge.get("resolution", "Case solved.")}
        attempts = row["challenge_attempts"] + 1
        correct = answer_id == challenge.get("answer_id")
        solved_at = stamp if correct else ""
        db.execute("UPDATE cases SET challenge_attempts=?,status=?,challenge_solved_at=?,updated_at=? WHERE id=?", (
            attempts, "solved" if correct else "unsolved", solved_at, stamp, case_id,
        ))
    result = {"correct": correct, "attempts": attempts, "solved_at": solved_at}
    if correct:
        result["resolution"] = challenge.get("resolution", "Case solved.")
    else:
        result["hint"] = challenge.get("hint", "Compare the source dates and look for the latest record that answers the case question.")
    return result


def challenge_hint(case_id: str, level: int) -> dict[str, Any] | None:
    with connect() as db:
        row = db.execute("SELECT play_mode,challenge_json,status FROM cases WHERE id=?", (case_id,)).fetchone()
    if not row or row["play_mode"] != "challenge":
        return None
    if row["status"] == "solved":
        return {"hint": "Case solved. Revisit the cited passages in the case briefing."}
    challenge = load(row["challenge_json"], {})
    hints = challenge.get("hints") or [challenge.get("hint", "Compare the source dates and look for the latest record that answers the case question.")]
    index = min(max(level, 0), len(hints) - 1)
    return {"level": index + 1, "hint": hints[index], "has_more": index < len(hints) - 1}


def add_source(case_id: str, data: dict[str, Any]) -> dict[str, Any]:
    source_id, stamp = uid("src"), now_iso()
    import hashlib
    text = data["text"]
    digest = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
    with connect() as db:
        db.execute("INSERT INTO sources(id,case_id,title,url,publisher,published_date,retrieved_at,source_type,text,content_hash,original_filename,extraction_note) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (
            source_id, case_id, data.get("title") or "Untitled source", data.get("url", ""), data.get("publisher", ""),
            data.get("published_date", ""), stamp, data.get("source_type", "pasted excerpt"), text,
            digest, data.get("original_filename", ""), data.get("extraction_note", ""),
        ))
        db.execute("UPDATE cases SET updated_at=? WHERE id=?", (stamp, case_id))
    return {"id": source_id, "case_id": case_id, "title": data.get("title") or "Untitled source", "url": data.get("url", ""), "publisher": data.get("publisher", ""), "published_date": data.get("published_date", ""), "retrieved_at": stamp, "source_type": data.get("source_type", "pasted excerpt"), "text": text, "content_hash": digest, "original_filename": data.get("original_filename", ""), "extraction_note": data.get("extraction_note", "")}


def delete_source(case_id: str, source_id: str) -> bool:
    with connect() as db:
        cur = db.execute("DELETE FROM sources WHERE case_id=? AND id=?", (case_id, source_id))
        if cur.rowcount:
            db.execute("UPDATE cases SET updated_at=? WHERE id=?", (now_iso(), case_id))
        return cur.rowcount > 0


def delete_case(case_id: str) -> bool:
    with connect() as db:
        cur = db.execute("DELETE FROM cases WHERE id=?", (case_id,))
        return cur.rowcount > 0


def add_analysis(case_id: str, result: dict[str, Any], method: str) -> dict[str, Any]:
    run_id, stamp = uid("run"), now_iso()
    source_ids = result.get("source_ids", [])
    with connect() as db:
        prior_tasks = {row["finding_id"]: dict(row) for row in db.execute("SELECT * FROM verification_tasks WHERE case_id=? ORDER BY updated_at DESC", (case_id,)).fetchall()}
        db.execute("INSERT INTO analysis_runs(id,case_id,created_at,method,result_json,source_ids_json) VALUES(?,?,?,?,?,?)", (run_id, case_id, stamp, method, dump(result), dump(source_ids)))
        db.execute("DELETE FROM verification_tasks WHERE case_id=?", (case_id,))
        for i, finding in enumerate(result.get("findings", [])):
            task = finding.get("task")
            if not task:
                continue
            prior = prior_tasks.get(finding["id"], {})
            db.execute("INSERT INTO verification_tasks(id,case_id,run_id,finding_id,title,description,priority,status,notes,evidence_json,sort_order,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (
                uid("task"), case_id, run_id, finding["id"], task["title"], task["description"], task.get("priority", "normal"), prior.get("status", "open"), prior.get("notes", ""), dump(finding.get("evidence", [])), i, stamp,
            ))
        db.execute("UPDATE cases SET updated_at=? WHERE id=?", (stamp, case_id))
    return {"id": run_id, "case_id": case_id, "created_at": stamp, "method": method, "result": result}


def update_task(task_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
    allowed = {"status", "notes", "title", "description", "priority", "sort_order"}
    fields = {k: v for k, v in patch.items() if k in allowed}
    if not fields:
        return None
    cols, values = [], []
    for key, value in fields.items():
        cols.append(f"{key}=?")
        values.append(value)
    cols.append("updated_at=?")
    values.extend([now_iso(), task_id])
    with connect() as db:
        cur = db.execute(f"UPDATE verification_tasks SET {', '.join(cols)} WHERE id=?", values)
        if not cur.rowcount:
            return None
        row = db.execute("SELECT * FROM verification_tasks WHERE id=?", (task_id,)).fetchone()
        return {**dict(row), "evidence": load(row["evidence_json"], [])}


def get_sources(case_id: str) -> list[dict[str, Any]]:
    with connect() as db:
        return [dict(r) for r in db.execute("SELECT * FROM sources WHERE case_id=? ORDER BY retrieved_at", (case_id,)).fetchall()]
