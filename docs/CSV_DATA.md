## Importing local candle CSV files

The data helper reads local CSV files only; it makes no network requests. Required headers are `timestamp,open,high,low,close`. `volume` and `funding_rate` are optional and default to zero.

Timestamps must be ISO 8601 and include an explicit timezone (for example `2026-01-01T00:00:00Z`). Prices must be positive, OHLC ranges must be internally consistent, and timestamps must be strictly increasing.

```python
from autonomous_trading_lab.data import load_candles_csv
from autonomous_trading_lab import run_backtest

candles = load_candles_csv("data/sample.csv")
result = run_backtest(candles)
```

Funding values are decimal rates per candle as described in the README. Check source data conventions, gaps, duplicate records, and funding intervals before interpreting a backtest.
