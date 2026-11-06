import unittest

from sleep_for_duration_kit import parse_duration, sleep_for_duration


class ParseDurationTests(unittest.TestCase):
    def test_single_second(self):
        self.assertEqual(parse_duration("5s"), 5.0)

    def test_single_minute(self):
        self.assertEqual(parse_duration("2m"), 120.0)

    def test_milliseconds(self):
        self.assertEqual(parse_duration("250ms"), 0.25)

    def test_hours_and_days(self):
        self.assertEqual(parse_duration("1h"), 3600.0)
        self.assertEqual(parse_duration("1d"), 86400.0)

    def test_compound_duration(self):
        self.assertEqual(parse_duration("1h30m"), 5400.0)

    def test_compound_with_spaces(self):
        self.assertEqual(parse_duration("1h 30m 15s"), 5415.0)

    def test_decimal_value(self):
        self.assertEqual(parse_duration("1.5s"), 1.5)

    def test_leading_and_trailing_whitespace(self):
        self.assertEqual(parse_duration("  2m  "), 120.0)

    def test_bare_number_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_duration("5")

    def test_unknown_unit_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_duration("5w")

    def test_empty_string_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_duration("")

    def test_non_string_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_duration(5)

    def test_negative_value_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_duration("-5s")


class SleepForDurationTests(unittest.TestCase):
    def test_calls_sleep_with_parsed_value(self):
        calls = []

        def fake_sleep(seconds):
            calls.append(seconds)

        result = sleep_for_duration("2m", sleep=fake_sleep)
        self.assertEqual(result, 120.0)
        self.assertEqual(calls, [120.0])

    def test_returns_seconds_slept(self):
        def fake_sleep(seconds):
            pass

        self.assertEqual(sleep_for_duration("1.5s", sleep=fake_sleep), 1.5)

    def test_invalid_duration_does_not_sleep(self):
        calls = []

        def fake_sleep(seconds):
            calls.append(seconds)

        with self.assertRaises(ValueError):
            sleep_for_duration("nope", sleep=fake_sleep)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
