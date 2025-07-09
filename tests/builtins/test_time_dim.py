import pytest
import datetime
from sym import Symbol
from sym.builtins.time_dim import SymbolTimeDimMixin, SymbolHeadTailView
from sym.builtins import apply_builtins



def test_parse_timestamp():
    # _parse_timestamp is now a static method, call it directly from the class
    # It expects a Symbol instance as an argument

    # Test with valid ISO format datetime
    s1 = Symbol("2023-01-15T10:30:00")
    dt1 = SymbolTimeDimMixin._parse_timestamp(s1)
    assert dt1 == datetime.datetime(2023, 1, 15, 10, 30, 0)

    # Test with valid ISO format date (time defaults to 00:00:00)
    s2 = Symbol("2023-03-20")
    dt2 = SymbolTimeDimMixin._parse_timestamp(s2)
    assert dt2 == datetime.datetime(2023, 3, 20, 0, 0, 0)

    # Test with invalid format (should return today's date with time 00:00:00)
    s3 = Symbol("invalid-date")
    dt3 = SymbolTimeDimMixin._parse_timestamp(s3)
    assert dt3.date() == datetime.date.today()
    assert dt3.time() == datetime.time(0, 0, 0)

def test_sym_time_dim_properties():
    s_dt = Symbol("2023-04-22T14:45:30")

    assert s_dt.as_date == datetime.date(2023, 4, 22)
    assert s_dt.as_time == datetime.time(14, 45, 30)
    assert s_dt.as_datetime == datetime.datetime(2023, 4, 22, 14, 45, 30)
    assert s_dt.day == 22
    assert s_dt.hour == 14
    assert s_dt.minute == 45
    assert s_dt.second == 30

    # Test with a date-only sym
    s_date_only = Symbol("2023-05-01")
    assert s_date_only.as_date == datetime.date(2023, 5, 1)
    assert s_date_only.as_time == datetime.time(0, 0, 0)
    assert s_date_only.as_datetime == datetime.datetime(2023, 5, 1, 0, 0, 0)


