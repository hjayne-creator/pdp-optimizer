"""Local persistence for API keys and optimization reports."""

from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

DATA_DIR = Path(__file__).resolve().parent / "data"
KEYS_PATH = DATA_DIR / "api_keys.json"
REPORTS_DIR = DATA_DIR / "reports"

KEY_FIELDS = ("openai", "anthropic", "google")


def _ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_api_keys() -> dict[str, str]:
    _ensure_dirs()
    if not KEYS_PATH.exists():
        return {k: "" for k in KEY_FIELDS}
    try:
        raw = json.loads(KEYS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {k: "" for k in KEY_FIELDS}
    return {k: str(raw.get(k, "") or "") for k in KEY_FIELDS}


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


def save_report(
    *,
    subject_url: str,
    provider: str,
    model: str,
    result_text: str,
    style_guide_note: str = "",
    usage: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _ensure_dirs()
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
    path = REPORTS_DIR / f"{report_id}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def list_reports() -> list[dict[str, Any]]:
    _ensure_dirs()
    reports: list[dict[str, Any]] = []
    for path in REPORTS_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        usage = data.get("usage") or {}
        reports.append(
            {
                "id": data.get("id", path.stem),
                "created_at": data.get("created_at", ""),
                "subject_url": data.get("subject_url", ""),
                "provider": data.get("provider", ""),
                "model": data.get("model", ""),
                "title": data.get("title", path.stem),
                "style_guide_note": data.get("style_guide_note", ""),
                "cost_usd": usage.get("cost_usd"),
                "path": str(path),
            }
        )
    reports.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    return reports


def load_report(report_id: str) -> dict[str, Any] | None:
    _ensure_dirs()
    path = REPORTS_DIR / f"{report_id}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def delete_report(report_id: str) -> bool:
    path = REPORTS_DIR / f"{report_id}.json"
    if not path.exists():
        return False
    path.unlink()
    return True
