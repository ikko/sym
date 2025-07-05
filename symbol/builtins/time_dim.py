"""This module provides time_dim-related functionality for Symbol objects.

It includes a mixin that adds properties for accessing the date and time components of a Symbol's name,
as well as for calculating time periods and durations.
"""
import pendulum
from typing import Iterator, Union, Any

from ..core.base_symbol import Symbol

class SymbolTimeDimMixin:
    def _parse_timestamp(self) -> pendulum.DateTime:
        try:
            return pendulum.parse(self.name)
        except Exception:
            return pendulum.now().start_of('day')

    @staticmethod
    def _sorted_by_time(symbol_cls: type[Symbol]) -> list['Symbol']:
        # _parse_timestamp is an instance method, so it must be called on an instance 's'
        return sorted(symbol_cls._numbered, key=lambda s: s._parse_timestamp())

    @property
    def time_head(self) -> 'SymbolHeadTailView':
        # Pass the actual Symbol class to the static method
        return SymbolHeadTailView(SymbolTimeDimMixin._sorted_by_time(self.__class__))

    @property
    def time_tail(self) -> 'SymbolHeadTailView':
        # Pass the actual Symbol class to the static method
        return SymbolHeadTailView(SymbolTimeDimMixin._sorted_by_time(self.__class__)[::-1])

    @property
    def as_date(self) -> pendulum.Date:
        return self._parse_timestamp().date()

    @property
    def as_time(self) -> pendulum.Time:
        return self._parse_timestamp().time()

    @property
    def as_datetime(self) -> pendulum.DateTime:
        return self._parse_timestamp()

    @property
    def day(self) -> int:
        return self._parse_timestamp().day

    @property
    def hour(self) -> int:
        return self._parse_timestamp().hour

    @property
    def minute(self) -> int:
        return self._parse_timestamp().minute

    @property
    def second(self) -> int:
        return self._parse_timestamp().second

    @property
    def period(self) -> pendulum.Duration:
        return self.time_head.period

    @property
    def as_period(self) -> pendulum.Duration:
        return self.time_head.as_period

    @property
    def duration(self) -> pendulum.Duration:
        return self.period

    @property
    def as_duration(self) -> pendulum.Duration:
        return self.as_period

    @property
    def delta(self) -> pendulum.Duration:
        return self.period

    @property
    def as_delta(self) -> pendulum.Duration:
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
    def period(self) -> pendulum.Duration:
        if not self._items:
            return pendulum.duration(0)
        start = self._items[0]._parse_timestamp()
        end = self._items[-1]._parse_timestamp()
        return end - start

    @property
    def as_period(self) -> pendulum.Duration:
        return self.period

    @property
    def days(self) -> int:
        return self.period.days

    @property
    def seconds(self) -> int:
        return self.period.seconds

    def filter_by_month(self, year: int, month: int) -> 'SymbolHeadTailView':
        result = [s for s in self._items
                  if SymbolTimeDimMixin()._parse_timestamp(s).year == year and
                     SymbolTimeDimMixin()._parse_timestamp(s).month == month]
        return SymbolHeadTailView(result)