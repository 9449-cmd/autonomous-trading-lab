"""CLI for local backtest demonstrations.

Usage: python -m autonomous_trading_lab.cli
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone

from .engine import BacktestConfig, Candle, run_backtest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a local, simulated backtest")
    parser.add_argument("--initial-equity", type=float, default=10_000.0)
    parser.add_argument("--max-leverage", type=float, default=1.0)
    parser.add_argument("--fast-window", type=int, default=5)
    parser.add_argument("--slow-window", type=int, default=20)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    prices = (100, 101, 99, 98, 97, 100, 104, 106, 103, 101,
              105, 108, 110, 107, 104, 102, 106, 112, 115, 111,
              109, 113, 117, 114, 118, 121, 119, 116, 120, 124)
    bars = [
        Candle(start + timedelta(hours=i), p, p, p, p, volume=1.0)
        for i, p in enumerate(prices)
    ]
    config = BacktestConfig(initial_equity=args.initial_equity, max_leverage=args.max_leverage)
    result = run_backtest(
        bars,
        fast_window=args.fast_window,
        slow_window=args.slow_window,
        config=config,
    )
    print(json.dumps({
        "initial_equity": result.initial_equity,
        "final_equity": round(result.final_equity, 6),
        "total_return_pct": round(result.total_return_pct, 6),
        "max_drawdown_pct": round(result.max_drawdown_pct, 6),
        "trades": result.trades,
        "stopped_reason": result.stopped_reason,
    }, indent=2))


if __name__ == "__main__":
    main()
