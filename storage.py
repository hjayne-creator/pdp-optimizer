"""Persistence for API keys and optimization reports.

Reports use Neon Postgres when a connection URL is configured
(Streamlit secrets / env). Otherwise they fall back to local JSON files.
"""

from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

DATA_DIR = Path(__file__).resolve().parent / "data"
KEYS_PATH = DATA_DIR / "api_keys.json"
REPORTS_DIR = DATA_DIR / "reports"

KEY_FIELDS = ("openai", "anthropic", "google", "deepseek")

# Env var names checked in order for each provider.
ENV_KEY_MAP: dict[str, tuple[str, ...]] = {
    "openai": ("OPENAI_API_KEY",),
    "anthropic": ("ANTHROPIC_API_KEY",),
    "google": ("GOOGLE_API_KEY", "GOOGLE_AI_API_KEY", "GEMINI_API_KEY"),
    "deepseek": ("DEEPSEEK_API_KEY",),
}

_SCHEMA_READY = False

_CREATE_REPORTS_SQL = """
CREATE TABLE IF NOT EXISTS reports (
  id TEXT PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL,
  subject_url TEXT NOT NULL,
  provider TEXT,
  model TEXT,
  style_guide_note TEXT,
  title TEXT,
  result_text TEXT NOT NULL,
  usage JSONB NOT NULL DEFAULT '{}'::jsonb
);
"""


def _ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _from_env(field: str) -> str:
    for name in ENV_KEY_MAP.get(field, ()):
        value = (os.environ.get(name) or "").strip()
        if value:
            return value
    return ""


def _from_secrets(field: str) -> str:
    """Read from Streamlit secrets when available (e.g. Streamlit Community Cloud)."""
    try:
        import streamlit as st

        secrets = st.secrets
    except Exception:
        return ""

    for name in ENV_KEY_MAP.get(field, ()):
        try:
            value = str(secrets.get(name, "") or "").strip()
        except Exception:
            value = ""
        if value:
            return value

    try:
        nested = secrets.get("api_keys", {})
        value = str(nested.get(field, "") or "").strip()
        if value:
            return value
    except Exception:
        pass

    try:
        value = str(secrets.get(field, "") or "").strip()
        if value:
            return value
    except Exception:
        pass

    return ""


def _from_file() -> dict[str, str]:
    if not KEYS_PATH.exists():
        return {k: "" for k in KEY_FIELDS}
    try:
        raw = json.loads(KEYS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {k: "" for k in KEY_FIELDS}
    return {k: str(raw.get(k, "") or "") for k in KEY_FIELDS}


def load_api_keys() -> dict[str, str]:
    """Load keys with precedence: local file → env vars → Streamlit secrets."""
    _ensure_dirs()
    file_keys = _from_file()
    return {
        k: (file_keys.get(k) or _from_env(k) or _from_secrets(k) or "")
        for k in KEY_FIELDS
    }


def save_api_keys(keys: dict[str, str]) -> None:
    _ensure_dirs()
    payload = {k: (keys.get(k) or "").strip() for k in KEY_FIELDS}
    KEYS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _slug_from_url(url: str) -> str:
    host = urlparse(url).netloc or "report"
    path = urlparse(url).path.strip("/").replace("/", "-")
    base = f"{host}-{path}" if path else host
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", base).strip("-").lower()
    return (slug or "report")[:60]


def _database_url() -> str:
    for name in ("DATABASE_URL", "NEON_DATABASE_URL"):
        value = (os.environ.get(name) or "").strip()
        if value:
            return value

    try:
        import streamlit as st

        secrets = st.secrets
    except Exception:
        return ""

    try:
        nested = secrets.get("connections", {}).get("neon", {})
        value = str(nested.get("url", "") or "").strip()
        if value:
            return value
    except Exception:
        pass

    for name in ("DATABASE_URL", "NEON_DATABASE_URL"):
        try:
            value = str(secrets.get(name, "") or "").strip()
        except Exception:
            value = ""
        if value:
            return value

    return ""


def _use_neon() -> bool:
    return bool(_database_url())


def _connect():
    import psycopg2

    return psycopg2.connect(_database_url())


def _ensure_schema() -> None:
    global _SCHEMA_READY
    if _SCHEMA_READY:
        return
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(_CREATE_REPORTS_SQL)
        conn.commit()
    _SCHEMA_READY = True


def _created_at_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()
    return str(value)


def _usage_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


def _list_item_from_row(row: dict[str, Any]) -> dict[str, Any]:
    usage = _usage_dict(row.get("usage"))
    return {
        "id": row.get("id", ""),
        "created_at": _created_at_str(row.get("created_at")),
        "subject_url": row.get("subject_url", ""),
        "provider": row.get("provider", ""),
        "model": row.get("model", ""),
        "title": row.get("title", ""),
        "style_guide_note": row.get("style_guide_note", ""),
        "cost_usd": usage.get("cost_usd"),
    }


def _save_report_neon(report: dict[str, Any]) -> None:
    from psycopg2.extras import Json

    _ensure_schema()
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO reports (
                  id, created_at, subject_url, provider, model,
                  style_guide_note, title, result_text, usage
                ) VALUES (
                  %(id)s, %(created_at)s, %(subject_url)s, %(provider)s, %(model)s,
                  %(style_guide_note)s, %(title)s, %(result_text)s, %(usage)s
                )
                """,
                {
                    **report,
                    "usage": Json(report.get("usage") or {}),
                },
            )
        conn.commit()


def _list_reports_neon() -> list[dict[str, Any]]:
    _ensure_schema()
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, created_at, subject_url, provider, model,
                       title, style_guide_note, usage
                FROM reports
                ORDER BY created_at DESC
                """
            )
            cols = [d[0] for d in cur.description]
            rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    return [_list_item_from_row(row) for row in rows]


