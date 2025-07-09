"""This module provides time_dim-related functionality for Symbol objects.

It includes a mixin that adds properties for accessing the date and time components of a Symbol's name,
as well as for calculating time periods and durations.
"""
from __future__ import annotations
import datetime
from typing import Iterator, Union, Any, Callable

class SymbolTimeDimMixin:
    @staticmethod
    def _parse_timestamp(s: 'Symbol') -> datetime.datetime:
        try:
            return datetime.datetime.fromisoformat(s.name)
        except ValueError:
            return datetime.datetime.combine(datetime.date.today(), datetime.time.min)

    @staticmethod
    def _sorted_by_time(symb_cls: type['Symbol']) -> list['Symbol']:
        return sorted(symb_cls._numbered, key=lambda s: SymbolTimeDimMixin._parse_timestamp(s))

    @property
    def time_head(self) -> 'SymbolHeadTailView':
        # Pass the actual Symbol class to the static method
        return SymbolHeadTailView(SymbolTimeDimMixin._sorted_by_time(self.__class__))

    @property
    def time_tail(self) -> 'SymbolHeadTailView':
        # Pass the actual Symbol class to the static method
        return SymbolHeadTailView(SymbolTimeDimMixin._sorted_by_time(self.__class__)[::-1])

    @property
    def as_date(self) -> datetime.date:
        return SymbolTimeDimMixin._parse_timestamp(self).date()

    @property
    def as_time(self) -> datetime.time:
        return SymbolTimeDimMixin._parse_timestamp(self).time()

    @property
    def as_datetime(self) -> datetime.datetime:
        return SymbolTimeDimMixin._parse_timestamp(self)

    @property
    def day(self) -> int:
        return SymbolTimeDimMixin._parse_timestamp(self).day

    @property
    def hour(self) -> int:
        return SymbolTimeDimMixin._parse_timestamp(self).hour

    @property
    def minute(self) -> int:
        return SymbolTimeDimMixin._parse_timestamp(self).minute

    @property
    def second(self) -> int:
        return SymbolTimeDimMixin._parse_timestamp(self).second

    @property
    def period(self) -> datetime.timedelta:
        return self.time_head.period

    @property
    def as_period(self) -> datetime.timedelta:
        return self.time_head.as_period

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
        start = SymbolTimeDimMixin._parse_timestamp(self._items[0])
        end = SymbolTimeDimMixin._parse_timestamp(self._items[-1])
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
                  if SymbolTimeDimMixin._parse_timestamp(s).year == year and
                     SymbolTimeDimMixin._parse_timestamp(s).month == month]
        return SymbolHeadTailView(result)

    def filter_by_day(self, year: int, month: int, day: int) -> 'SymbolHeadTailView':
        result = [s for s in self._items
                  if SymbolTimeDimMixin._parse_timestamp(s).year == year and
                     SymbolTimeDimMixin._parse_timestamp(s).month == month and
                     SymbolTimeDimMixin._parse_timestamp(s).day == day]
        return SymbolHeadTailView(result)

    def filter_by_hour(self, year: int, month: int, day: int, hour: int) -> 'SymbolHeadTailView':
        result = [s for s in self._items
                  if SymbolTimeDimMixin._parse_timestamp(s).year == year and
                     SymbolTimeDimMixin._parse_timestamp(s).month == month and
                     SymbolTimeDimMixin._parse_timestamp(s).day == day and
                     SymbolTimeDimMixin._parse_timestamp(s).hour == hour]
        return SymbolHeadTailView(result)

    def filter_by_minute(self, year: int, month: int, day: int, hour: int, minute: int) -> 'SymbolHeadTailView':
        result = [s for s in self._items
                  if SymbolTimeDimMixin._parse_timestamp(s).year == year and
                     SymbolTimeDimMixin._parse_timestamp(s).month == month and
                     SymbolTimeDimMixin._parse_timestamp(s).day == day and
                     SymbolTimeDimMixin._parse_timestamp(s).hour == hour and
                     SymbolTimeDimMixin._parse_timestamp(s).minute == minute]
        return SymbolHeadTailView(result)

    def filter_by_second(self, year: int, month: int, day: int, hour: int, minute: int, second: int) -> 'SymbolHeadTailView':
        result = [s for s in self._items
                  if SymbolTimeDimMixin._parse_timestamp(s).year == year and
                     SymbolTimeDimMixin._parse_timestamp(s).month == month and
                     SymbolTimeDimMixin._parse_timestamp(s).day == day and
                     SymbolTimeDimMixin._parse_timestamp(s).hour == hour and
                     SymbolTimeDimMixin._parse_timestamp(s).minute == minute and
                     SymbolTimeDimMixin._parse_timestamp(s).second == second]
        return SymbolHeadTailView(result)

    def filter_by_weekday(self, weekday: int) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).weekday() == weekday]
        return SymbolHeadTailView(result)

    def filter_by_week_of_year(self, week_of_year: int) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).isocalendar()[1] == week_of_year]
        return SymbolHeadTailView(result)

    def filter_by_quarter(self, quarter: int) -> 'SymbolHeadTailView':
        result = [s for s in self._items if (SymbolTimeDimMixin._parse_timestamp(s).month - 1) // 3 + 1 == quarter]
        return SymbolHeadTailView(result)

    def filter_by_year(self, year: int) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).year == year]
        return SymbolHeadTailView(result)

    def filter_by_time_of_day(self, time_of_day: str) -> 'SymbolHeadTailView':
        # This is a bit more complex as datetime doesn't have a direct equivalent.
        # We can simulate this by checking the hour.
        result = []
        for s in self._items:
            hour = SymbolTimeDimMixin._parse_timestamp(s).hour
            if time_of_day == 'morning' and 5 <= hour < 12:
                result.append(s)
            elif time_of_day == 'afternoon' and 12 <= hour < 17:
                result.append(s)
            elif time_of_day == 'evening' and 17 <= hour < 21:
                result.append(s)
            elif time_of_day == 'night' and (21 <= hour or hour < 5):
                result.append(s)
        return SymbolHeadTailView(result)

    def filter_by_timezone(self, timezone: str) -> 'SymbolHeadTailView':
        # datetime objects are naive by default, so this is not directly supported.
        # We will return an empty list.
        return SymbolHeadTailView([])

    def filter_by_dst(self, is_dst: bool) -> 'SymbolHeadTailView':
        # datetime objects are naive by default, so this is not directly supported.
        # We will return an empty list.
        return SymbolHeadTailView([])

    def filter_by_leap_year(self, is_leap_year: bool) -> 'SymbolHeadTailView':
        result = [s for s in self._items if self._is_leap(SymbolTimeDimMixin._parse_timestamp(s).year) == is_leap_year]
        return SymbolHeadTailView(result)

    def _is_leap(self, year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def filter_by_start_of_month(self) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).day == 1]
        return SymbolHeadTailView(result)

    def filter_by_end_of_month(self) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).day == self._days_in_month(SymbolTimeDimMixin._parse_timestamp(s).year, SymbolTimeDimMixin._parse_timestamp(s).month)]
        return SymbolHeadTailView(result)

    def _days_in_month(self, year: int, month: int) -> int:
        if month == 2:
            return 29 if self._is_leap(year) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31

    def filter_by_start_of_year(self) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).month == 1 and SymbolTimeDimMixin._parse_timestamp(s).day == 1]
        return SymbolHeadTailView(result)

    def filter_by_end_of_year(self) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).month == 12 and SymbolTimeDimMixin._parse_timestamp(s).day == 31]
        return SymbolHeadTailView(result)

    def filter_by_start_of_quarter(self) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).month in [1, 4, 7, 10] and SymbolTimeDimMixin._parse_timestamp(s).day == 1]
        return SymbolHeadTailView(result)

    def filter_by_end_of_quarter(self) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).month in [3, 6, 9, 12] and SymbolTimeDimMixin._parse_timestamp(s).day == self._days_in_month(SymbolTimeDimMixin._parse_timestamp(s).year, SymbolTimeDimMixin._parse_timestamp(s).month)]
        return SymbolHeadTailView(result)

    def filter_by_start_of_week(self) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).weekday() == 0]
        return SymbolHeadTailView(result)

    def filter_by_end_of_week(self) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).weekday() == 6]
        return SymbolHeadTailView(result)

    def filter_by_weekend(self) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).weekday() >= 5]
        return SymbolHeadTailView(result)

    def filter_by_weekday(self) -> 'SymbolHeadTailView':
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).weekday() < 5]
        return SymbolHeadTailView(result)

    def filter_by_yesterday(self) -> 'SymbolHeadTailView':
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).date() == yesterday]
        return SymbolHeadTailView(result)

    def filter_by_today(self) -> 'SymbolHeadTailView':
        today = datetime.date.today()
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).date() == today]
        return SymbolHeadTailView(result)

    def filter_by_tomorrow(self) -> 'SymbolHeadTailView':
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).date() == tomorrow]
        return SymbolHeadTailView(result)

    def filter_by_future(self) -> 'SymbolHeadTailView':
        now = datetime.datetime.now()
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s) > now]
        return SymbolHeadTailView(result)

    def filter_by_past(self) -> 'SymbolHeadTailView':
        now = datetime.datetime.now()
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s) < now]
        return SymbolHeadTailView(result)

    def filter_by_same_day(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).date() == other.date()]
        return SymbolHeadTailView(result)

    def filter_by_same_month(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).month == other.month and SymbolTimeDimMixin._parse_timestamp(s).year == other.year]
        return SymbolHeadTailView(result)

    def filter_by_same_year(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).year == other.year]
        return SymbolHeadTailView(result)

    def filter_by_same_quarter(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if (SymbolTimeDimMixin._parse_timestamp(s).month - 1) // 3 == (other.month - 1) // 3 and SymbolTimeDimMixin._parse_timestamp(s).year == other.year]
        return SymbolHeadTailView(result)

    def filter_by_same_week(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).isocalendar()[1] == other.isocalendar()[1] and SymbolTimeDimMixin._parse_timestamp(s).year == other.year]
        return SymbolHeadTailView(result)

    def filter_by_same_weekday(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).weekday() == other.weekday()]
        return SymbolHeadTailView(result)

    def filter_by_same_time(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).time() == other.time()]
        return SymbolHeadTailView(result)

    def filter_by_between(self, start: Union['Symbol', datetime.datetime], end: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        if isinstance(start, Symbol):
            start = SymbolTimeDimMixin._parse_timestamp(start)
        if isinstance(end, Symbol):
            end = SymbolTimeDimMixin._parse_timestamp(end)
        result = [s for s in self._items if start <= SymbolTimeDimMixin._parse_timestamp(s) <= end]
        return SymbolHeadTailView(result)

    def filter_by_closest(self, other: Union['Symbol', datetime.datetime]) -> 'Symbol':
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        return min(self._items, key=lambda s: abs(SymbolTimeDimMixin._parse_timestamp(s) - other))

    def filter_by_furthest(self, other: Union['Symbol', datetime.datetime]) -> 'Symbol':
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        return max(self._items, key=lambda s: abs(SymbolTimeDimMixin._parse_timestamp(s) - other))

    def filter_by_average(self) -> datetime.datetime:
        if not self._items:
            return datetime.datetime.now()
        return datetime.datetime.fromtimestamp(sum(s._parse_timestamp().timestamp() for s in self._items) / len(self._items))

    def filter_by_median(self) -> datetime.datetime:
        if not self._items:
            return datetime.datetime.now()
        sorted_items = sorted(self._items, key=lambda s: s._parse_timestamp())
        mid = len(sorted_items) // 2
        if len(sorted_items) % 2 == 0:
            return datetime.datetime.fromtimestamp((sorted_items[mid - 1]._parse_timestamp().timestamp() + sorted_items[mid]._parse_timestamp().timestamp()) / 2)
        else:
            return sorted_items[mid]._parse_timestamp()

    def filter_by_mode(self) -> list[datetime.datetime]:
        if not self._items:
            return []
        from collections import Counter
        counts = Counter(s._parse_timestamp() for s in self._items)
        max_count = max(counts.values())
        return [dt for dt, count in counts.items() if count == max_count]

    def filter_by_range(self) -> datetime.timedelta:
        if not self._items:
            return datetime.timedelta(0)
        return self.period

    def filter_by_std(self) -> float:
        if not self._items:
            return 0.0
        import numpy as np
        return np.std([s._parse_timestamp().timestamp() for s in self._items])

    def filter_by_variance(self) -> float:
        if not self._items:
            return 0.0
        import numpy as np
        return np.var([s._parse_timestamp().timestamp() for s in self._items])

    def filter_by_percentile(self, percentile: int) -> datetime.datetime:
        if not self._items:
            return datetime.datetime.now()
        import numpy as np
        return datetime.datetime.fromtimestamp(np.percentile([s._parse_timestamp().timestamp() for s in self._items], percentile))

    def filter_by_quantile(self, quantile: float) -> datetime.datetime:
        if not self._items:
            return datetime.datetime.now()
        import numpy as np
        return datetime.datetime.fromtimestamp(np.quantile([s._parse_timestamp().timestamp() for s in self._items], quantile))

    def filter_by_first(self) -> 'Symbol':
        return self._items[0]

    def filter_by_last(self) -> 'Symbol':
        return self._items[-1]

    def filter_by_nth(self, n: int) -> 'Symbol':
        return self._items[n]

    def filter_by_sample(self, n: int) -> 'SymbolHeadTailView':
        import random
        return SymbolHeadTailView(random.sample(self._items, n))

    def filter_by_shuffle(self) -> 'SymbolHeadTailView':
        import random
        shuffled = list(self._items)
        random.shuffle(shuffled)
        return SymbolHeadTailView(shuffled)

    def filter_by_reverse(self) -> 'SymbolHeadTailView':
        return SymbolHeadTailView(self._items[::-1])

    def filter_by_unique(self) -> 'SymbolHeadTailView':
        return SymbolHeadTailView(list(dict.fromkeys(self._items)))

    def filter_by_count(self) -> int:
        return len(self._items)

    def filter_by_is_empty(self) -> bool:
        return not self._items

    def filter_by_any(self, pred: Callable[['Symbol'], bool]) -> bool:
        return any(pred(s) for s in self._items)

    def filter_by_all(self, pred: Callable[['Symbol'], bool]) -> bool:
        return all(pred(s) for s in self._items)

    def filter_by_none(self, pred: Callable[['Symbol'], bool]) -> bool:
        return not any(pred(s) for s in self._items)

    def filter_by_map(self, fn: Callable[['Symbol'], Any]) -> list[Any]:
        return [fn(s) for s in self._items]

    def filter_by_reduce(self, fn: Callable[[Any, 'Symbol'], Any], initial: Any) -> Any:
        from functools import reduce
        return reduce(fn, self._items, initial)

    def filter_by_sum(self, fn: Callable[['Symbol'], Any]) -> Any:
        return sum(fn(s) for s in self._items)

    def filter_by_max(self, fn: Callable[['Symbol'], Any]) -> Any:
        return max(fn(s) for s in self._items)

    def filter_by_min(self, fn: Callable[['Symbol'], Any]) -> Any:
        return min(fn(s) for s in self._items)

    def filter_by_average(self, fn: Callable[['Symbol'], Any]) -> Any:
        return sum(fn(s) for s in self._items) / len(self._items)

    def filter_by_median(self, fn: Callable[['Symbol'], Any]) -> Any:
        import numpy as np
        return np.median([fn(s) for s in self._items])

    def filter_by_mode(self, fn: Callable[['Symbol'], Any]) -> Any:
        from collections import Counter
        counts = Counter(fn(s) for s in self._items)
        max_count = max(counts.values())
        return [item for item, count in counts.items() if count == max_count]

    def filter_by_std(self, fn: Callable[['Symbol'], Any]) -> Any:
        import numpy as np
        return np.std([fn(s) for s in self._items])

    def filter_by_variance(self, fn: Callable[['Symbol'], Any]) -> Any:
        import numpy as np
        return np.var([fn(s) for s in self._items])

    def filter_by_percentile(self, fn: Callable[['Symbol'], Any], percentile: int) -> Any:
        import numpy as np
        return np.percentile([fn(s) for s in self._items], percentile)

    def filter_by_quantile(self, fn: Callable[['Symbol'], Any], quantile: float) -> Any:
        import numpy as np
        return np.quantile([fn(s) for s in self._items], quantile)

    def filter_by_first(self, fn: Callable[['Symbol'], Any]) -> Any:
        return fn(self._items[0])

    def filter_by_last(self, fn: Callable[['Symbol'], Any]) -> Any:
        return fn(self._items[-1])

    def filter_by_nth(self, fn: Callable[['Symbol'], Any], n: int) -> Any:
        return fn(self._items[n])

    def filter_by_sample(self, fn: Callable[['Symbol'], Any], n: int) -> list[Any]:
        import random
        return [fn(s) for s in random.sample(self._items, n)]

    def filter_by_shuffle(self, fn: Callable[['Symbol'], Any]) -> list[Any]:
        import random
        shuffled = list(self._items)
        random.shuffle(shuffled)
        return [fn(s) for s in shuffled]

    def filter_by_reverse(self, fn: Callable[['Symbol'], Any]) -> list[Any]:
        return [fn(s) for s in self._items[::-1]]

    def filter_by_unique(self, fn: Callable[['Symbol'], Any]) -> list[Any]:
        return list(dict.fromkeys(fn(s) for s in self._items))

    def filter_by_count(self, fn: Callable[['Symbol'], Any]) -> int:
        return len(list(fn(s) for s in self._items))

    def filter_by_is_empty(self, fn: Callable[['Symbol'], Any]) -> bool:
        return not list(fn(s) for s in self._items)

    def filter_by_any(self, fn: Callable[['Symbol'], Any], pred: Callable[[Any], bool]) -> bool:
        return any(pred(fn(s)) for s in self._items)

    def filter_by_all(self, fn: Callable[['Symbol'], Any], pred: Callable[[Any], bool]) -> bool:
        return all(pred(fn(s)) for s in self._items)

    def filter_by_none(self, fn: Callable[['Symbol'], Any], pred: Callable[[Any], bool]) -> bool:
        return not any(pred(fn(s)) for s in self._items)
