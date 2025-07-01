"""This module provides datetime-related functionality for Symbol objects.

It includes a mixin that adds properties for accessing the date and time components of a Symbol's name,
as well as for calculating time periods and durations.
"""
import datetime
from typing import Iterator, Union, Any

from ..core.base_symbol import Symbol
from ..core.protocols import SymbolDateTimeProtocol

class SymbolDateTimeMixin(SymbolDateTimeProtocol):
    def _parse_timestamp(self, s: 'Symbol') -> datetime.datetime:
        try:
            return datetime.datetime.fromisoformat(s.name)
        except Exception:
            return datetime.datetime.combine(datetime.date.today(), datetime.time())

    def _sorted_by_time(self) -> list['Symbol']:
        return sorted(self._numbered, key=lambda s: self._parse_timestamp(s))

    @property
    def head(self) -> 'SymbolHeadTailView':
        return SymbolHeadTailView(self._sorted_by_time())

    @property
    def tail(self) -> 'SymbolHeadTailView':
        return SymbolHeadTailView(self._sorted_by_time()[::-1])

    @property
    def as_date(self) -> datetime.date:
        return self._parse_timestamp(self).date()

    @property
    def as_time(self) -> datetime.time:
        return self._parse_timestamp(self).time()

    @property
    def as_datetime(self) -> datetime.datetime:
        return self._parse_timestamp(self)

    @property
    def day(self) -> int:
        return self._parse_timestamp(self).day

    @property
    def hour(self) -> int:
        return self._parse_timestamp(self).hour

    @property
    def minute(self) -> int:
        return self._parse_timestamp(self).minute

    @property
    def second(self) -> int:
        return self._parse_timestamp(self).second

    @property
    def period(self) -> datetime.timedelta:
        return self.head.period

    @property
    def as_period(self) -> datetime.timedelta:
        return self.head.as_period

    @property
    def duration(self) -> datetime.timedelta:
        return self.period

    @property
    def as_duration(self) -> datetime.timedelta:
        return self.as_period

    @property
    def delta(self) -> datetime.timedelta:
        return self.period

    @property
    def as_delta(self) -> datetime.timedelta:
        return self.as_period


class SymbolHeadTailView:
    def __init__(self, items: list['Symbol']):
        self._items = items

    def __getitem__(self, item):
        return self._items[item]

    def __iter__(self) -> Iterator['Symbol']:
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    @property
    def period(self) -> datetime.timedelta:
        if not self._items:
            return datetime.timedelta(0)
        start = SymbolDateTimeMixin()._parse_timestamp(self._items[0])
        end = SymbolDateTimeMixin()._parse_timestamp(self._items[-1])
        return end - start

    @property
    def as_period(self) -> datetime.timedelta:
        return self.period

    @property
    def days(self) -> int:
        return self.period.days

    @property
    def seconds(self) -> int:
        return self.period.seconds

    def filter_by_month(self, year: int, month: int) -> 'SymbolHeadTailView':
        result = [s for s in self._items
                  if SymbolDateTimeMixin()._parse_timestamp(s).year == year and
                     SymbolDateTimeMixin()._parse_timestamp(s).month == month]
        return SymbolHeadTailView(result)


# Attach at runtime:
# Symbol.head = property(SymbolDateTimeMixin.head.fget)
# Symbol.tail = property(SymbolDateTimeMixin.tail.fget)
# Symbol.as_date = property(SymbolDateTimeMixin.as_date.fget)
# Symbol.as_time = property(SymbolDateTimeMixin.as_time.fget)
# Symbol.as_datetime = property(SymbolDateTimeMixin.as_datetime.fget)
# Symbol.day = property(SymbolDateTimeMixin.day.fget)
# Symbol.hour = property(SymbolDateTimeMixin.hour.fget)
# Symbol.minute = property(SymbolDateTimeMixin.minute.fget)
# Symbol.second = property(SymbolDateTimeMixin.second.fget)
# Symbol.period = property(SymbolDateTimeMixin.period.fget)
# Symbol.as_period = property(SymbolDateTimeMixin.as_period.fget)
# Symbol.duration = property(SymbolDateTimeMixin.duration.fget)
# Symbol.as_duration = property(SymbolDateTimeMixin.as_duration.fget)
# Symbol.delta = property(SymbolDateTimeMixin.delta.fget)
# Symbol.as_delta = property(SymbolDateTimeMixin.as_delta.fget)
