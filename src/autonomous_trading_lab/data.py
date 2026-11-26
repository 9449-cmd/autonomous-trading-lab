"""Import and validate local CSV candle data; no network or exchange access."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from .engine import Candle

_REQUIRED_COLUMNS = {"timestamp", "open", "high", "low", "close"}
_OPTIONAL_COLUMNS = {"volume", "funding_rate"}


def load_candles_csv(path: str | Path) -> list[Candle]:
    """Load candles from a local CSV file.

    Required columns are ``timestamp,open,high,low,close``. Optional columns
    ``volume`` and ``funding_rate`` default to zero. Timestamps must be ISO 8601;
    timezone-naive timestamps are rejected so callers cannot accidentally mix
    local time with UTC market data. Rows must be chronologically increasing.
    """
    source = Path(path)
    with source.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        headers = reader.fieldnames
        if headers is None:
            raise ValueError("CSV is empty or missing a header row")
        if len(headers) != len(set(headers)):
            raise ValueError("CSV contains duplicate column names")
        missing = _REQUIRED_COLUMNS - set(headers)
        if missing:
            raise ValueError(f"CSV missing required columns: {', '.join(sorted(missing))}")

        candles: list[Candle] = []
        for row_number, row in enumerate(reader, start=2):
            if None in row:
                raise ValueError(f"CSV row {row_number} has more fields than the header")
            if not any(value and value.strip() for value in row.values() if value is not None):
                continue
            try:
                timestamp = datetime.fromisoformat(row["timestamp"].strip().replace("Z", "+00:00"))
                if timestamp.tzinfo is None or timestamp.utcoffset() is None:
                    raise ValueError("timestamp must include a timezone")
                candle = Candle(
                    timestamp=timestamp,
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"]) if "volume" in row and row["volume"].strip() else 0.0,
                    funding_rate=(
                        float(row["funding_rate"])
                        if "funding_rate" in row and row["funding_rate"].strip()
                        else 0.0
                    ),
                )
            except (TypeError, ValueError, KeyError) as exc:
                raise ValueError(f"Invalid CSV row {row_number}: {exc}") from exc
            if candles and candle.timestamp <= candles[-1].timestamp:
                raise ValueError(f"CSV row {row_number}: timestamps must be strictly increasing")
            candles.append(candle)
    return candles
