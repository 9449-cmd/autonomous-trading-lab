"""Research-only tools for backtesting and simulated trading."""

from .engine import BacktestConfig, BacktestResult, Candle, run_backtest
from .models import Signal
from .reporting import build_backtest_report, render_markdown_report, write_backtest_report
from .risk import RiskDecision, RiskLimits, evaluate_order

__all__ = [
    "BacktestConfig",
    "BacktestResult",
    "Candle",
    "RiskDecision",
    "RiskLimits",
    "Signal",
    "build_backtest_report",
    "evaluate_order",
    "render_markdown_report",
    "run_backtest",
    "write_backtest_report",
]
