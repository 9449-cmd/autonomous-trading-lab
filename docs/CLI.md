## Running a local simulation

```bash
python -m autonomous_trading_lab.cli --initial-equity 10000 --max-leverage 1
```

The CLI uses synthetic OHLCV data and never sends network requests or exchange orders.
