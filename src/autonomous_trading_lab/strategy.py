"""Deterministic, local moving-average baseline strategy."""

from collections.abc import Sequence

from .models import Signal


def moving_average_signal(closes: Sequence[float], fast_window: int, slow_window: int) -> Signal:
    if fast_window < 1 or slow_window <= fast_window:
        raise ValueError("Require 1 <= fast_window < slow_window")
    if len(closes) < slow_window:
        return Signal.FLAT
    fast = sum(closes[-fast_window:]) / fast_window
    slow = sum(closes[-slow_window:]) / slow_window
    if fast > slow:
        return Signal.LONG
    if fast < slow:
        return Signal.SHORT
    return Signal.FLAT
