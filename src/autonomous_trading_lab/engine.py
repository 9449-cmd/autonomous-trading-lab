"""Small, deterministic close-to-close backtesting engine.

Signals observed at a candle close are applied to the *next* candle, avoiding
same-bar lookahead. This educational engine is not an execution simulator.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isfinite
from typing import Iterable

from .models import Signal
from .risk import RiskLimits
from .strategy import moving_average_signal


@dataclass(frozen=True)
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0
    funding_rate: float = 0.0

    def __post_init__(self) -> None:
        values = (self.open, self.high, self.low, self.close, self.volume, self.funding_rate)
        if not all(isfinite(value) for value in values):
            raise ValueError("Candle values must be finite")
        if min(self.open, self.high, self.low, self.close) <= 0 or self.volume < 0:
            raise ValueError("Prices must be positive and volume cannot be negative")
        if self.high < max(self.open, self.close) or self.low > min(self.open, self.close):
            raise ValueError("Candle high/low do not contain open and close")


@dataclass(frozen=True)
class BacktestConfig:
    initial_equity: float = 10_000.0
    max_leverage: float = 1.0
    fee_rate: float = 0.0004
    slippage_rate: float = 0.0002
    risk_limits: RiskLimits = RiskLimits()

    def __post_init__(self) -> None:
        if not isfinite(self.initial_equity) or self.initial_equity <= 0:
            raise ValueError("initial_equity must be positive")
        if not 0 < self.max_leverage <= self.risk_limits.max_leverage:
            raise ValueError("max_leverage must be positive and within risk limits")
        if not 0 <= self.fee_rate < 1 or not 0 <= self.slippage_rate < 1:
            raise ValueError("fee and slippage rates must be in [0, 1)")


@dataclass(frozen=True)
class EquityPoint:
    timestamp: datetime
    equity: float
    exposure: float


@dataclass(frozen=True)
class BacktestResult:
    initial_equity: float
    final_equity: float
    total_return_pct: float
    max_drawdown_pct: float
    trades: int
    equity_curve: tuple[EquityPoint, ...]
    stopped_reason: str | None = None


def run_backtest(
    candles: Iterable[Candle],
    *,
    fast_window: int = 5,
    slow_window: int = 20,
    config: BacktestConfig = BacktestConfig(),
) -> BacktestResult:
    """Run a long/short SMA baseline; funding is signed (positive means longs pay).

    Position is a signed equity multiple, bounded by configured leverage. Fees and
    slippage are charged on changes in exposure. When the daily loss limit trips,
    the engine goes flat for the remainder of that UTC day.
    """
    bars = tuple(candles)
    if fast_window < 1 or slow_window <= fast_window:
        raise ValueError("Require 1 <= fast_window < slow_window")
    if any(bars[index].timestamp >= bars[index + 1].timestamp for index in range(len(bars) - 1)):
        raise ValueError("Candle timestamps must be strictly increasing")

    equity = config.initial_equity
    peak = equity
    max_drawdown = 0.0
    exposure = 0.0
    trade_count = 0
    daily_start = equity
    active_day = bars[0].timestamp.date() if bars else None
    stopped_reason = None
    points: list[EquityPoint] = []
    closes: list[float] = []

    for index, bar in enumerate(bars):
        day = bar.timestamp.date()
        if day != active_day:
            active_day, daily_start = day, equity
            stopped_reason = None
        if index:
            previous_close = bars[index - 1].close
            price_return = bar.close / previous_close - 1.0
            # Exposure is held over the interval from prior close to this close.
            period_return = exposure * price_return - exposure * bar.funding_rate
            equity *= max(0.0, 1.0 + period_return)

        peak = max(peak, equity)
        drawdown = (peak - equity) / peak if peak else 0.0
        max_drawdown = max(max_drawdown, drawdown)
        daily_loss = (daily_start - equity) / daily_start if daily_start else 0.0
        if daily_loss >= config.risk_limits.max_daily_loss_pct:
            stopped_reason = "daily_loss_limit"
            target = 0.0
        elif drawdown >= config.risk_limits.max_drawdown_pct:
            stopped_reason = "max_drawdown_limit"
            target = 0.0
        elif stopped_reason:
            target = 0.0
        else:
            closes.append(bar.close)
            signal = moving_average_signal(closes, fast_window, slow_window)
            target = config.max_leverage * signal.sign

        if target != exposure:
            turnover = abs(target - exposure)
            equity *= max(0.0, 1.0 - turnover * (config.fee_rate + config.slippage_rate))
            if target != 0.0:
                trade_count += 1
            exposure = target
        points.append(EquityPoint(bar.timestamp, equity, exposure))

    final = equity
    return BacktestResult(
        initial_equity=config.initial_equity,
        final_equity=final,
        total_return_pct=(final / config.initial_equity - 1.0) * 100.0,
        max_drawdown_pct=max_drawdown * 100.0,
        trades=trade_count,
        equity_curve=tuple(points),
        stopped_reason=stopped_reason,
    )
