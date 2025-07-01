import pytest
import datetime
from symbol.core.symbol import Symbol
from symbol.builtins.datetime import SymbolDateTimeMixin, SymbolHeadTailView
from symbol.builtins import apply_builtins

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Ensure builtins are applied before each test
    apply_builtins()
    # Clear _numbered for predictable testing of head/tail
    Symbol._numbered.clear()
    yield
    # Clean up after each test if necessary
    Symbol._numbered.clear()

def test_parse_timestamp():
    # _parse_timestamp is now a static method, call it directly from the class
    # It expects a Symbol instance as an argument

    # Test with valid ISO format datetime
    s1 = Symbol("2023-01-15T10:30:00")
    dt1 = SymbolDateTimeMixin._parse_timestamp(s1)
    assert dt1 == datetime.datetime(2023, 1, 15, 10, 30, 0)

    # Test with valid ISO format date (time defaults to 00:00:00)
    s2 = Symbol("2023-03-20")
    dt2 = SymbolDateTimeMixin._parse_timestamp(s2)
    assert dt2 == datetime.datetime(2023, 3, 20, 0, 0, 0)

    # Test with invalid format (should return today's date with time 00:00:00)
    s3 = Symbol("invalid-date")
    dt3 = SymbolDateTimeMixin._parse_timestamp(s3)
    assert dt3.date() == datetime.date.today()
    assert dt3.time() == datetime.time(0, 0, 0)

def test_symbol_datetime_properties():
    s_dt = Symbol("2023-04-22T14:45:30")

    assert s_dt.as_date == datetime.date(2023, 4, 22)
    assert s_dt.as_time == datetime.time(14, 45, 30)
    assert s_dt.as_datetime == datetime.datetime(2023, 4, 22, 14, 45, 30)
    assert s_dt.day == 22
    assert s_dt.hour == 14
    assert s_dt.minute == 45
    assert s_dt.second == 30

    # Test with a date-only symbol
    s_date_only = Symbol("2023-05-01")
    assert s_date_only.as_date == datetime.date(2023, 5, 1)
    assert s_date_only.as_time == datetime.time(0, 0, 0)
    assert s_date_only.as_datetime == datetime.datetime(2023, 5, 1, 0, 0, 0)

def test_symbol_head_and_tail():
    # Create symbols with different timestamps
    s_early = Symbol("2023-01-01T10:00:00")
    s_middle = Symbol("2023-01-01T12:00:00")
    s_late = Symbol("2023-01-01T14:00:00")

    # Symbols are added to _numbered upon creation. Ensure they are in _numbered.
    # The order in _numbered is insertion order, not chronological.
    # The _sorted_by_time method in SymbolDateTimeMixin is supposed to handle sorting.

    # Test head (should be chronologically sorted)
    head_view = s_early.head # Any symbol instance can call head/tail
    assert isinstance(head_view, SymbolHeadTailView)
    assert list(head_view) == [s_early, s_middle, s_late]

    # Test tail (should be reverse chronologically sorted)
    tail_view = s_early.tail
    assert isinstance(tail_view, SymbolHeadTailView)
    assert list(tail_view) == [s_late, s_middle, s_early]

def test_symbol_period_properties():
    s_start = Symbol("2023-01-01T10:00:00")
    s_end = Symbol("2023-01-01T11:30:00")

    # Test period, duration, delta properties
    expected_period = datetime.timedelta(hours=1, minutes=30)

    assert s_start.period == expected_period
    assert s_start.as_period == expected_period
    assert s_start.duration == expected_period
    assert s_start.as_duration == expected_period
    assert s_start.delta == expected_period
    assert s_start.as_delta == expected_period

    # Test with a single symbol (period should be 0)
    s_single = Symbol("2023-01-01T10:00:00")
    assert s_single.period == datetime.timedelta(0)