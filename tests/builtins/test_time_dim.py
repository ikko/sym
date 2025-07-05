import pytest
import pendulum
from symbol.core.symbol import Symbol
from symbol.builtins.time_dim import SymbolTimeDimMixin, SymbolHeadTailView
from symbol.builtins import apply_builtins



def test_parse_timestamp():
    # _parse_timestamp is now a static method, call it directly from the class
    # It expects a Symbol instance as an argument

    # Test with valid ISO format datetime
    s1 = Symbol("2023-01-15T10:30:00")
    dt1 = SymbolTimeDimMixin._parse_timestamp(s1)
    assert dt1 == pendulum.datetime(2023, 1, 15, 10, 30, 0)

    # Test with valid ISO format date (time defaults to 00:00:00)
    s2 = Symbol("2023-03-20")
    dt2 = SymbolTimeDimMixin._parse_timestamp(s2)
    assert dt2 == pendulum.datetime(2023, 3, 20, 0, 0, 0)

    # Test with invalid format (should return today's date with time 00:00:00)
    s3 = Symbol("invalid-date")
    dt3 = SymbolTimeDimMixin._parse_timestamp(s3)
    assert dt3.date() == pendulum.today().date()
    assert dt3.time() == pendulum.time(0, 0, 0)

def test_symbol_time_dim_properties():
    s_dt = Symbol("2023-04-22T14:45:30")

    assert s_dt.as_date == pendulum.date(2023, 4, 22)
    assert s_dt.as_time == pendulum.time(14, 45, 30)
    assert s_dt.as_datetime == pendulum.datetime(2023, 4, 22, 14, 45, 30)
    assert s_dt.day == 22
    assert s_dt.hour == 14
    assert s_dt.minute == 45
    assert s_dt.second == 30

    # Test with a date-only symbol
    s_date_only = Symbol("2023-05-01")
    assert s_date_only.as_date == pendulum.date(2023, 5, 1)
    assert s_date_only.as_time == pendulum.time(0, 0, 0)
    assert s_date_only.as_datetime == pendulum.datetime(2023, 5, 1, 0, 0, 0)

@pytest.mark.parametrize("setup_and_teardown", [[Symbol("2023-01-01T10:00:00"), Symbol("2023-01-01T12:00:00"), Symbol("2023-01-01T14:00:00")]], indirect=True)
def test_symbol_head_and_tail(setup_and_teardown):
    # Symbols are provided by the fixture in Symbol._numbered
    s_early = Symbol._numbered[0]
    s_middle = Symbol._numbered[1]
    s_late = Symbol._numbered[2]

    # Test head (should be chronologically sorted)
    head_view = s_early.time_head
    assert isinstance(head_view, SymbolHeadTailView)
    assert list(head_view) == [s_early, s_middle, s_late]

    # Test tail (should be reverse chronologically sorted)
    tail_view = s_early.time_tail
    assert isinstance(tail_view, SymbolHeadTailView)
    assert list(tail_view) == [s_late, s_middle, s_early]

@pytest.mark.parametrize("setup_and_teardown", [
    [Symbol("2023-01-01T10:00:00"), Symbol("2023-01-01T11:30:00")],
    [Symbol("2023-01-01T10:00:00")]
], indirect=True)
def test_symbol_period_properties(setup_and_teardown):
    if len(Symbol._numbered) == 2:
        s_start = Symbol._numbered[0]
        s_end = Symbol._numbered[1]
        expected_period = pendulum.duration(hours=1, minutes=30)
        assert s_start.period == expected_period
        assert s_start.as_period == expected_period
        assert s_start.duration == expected_period
        assert s_start.as_duration == expected_period
        assert s_start.delta == expected_period
        assert s_start.as_delta == expected_period
    else: # len(Symbol._numbered) == 1
        s_single = Symbol._numbered[0]
        expected_period_single = pendulum.duration(0)
        assert s_single.period == expected_period_single
        assert s_single.as_period == expected_period_single
        assert s_single.duration == expected_period_single
        assert s_single.as_duration == expected_period_single
        assert s_single.delta == expected_period_single
        assert s_single.as_delta == expected_period_single