def _load_report_neon(report_id: str) -> dict[str, Any] | None:
    _ensure_schema()
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, created_at, subject_url, provider, model,
                       style_guide_note, title, result_text, usage
                FROM reports
                WHERE id = %s
                """,
                (report_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
    data = dict(zip(cols, row))
    return {
        "id": data.get("id", ""),
        "created_at": _created_at_str(data.get("created_at")),
        "subject_url": data.get("subject_url", ""),
        "provider": data.get("provider", ""),
        "model": data.get("model", ""),
        "style_guide_note": data.get("style_guide_note", ""),
        "title": data.get("title", ""),
        "result_text": data.get("result_text", ""),
        "usage": _usage_dict(data.get("usage")),
    }


def _delete_report_neon(report_id: str) -> bool:
    _ensure_schema()
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM reports WHERE id = %s", (report_id,))
            deleted = cur.rowcount > 0
        conn.commit()
    return deleted


def _save_report_local(report: dict[str, Any]) -> None:
    _ensure_dirs()
    path = REPORTS_DIR / f"{report['id']}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def _list_reports_local() -> list[dict[str, Any]]:
    _ensure_dirs()
    reports: list[dict[str, Any]] = []
    for path in REPORTS_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        item = _list_item_from_row(data)
        item["path"] = str(path)
        if not item["id"]:
            item["id"] = path.stem
        if not item["title"]:
            item["title"] = path.stem
        reports.append(item)
    reports.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    return reports


def _load_report_local(report_id: str) -> dict[str, Any] | None:
    _ensure_dirs()
    path = REPORTS_DIR / f"{report_id}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _delete_report_local(report_id: str) -> bool:
    path = REPORTS_DIR / f"{report_id}.json"
    if not path.exists():
        return False
    path.unlink()
    return True


def save_report(
    *,
    subject_url: str,
    provider: str,
    model: str,
    result_text: str,
    style_guide_note: str = "",
    usage: dict[str, Any] | None = None,
) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    report_id = f"{now.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
    report = {
        "id": report_id,
        "created_at": now.isoformat(),
        "subject_url": subject_url,
        "provider": provider,
        "model": model,
        "style_guide_note": style_guide_note,
        "title": _slug_from_url(subject_url),
        "result_text": result_text,
        "usage": usage or {},
    }
    if _use_neon():
        _save_report_neon(report)
    else:
        _save_report_local(report)
    return report


def list_reports() -> list[dict[str, Any]]:
    if _use_neon():
        return _list_reports_neon()
    return _list_reports_local()


def load_report(report_id: str) -> dict[str, Any] | None:
    if _use_neon():
        return _load_report_neon(report_id)
    return _load_report_local(report_id)


def delete_report(report_id: str) -> bool:
    if _use_neon():
        return _delete_report_neon(report_id)
    return _delete_report_local(report_id)
