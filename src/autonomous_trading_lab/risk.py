from dataclasses import dataclass


@dataclass(frozen=True)
class RiskLimits:
    max_leverage: float = 3.0
    max_position_notional_pct: float = 0.10
    max_portfolio_exposure_pct: float = 0.30
    max_daily_loss_pct: float = 0.02
    max_drawdown_pct: float = 0.10


@dataclass(frozen=True)
class RiskDecision:
    allowed: bool
    reason: str
