"""Fail-closed, pre-trade risk checks for simulated positions."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class RiskLimits:
    max_leverage: float = 3.0
    max_position_notional_pct: float = 0.10
    max_portfolio_exposure_pct: float = 0.30
    max_daily_loss_pct: float = 0.02
    max_drawdown_pct: float = 0.10

    def __post_init__(self) -> None:
        if not isfinite(self.max_leverage) or self.max_leverage <= 0:
            raise ValueError("max_leverage must be positive")
        for name in (
            "max_position_notional_pct",
            "max_portfolio_exposure_pct",
            "max_daily_loss_pct",
            "max_drawdown_pct",
        ):
            value = getattr(self, name)
            if not isfinite(value) or not 0 < value <= 1:
                raise ValueError(f"{name} must be in (0, 1]")


@dataclass(frozen=True)
class RiskDecision:
    allowed: bool
    reason: str


def evaluate_order(
    *,
    equity: float,
    current_exposure: float,
    order_notional: float,
    daily_loss_pct: float,
    drawdown_pct: float,
    limits: RiskLimits = RiskLimits(),
) -> RiskDecision:
    """Check a simulated order using absolute notional and current portfolio exposure."""
    numbers = (equity, current_exposure, order_notional, daily_loss_pct, drawdown_pct)
    if not all(isfinite(value) for value in numbers) or equity <= 0 or order_notional < 0:
        return RiskDecision(False, "invalid_or_non_finite_input")
    if daily_loss_pct >= limits.max_daily_loss_pct:
        return RiskDecision(False, "daily_loss_limit")
    if drawdown_pct >= limits.max_drawdown_pct:
        return RiskDecision(False, "max_drawdown_limit")
    order_pct = order_notional / equity
    if order_pct > limits.max_position_notional_pct:
        return RiskDecision(False, "position_notional_limit")
    if abs(current_exposure) + order_pct > limits.max_portfolio_exposure_pct:
        return RiskDecision(False, "portfolio_exposure_limit")
    if abs(current_exposure) + order_pct > limits.max_leverage:
        return RiskDecision(False, "leverage_limit")
    return RiskDecision(True, "allowed")
