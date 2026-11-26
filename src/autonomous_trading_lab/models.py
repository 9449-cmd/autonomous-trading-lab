"""Signal representation."""

from enum import Enum


class Signal(str, Enum):
    LONG = "long"
    SHORT = "short"
    FLAT = "flat"

    @property
    def sign(self) -> int:
        return {Signal.LONG: 1, Signal.SHORT: -1, Signal.FLAT: 0}[self]
