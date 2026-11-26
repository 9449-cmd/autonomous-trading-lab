"""Deterministic JSON and Markdown summaries for completed backtests."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable

from .engine import BacktestConfig, BacktestResult, Candle


def build_backtest_report(
    result: BacktestResult,
    candles: Iterable[Candle],
    *,
    config: BacktestConfig,
    fast_window: int,
    slow_window: int,
) -> dict[str, Any]:
    """Build a JSON-compatible report from a result and its input data."""
    bars = tuple(candles)
    if fast_window < 1 or slow_window <= fast_window:
        raise ValueError("Require 1 <= fast_window < slow_window")
    if any(bars[i].timestamp >= bars[i + 1].timestamp for i in range(len(bars) - 1)):
        raise ValueError("Candle timestamps must be strictly increasing")

    return {
        "schema_version": 1,
        "strategy": {"name": "moving_average_baseline", "fast_window": fast_window, "slow_window": slow_window},
        "data": {
            "candle_count": len(bars),
            "start": bars[0].timestamp.isoformat() if bars else None,
            "end": bars[-1].timestamp.isoformat() if bars else None,
        },
        "config": {
            "initial_equity": config.initial_equity,
            "max_leverage": config.max_leverage,
            "fee_rate": config.fee_rate,
            "slippage_rate": config.slippage_rate,
            "risk_limits": asdict(config.risk_limits),
        },
        "results": {
            "initial_equity": result.initial_equity,
            "final_equity": result.final_equity,
            "total_return_pct": result.total_return_pct,
            "max_drawdown_pct": result.max_drawdown_pct,
            "trades": result.trades,
            "stopped_reason": result.stopped_reason,
        },
    }


def render_markdown_report(report: dict[str, Any]) -> str:
    """Render a compact human-readable report from ``build_backtest_report``."""
    strategy = report["strategy"]
    data = report["data"]
    config = report["config"]
    results = report["results"]
    stopped_reason = results["stopped_reason"] or "none"
    return "\n".join(
        [
            "# Backtest report",
            "",
            f"- Strategy: {strategy['name']} (fast={strategy['fast_window']}, slow={strategy['slow_window']})",
            f"- Candles: {data['candle_count']}",
            f"- Period: {data['start'] or 'n/a'} to {data['end'] or 'n/a'}",
            f"- Initial equity: {results['initial_equity']:.2f}",
            f"- Final equity: {results['final_equity']:.2f}",
            f"- Total return: {results['total_return_pct']:.4f}%",
            f"- Maximum drawdown: {results['max_drawdown_pct']:.4f}%",
            f"- Trades: {results['trades']}",
            f"- Stop reason: {stopped_reason}",
            f"- Max leverage: {config['max_leverage']}",
            f"- Fee rate: {config['fee_rate']}",
            f"- Slippage rate: {config['slippage_rate']}",
            "",
            "> Research and simulation only; historical results do not predict future performance.",
            "",
        ]
    )


def write_backtest_report(report: dict[str, Any], directory: str | Path) -> tuple[Path, Path]:
    """Write stable JSON and Markdown report files and return their paths."""
    output_dir = Path(directory)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "backtest-report.json"
    markdown_path = output_dir / "backtest-report.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown_report(report), encoding="utf-8")
    return json_path, markdown_path
