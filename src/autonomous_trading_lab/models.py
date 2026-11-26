# -*- coding: utf-8 -*-

from enum import Enum


class Signal(str, Enum):
    LONG = "long"
    SHORT = "short"
    FLAT = "flat"
