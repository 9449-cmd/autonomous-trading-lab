from datetime import datetime, timedelta, timezone

import pytest

from autonomous_trading_lab import BacktestConfig, Candle, RiskLimits, evaluate_order, run_backtest
from autonomous_trading_lab.models import Signal
from autonomous_trading_lab.strategy import moving_average_signal


def candles_from_closes(closes):
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return [Candle(start + timedelta(hours=i), price, price, price, price) for i, price in enumerate(closes)]


def test_moving_average_waits_for_enough_history():
    assert moving_average_signal([1, 2], 1, 3) is Signal.FLAT
    assert moving_average_signal([1, 2, 3], 1, 3) is Signal.LONG


def test_backtest_is_deterministic_and_accounts_for_costs():
    bars = candles_from_closes([100, 99, 98, 97, 98, 99, 100, 101, 102])
    result = run_backtest(
        bars,
        fast_window=2,
        slow_window=3,
        config=BacktestConfig(initial_equity=1000, max_leverage=1, risk_limits=RiskLimits()),
    )
    assert len(result.equity_curve) == len(bars)
    assert result.final_equity < 1000  # costs are charged on position changes
    assert result.trades >= 1


def test_backtest_rejects_non_increasing_timestamps():
    bars = candles_from_closes([100, 101])
    with pytest.raises(ValueError, match="strictly increasing"):
        run_backtest([bars[0], bars[0]])


def test_risk_check_fails_closed_and_enforces_position_cap():
    limits = RiskLimits(max_position_notional_pct=0.1)
    assert not evaluate_order(
        equity=1000,
        current_exposure=0,
        order_notional=101,
        daily_loss_pct=0,
        drawdown_pct=0,
        limits=limits,
    ).allowed
    assert not evaluate_order(
        equity=float("nan"),
        current_exposure=0,
        order_notional=1,
        daily_loss_pct=0,
        drawdown_pct=0,
    ).allowed


def test_candle_rejects_invalid_price_ranges():
    with pytest.raises(ValueError, match="high/low"):
        Candle(datetime.now(timezone.utc), 10, 9, 8, 10)
