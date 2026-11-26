# Autonomous Trading Lab

Private research platform for leveraged cryptocurrency perpetual-futures strategies.

> **Research and simulation only.** This project has no exchange connectivity, live order API, credential handling, or deployment automation. Nothing here is financial advice.

## Current MVP

- Typed OHLCV/funding candles and deterministic moving-average signal baseline.
- Close-to-close backtest; a signal observed at a candle close is used for the next interval.
- Fee, slippage, signed funding-rate assumptions and equity curve.
- Daily-loss and peak-to-trough drawdown stop limits.
- Fail-closed simulated pre-trade risk checks.
- Local CSV import and deterministic JSON/Markdown backtest reports.
- `atl-backtest` CLI to run a CSV backtest and write both reports.

The engine is intentionally small and educational. It does not model order books, latency, partial fills, liquidation mechanics, exchange-specific funding schedules, or survivorship/data-quality issues.

## Setup

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -e .
python -m pip install -r requirements-dev.txt
pytest
```

## Quick CLI run

```bash
atl-backtest data/sample_candles.csv --output artifacts --fast-window 2 --slow-window 3
```

The command writes `artifacts/backtest-report.json` and `artifacts/backtest-report.md`. See [docs/CLI.md](docs/CLI.md) for all parameters and [docs/CSV_DATA.md](docs/CSV_DATA.md) for the input format.

## Python example

```python
from datetime import datetime, timedelta, timezone
from autonomous_trading_lab import BacktestConfig, Candle, run_backtest

start = datetime(2026, 1, 1, tzinfo=timezone.utc)
prices = [100, 99, 101, 102, 98, 97, 100, 103]
bars = [
    Candle(start + timedelta(hours=i), p, p, p, p, volume=1.0)
    for i, p in enumerate(prices)
]
result = run_backtest(bars, fast_window=2, slow_window=3, config=BacktestConfig())
print(result.final_equity, result.total_return_pct, result.max_drawdown_pct)
```

Funding rates are decimal rates per candle: positive values represent longs paying shorts. The model applies funding to the signed exposure once per candle; supply data at the intended funding interval.

## Safety boundaries

- Never add real exchange secrets to this repository or local `.env` files committed to Git.
- The package deliberately contains no exchange client or order-submission code.
- Simulated risk checks are not a guarantee of capital preservation.
