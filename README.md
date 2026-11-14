# sleep-for-duration-kit

Parse a duration string such as `"5s"` or `"2m"` and suspend execution for that long.

```python
from sleep_for_duration_kit import parse_duration, sleep_for_duration

parse_duration("1h30m")        # 5400.0
sleep_for_duration("250ms")    # sleeps for a quarter second, returns 0.25
```

The exported names are exactly `parse_duration` and `sleep_for_duration`.

## Why this exists

`time.sleep` takes a number of seconds. Callers usually have a string like
`"30s"` or `"5m"` from a config file or command line, and every project that
needs this writes the same regex. This library centralises the parsing and
makes the sleeping step injectable so it can be tested without waiting.

The trade-off: there is no default unit. `parse_duration("5")` raises
`ValueError` instead of assuming seconds. Guessing wrong here is a silent bug
(a timeout that should be five seconds becomes five milliseconds), so the
library refuses ambiguous input.

## The awkward edge

Compound durations are summed, and whitespace between parts is optional, so
`"1h30m"` and `"1h 30m"` are equivalent. However, a unit is required on every
part: `"1h30"` is rejected. Units are `ms`, `s`, `m`, `h` and `d`; anything
else, including a bare number, raises `ValueError`.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

