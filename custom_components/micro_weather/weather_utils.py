"""Weather helpers for micro_weather integration.

Small, testable utilities for normalizing rain inputs and deciding rain state.
"""
from __future__ import annotations

from typing import Any, Optional


def normalize_rain_rate(value: Any) -> Optional[float]:
    """Normalize a reported rain rate to mm/h.

    Accept numeric inputs (int/float/numeric-strings). Return None for
    unavailable/unparseable values. This function assumes the caller has
    already converted units to mm/h when necessary; sensor units are not
    handled here to keep the function simple and deterministic for tests.
    """
    if value is None:
        return None
    # Booleans are not valid numeric rain rates; treat True/False as None
    # because some sensors report wet/dry as booleans.
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_rain_state(value: Any) -> str:
    """Parse a rain-state-like value and return 'wet' or 'dry'.

    Accepts booleans, numeric flags, and common sensor strings such as
    "on"/"off", "true"/"false", "wet"/"dry". Unknown/missing values
    are considered 'dry'.
    """
    if value is None:
        return "dry"
    if isinstance(value, bool):
        return "wet" if value else "dry"
    try:
        # Numeric 1/0
        if float(value) == 1.0:
            return "wet"
        if float(value) == 0.0:
            return "dry"
    except Exception:
        pass
    s = str(value).strip().lower()
    if s in ("wet", "raining", "rain", "precip", "on", "true", "1", "yes"):
        return "wet"
    return "dry"
