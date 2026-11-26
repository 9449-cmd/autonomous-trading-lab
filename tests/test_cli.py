from __future__ import annotations

import json
from pathlib import Path

import pytest

from autonomous_trading_lab.cli import main


def test_cli_runs_csv_backtest_with_fixed_arguments(tmp_path: Path, capsys):
    csv_path = tmp_path / "candles.csv"
    csv_path.write_text(
        "timestamp,open,high,low,close,volume,funding_rate\n"
        "2026-01-01T00:00:00Z,100,100,100,100,1,0\n"
        "2026-01-01T01:00:00Z,101,101,101,101,1,0\n"
        "2026-01-01T02:00:00Z,102,102,102,102,1,0\n"
        "2026-01-01T03:00:00Z,103,103,103,103,1,0\n"
        "2026-01-01T04:00:00Z,104,104,104,104,1,0\n",
        encoding="utf-8",
    )
    output_dir = tmp_path / "reports"

    assert main([
        str(csv_path),
        "--output", str(output_dir),
        "--fast-window", "2",
        "--slow-window", "3",
        "--initial-equity", "2500",
        "--max-leverage", "0.5",
        "--fee-rate", "0.001",
        "--slippage-rate", "0.002",
    ]) == 0

    report = json.loads((output_dir / "backtest-report.json").read_text(encoding="utf-8"))
    assert report["strategy"] == {
        "name": "moving_average_baseline",
        "fast_window": 2,
        "slow_window": 3,
    }
    assert report["config"]["initial_equity"] == 2500.0
    assert report["config"]["max_leverage"] == 0.5
    assert report["config"]["fee_rate"] == 0.001
    assert report["config"]["slippage_rate"] == 0.002
    assert report["data"]["candle_count"] == 5
    assert (output_dir / "backtest-report.md").is_file()
    assert "JSON report:" in capsys.readouterr().out


def test_cli_rejects_invalid_window_arguments(tmp_path: Path):
    csv_path = tmp_path / "unused.csv"
    with pytest.raises(SystemExit) as exc:
        main([str(csv_path), "--fast-window", "3", "--slow-window", "3"])
    assert exc.value.code == 2
