# Autonomous Trading Lab

Private research platform for leveraged cryptocurrency perpetual-futures strategies.

> This repository is for historical research, backtesting, and simulated trading only. It does not execute live orders.

## Initial scope

- Cryptocurrency perpetual contract market data
- Volatility-aware trend-following baseline
- Funding-rate constraints
- Position and portfolio risk limits
- Backtesting and paper trading
- Reproducible audit records

## Safety policy

- No live order API is enabled in this repository.
- Backtests must model fees, slippage, funding, latency, and liquidation.
- Paper trading must remain separate from real exchange credentials.
- Strategy signals are advisory and are not financial advice.

## Planned stack

- Python / FastAPI
- PostgreSQL / TimescaleDB
- React / Next.js
- Docker Compose
