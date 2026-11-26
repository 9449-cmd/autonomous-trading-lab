# CSV-to-report CLI

`atl-backtest` reads a local OHLCV/funding CSV, runs the deterministic moving-average backtest, and writes JSON and Markdown summaries. It has no network or exchange access.

Install the project, then run the bundled sample:

```bash
python -m pip install -e .
atl-backtest data/sample_candles.csv --output artifacts --fast-window 2 --slow-window 3
```

This creates `artifacts/backtest-report.json` and `artifacts/backtest-report.md`. The input format and timestamp requirements are documented in [CSV_DATA.md](CSV_DATA.md).

Available fixed parameters:

- `--fast-window` and `--slow-window` (must satisfy `1 <= fast < slow`)
- `--initial-equity`
- `--max-leverage`
- `--fee-rate` and `--slippage-rate`
- `--output`

Defaults are 5/20 windows, 10,000 initial equity, 1x leverage, 0.0004 fee rate, and 0.0002 slippage. Invalid CSV data, configuration values, and window combinations exit with an argparse error. Run `pytest` to check CLI behavior and parameter forwarding.

Reports are research artifacts, not forecasts or trading advice. The engine is a simplified simulation and does not model execution, liquidation, or all market risks.
