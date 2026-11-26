"""JSONL audit records for reproducible simulated runs."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any


def _json_default(value: Any) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    raise TypeError(f"Cannot JSON-encode {type(value).__name__}")


def write_jsonl(path: str | Path, record: dict[str, Any]) -> None:
    """Append one JSON object as a line; create parent directories safely."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("a", encoding="utf-8") as output:
        output.write(json.dumps(record, sort_keys=True, default=_json_default) + "\n")


def dataclass_record(result: Any) -> dict[str, Any]:
    """Convert a dataclass result to an audit-friendly JSON-compatible mapping."""
    if not is_dataclass(result):
        raise TypeError("result must be a dataclass")
    return asdict(result)
