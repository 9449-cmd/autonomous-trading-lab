import json
from datetime import datetime, timezone

from autonomous_trading_lab.engine import BacktestConfig, BacktestResult, Candle
from autonomous_trading_lab.reporting import (
    build_backtest_report,
    render_markdown_report,
    write_backtest_report,
)


def test_backtest_report_contains_inputs_metrics_and_writes_files(tmp_path):
    candles = [
        Candle(datetime(2026, 1, 1, tzinfo=timezone.utc), 10, 11, 9, 10),
        Candle(datetime(2026, 1, 2, tzinfo=timezone.utc), 10, 12, 10, 11),
    ]
    config = BacktestConfig(initial_equity=500.0)
    result = BacktestResult(500.0, 510.0, 2.0, 1.0, 3, (), None)

    report = build_backtest_report(result, candles, config=config, fast_window=2, slow_window=5)
    json_path, markdown_path = write_backtest_report(report, tmp_path / "reports")

    saved = json.loads(json_path.read_text(encoding="utf-8"))
    assert saved["data"]["candle_count"] == 2
    assert saved["results"]["total_return_pct"] == 2.0
    assert "Total return: 2.0000%" in markdown_path.read_text(encoding="utf-8")
    assert "research and simulation only" in render_markdown_report(report)


def test_report_rejects_invalid_strategy_windows():
    result = BacktestResult(100.0, 100.0, 0.0, 0.0, 0, ())
    try:
        build_backtest_report(result, [], config=BacktestConfig(), fast_window=5, slow_window=5)
    except ValueError as exc:
        assert "fast_window" in str(exc)
    else:
        raise AssertionError("Expected invalid strategy window error")
