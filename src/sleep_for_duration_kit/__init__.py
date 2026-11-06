"""Parsing and sleeping for human-readable durations.

Public API:
    parse_duration(text) -> float
    sleep_for_duration(text, *, sleep=time.sleep) -> float
"""

from .core import parse_duration, sleep_for_duration

__all__ = ["parse_duration", "sleep_for_duration"]
