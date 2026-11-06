import re
import time

_UNIT_SECONDS = {
    "ms": 0.001,
    "s": 1.0,
    "m": 60.0,
    "h": 3600.0,
    "d": 86400.0,
}

# A duration is one or more number+unit pairs, optionally separated by spaces.
# The number may be an integer or a decimal. The unit must be one of the known
# suffixes. We deliberately do not accept a bare number: without a unit the
# caller's intent is ambiguous (seconds? milliseconds?) and guessing wrong is
# worse than rejecting the input.
_DURATION_RE = re.compile(
    r"^\s*"
    r"(?P<body>(?:\d+(?:\.\d+)?(?:ms|s|m|h|d)\s*)+)"
    r"$"
)

_PART_RE = re.compile(r"(\d+(?:\.\d+)?)(ms|s|m|h|d)")


def parse_duration(text: str) -> float:
    """Parse a duration string into a number of seconds.

    Accepts one or more number/unit pairs, concatenated with optional
    whitespace, for example ``"5s"``, ``"2m"``, ``"1h30m"``, ``"1.5s"``.
    Units are ``ms``, ``s``, ``m``, ``h`` and ``d``.

    Returns a float number of seconds. Raises ``ValueError`` for anything
    that is not a well-formed duration. There is no implicit unit: a bare
    number is rejected rather than guessed at.
    """
    if not isinstance(text, str):
        raise ValueError("duration must be a string")

    if not _DURATION_RE.match(text):
        raise ValueError(f"invalid duration: {text!r}")

    total = 0.0
    for value, unit in _PART_RE.findall(text):
        total += float(value) * _UNIT_SECONDS[unit]
    return total


def sleep_for_duration(text: str, *, sleep=time.sleep) -> float:
    """Sleep for the duration described by ``text`` and return the seconds slept.

    ``sleep`` is injectable so tests can observe the call without waiting.
    The return value is the parsed number of seconds, which is exactly what
    was passed to ``sleep``.
    """
    seconds = parse_duration(text)
    sleep(seconds)
    return seconds
