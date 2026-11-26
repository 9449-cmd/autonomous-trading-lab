"""Command-line entry point for local CSV backtests."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .data import load_candles_csv
from .engine import BacktestConfig, run_backtest
from .reporting import build_backtest_report, write_backtest_report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atl-backtest",
        description="Run a research-only backtest on a local candle CSV and write JSON/Markdown reports.",
    )
    parser.add_argument("csv", type=Path, help="input CSV with timestamp,open,high,low,close columns")
    parser.add_argument("--output", type=Path, default=Path("artifacts"), help="report output directory (default: artifacts)")
    parser.add_argument("--fast-window", type=int, default=5, help="fast SMA window (default: 5)")
    parser.add_argument("--slow-window", type=int, default=20, help="slow SMA window (default: 20)")
    parser.add_argument("--initial-equity", type=float, default=10_000.0, help="starting simulated equity")
    parser.add_argument("--max-leverage", type=float, default=1.0, help="maximum simulated exposure multiple")
    parser.add_argument("--fee-rate", type=float, default=0.0004, help="fee rate per unit turnover")
    parser.add_argument("--slippage-rate", type=float, default=0.0002, help="slippage rate per unit turnover")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI; return zero on success and let argparse report bad input."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.fast_window < 1 or args.slow_window <= args.fast_window:
        parser.error("Require 1 <= --fast-window < --slow-window")

    try:
        candles = load_candles_csv(args.csv)
        config = BacktestConfig(
            initial_equity=args.initial_equity,
            max_leverage=args.max_leverage,
            fee_rate=args.fee_rate,
            slippage_rate=args.slippage_rate,
        )
        result = run_backtest(
            candles,
            fast_window=args.fast_window,
            slow_window=args.slow_window,
            config=config,
        )
        report = build_backtest_report(
            result,
            candles,
            config=config,
            fast_window=args.fast_window,
            slow_window=args.slow_window,
        )
        json_path, markdown_path = write_backtest_report(report, args.output)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(f"JSON report: {json_path}")
    print(f"Markdown report: {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
