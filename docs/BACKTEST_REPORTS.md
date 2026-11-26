## Backtest reports

Completed backtests can be summarized as stable JSON and human-readable Markdown files. The report includes the strategy windows, input candle range/count, configuration and risk limits, performance metrics, and any stop reason.

```python
from autonomous_trading_lab.engine import BacktestConfig, run_backtest
from autonomous_trading_lab.data import load_candles_csv
from autonomous_trading_lab.reporting import build_backtest_report, write_backtest_report

config = BacktestConfig()
candles = load_candles_csv("data/sample.csv")
result = run_backtest(candles, fast_window=5, slow_window=20, config=config)
report = build_backtest_report(
    result, candles, config=config, fast_window=5, slow_window=20
)
json_path, markdown_path = write_backtest_report(report, "artifacts")
```

The JSON output is deterministic for the same inputs and does not include generation-time metadata. Reports are for research and simulation only; they do not model all execution risks or predict future performance.
