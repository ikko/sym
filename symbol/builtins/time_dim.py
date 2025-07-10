"""This module provides time_dim-related functionality for Symbol objects.

It includes a mixin that adds properties for accessing the date and time components of a Symbol's name,
as well as for calculating time periods and durations.
"""
from __future__ import annotations
import datetime
from typing import Iterator, Union, Any, Callable

class SymbolTimeDimMixin:
    __slots__ = ('_init_time',)

    def __init__(self):
        self._init_time = datetime.datetime.now()
    @staticmethod
    def _parse_timestamp(s: 'Symbol') -> datetime.datetime:
        """
        what: Parses a Symbol's name into a datetime object.
        why: To extract time-related information from Symbol names.
        how: Attempts ISO 8601 conversion, falls back to today's date.
        when: When accessing time-related properties of a Symbol.
        by (caller(s)): SymbolTimeDimMixin properties.
        how often: Frequently.
        how much: Minimal.
        what is it like: Interpreting a timestamp.
        how, what, why and when to improve: Handle more date/time formats.
        """
        try:
            return datetime.datetime.fromisoformat(s.name)
        except ValueError:
            return datetime.datetime.combine(datetime.date.today(), datetime.time.min)

    @staticmethod
    def _sorted_by_time(symbol_cls: type['Symbol']) -> list['Symbol']:
        """
        what: Sorts Symbols by their timestamp.
        why: To provide chronologically ordered views of Symbols.
        how: Uses `_parse_timestamp` as the sorting key.
        when: When creating time-ordered Symbol views.
        by (caller(s)): time_head, time_tail.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Arranging items by date.
        how, what, why and when to improve: Optimize sorting for large collections.
        """
        return sorted(symbol_cls._numbered, key=lambda s: SymbolTimeDimMixin._parse_timestamp(s))

    @property
    def time_head(self) -> 'SymbolHeadTailView':
        """
        what: Returns a view of Symbols sorted chronologically.
        why: To access the earliest Symbols in a collection.
        how: Calls `_sorted_by_time` and wraps in `SymbolHeadTailView`.
        when: When the earliest Symbols are needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Getting the beginning of a timeline.
        how, what, why and when to improve: N/A.
        """
        # Pass the actual Symbol class to the static method
        return SymbolHeadTailView(SymbolTimeDimMixin._sorted_by_time(self.__class__))

    @property
    def time_tail(self) -> 'SymbolHeadTailView':
        """
        what: Returns a view of Symbols sorted in reverse chronological order.
        why: To access the latest Symbols in a collection.
        how: Calls `_sorted_by_time`, reverses, and wraps in `SymbolHeadTailView`.
        when: When the latest Symbols are needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Getting the end of a timeline.
        how, what, why and when to improve: N/A.
        """
        # Pass the actual Symbol class to the static method
        return SymbolHeadTailView(SymbolTimeDimMixin._sorted_by_time(self.__class__)[::-1])

    @property
    def as_date(self) -> datetime.date:
        """
        what: Returns the date part of the Symbol's name.
        why: To access the date component of a Symbol.
        how: Parses timestamp and extracts date.
        when: When only the date is relevant.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Extracting a date from a timestamp.
        how, what, why and when to improve: N/A.
        """
        return SymbolTimeDimMixin._parse_timestamp(self).date()

    @property
    def as_time(self) -> datetime.time:
        """
        what: Returns the time part of the Symbol's name.
        why: To access the time component of a Symbol.
        how: Parses timestamp and extracts time.
        when: When only the time is relevant.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Extracting a time from a timestamp.
        how, what, why and when to improve: N/A.
        """
        return SymbolTimeDimMixin._parse_timestamp(self).time()

    @property
    def as_datetime(self) -> datetime.datetime:
        """
        what: Returns the full datetime object from the Symbol's name.
        why: To access the complete datetime information.
        how: Parses timestamp.
        when: When the full datetime is relevant.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Getting the full timestamp.
        how, what, why and when to improve: N/A.
        """
        return SymbolTimeDimMixin._parse_timestamp(self)

    @property
    def day(self) -> int:
        """
        what: Returns the day component of the Symbol's datetime.
        why: To access the day of the month.
        how: Parses timestamp and extracts day.
        when: When the day of the month is needed.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Getting a calendar day.
        how, what, why and when to improve: N/A.
        """
        return SymbolTimeDimMixin._parse_timestamp(self).day

    @property
    def hour(self) -> int:
        """
        what: Returns the hour component of the Symbol's datetime.
        why: To access the hour of the day.
        how: Parses timestamp and extracts hour.
        when: When the hour is needed.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Getting a clock hour.
        how, what, why and when to improve: N/A.
        """
        return SymbolTimeDimMixin._parse_timestamp(self).hour

    @property
    def minute(self) -> int:
        """
        what: Returns the minute component of the Symbol's datetime.
        why: To access the minute of the hour.
        how: Parses timestamp and extracts minute.
        when: When the minute is needed.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Getting a clock minute.
        how, what, why and when to improve: N/A.
        """
        return SymbolTimeDimMixin._parse_timestamp(self).minute

    @property
    def second(self) -> int:
        """
        what: Returns the second component of the Symbol's datetime.
        why: To access the second of the minute.
        how: Parses timestamp and extracts second.
        when: When the second is needed.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Getting a clock second.
        how, what, why and when to improve: N/A.
        """
        return SymbolTimeDimMixin._parse_timestamp(self).second

    @property
    def period(self) -> datetime.timedelta:
        """
        what: Returns the time duration between first and last Symbols.
        why: To calculate the span of a time-ordered collection.
        how: Delegates to `time_head.period`.
        when: When the duration of a Symbol sequence is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Measuring a time interval.
        how, what, why and when to improve: N/A.
        """
        return self.time_head.period

    @property
    def as_period(self) -> datetime.timedelta:
        """
        what: Alias for the `period` property.
        why: To provide an alternative, more explicit name.
        how: Returns the value of the `period` property.
        when: When the duration of the view is needed.
        by (caller(s)): SymbolTimeDimMixin properties.
        how often: Infrequently.
        how much: Minimal.
        what is it like: An alternative name for duration.
        how, what, why and when to improve: N/A.
        """
        return self.period

    @property
    def duration(self) -> datetime.timedelta:
        """
        what: Alias for the `period` property.
        why: To provide an alternative, more intuitive name.
        how: Returns the value of the `period` property.
        when: When the duration of a Symbol sequence is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: An alternative name for time span.
        how, what, why and when to improve: N/A.
        """
        return self.period

    @property
    def as_duration(self) -> datetime.timedelta:
        """
        what: Alias for the `as_period` property.
        why: To provide an alternative, more explicit name.
        how: Returns the value of the `as_period` property.
        when: When the duration of a Symbol sequence is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: An alternative name for time span.
        how, what, why and when to improve: N/A.
        """
        return self.as_period

    @property
    def delta(self) -> datetime.timedelta:
        """
        what: Alias for the `period` property.
        why: To provide an alternative, more concise name.
        how: Returns the value of the `period` property.
        when: When the duration of a Symbol sequence is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: An alternative name for time difference.
        how, what, why and when to improve: N/A.
        """
        return self.period

    @property
    def as_delta(self) -> datetime.timedelta:
        """
        what: Alias for the `as_period` property.
        why: To provide an alternative, more concise name.
        how: Returns the value of the `as_period` property.
        when: When the duration of a Symbol sequence is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: An alternative name for time difference.
        how, what, why and when to improve: N/A.
        """
        return self.as_period


class SymbolHeadTailView:
    def __init__(self, items: list['Symbol']):
        """
        what: Initializes a view of Symbols.
        why: To provide a flexible way to work with ordered Symbol collections.
        how: Stores a list of Symbols.
        when: When creating a time-ordered view.
        by (caller(s)): SymbolTimeDimMixin properties.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Creating a filtered list.
        how, what, why and when to improve: N/A.
        """
        self._items = items

    def __getitem__(self, item):
        """
        what: Retrieves a Symbol by index.
        why: To allow direct access to Symbols in the view.
        how: Delegates to the underlying list's `__getitem__`.
        when: When accessing Symbols by their position.
        by (caller(s)): Python's indexing mechanism.
        how often: Frequently.
        how much: Minimal.
        what is it like: Accessing an element in a list.
        how, what, why and when to improve: N/A.
        """
        return self._items[item]

    def __iter__(self) -> Iterator['Symbol']:
        """
        what: Provides an iterator for the Symbols in the view.
        why: To allow iteration over the collection.
        how: Delegates to the underlying list's `__iter__`.
        when: When iterating over Symbols in the view.
        by (caller(s)): Python's iteration mechanism.
        how often: Frequently.
        how much: Minimal.
        what is it like: Looping through a collection.
        how, what, why and when to improve: N/A.
        """
        return iter(self._items)

    def __len__(self):
        """
        what: Returns the number of Symbols in the view.
        why: To get the size of the collection.
        how: Delegates to the underlying list's `__len__`.
        when: When the count of Symbols is needed.
        by (caller(s)): Python's `len()` function.
        how often: Frequently.
        how much: Minimal.
        what is it like: Counting elements in a list.
        how, what, why and when to improve: N/A.
        """
        return len(self._items)

    @property
    def period(self) -> datetime.timedelta:
        """
        what: Returns the time duration between the first and last Symbols.
        why: To calculate the span of the time-ordered view.
        how: Parses timestamps of first and last Symbols, calculates difference.
        when: When the duration of the view is needed.
        by (caller(s)): SymbolTimeDimMixin properties.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Measuring a time interval.
        how, what, why and when to improve: N/A.
        """
        if not self._items:
            return datetime.timedelta(0)
        start = SymbolTimeDimMixin._parse_timestamp(self._items[0])
        end = SymbolTimeDimMixin._parse_timestamp(self._items[-1])
        return end - start

    @property
    def as_period(self) -> datetime.timedelta:
        """
        what: Alias for the `period` property.
        why: To provide an alternative, more explicit name.
        how: Returns the value of the `period` property.
        when: When the duration of a Symbol sequence is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: An alternative name for duration.
        how, what, why and when to improve: N/A.
        """
        return self.period

    @property
    def days(self) -> int:
        """
        what: Returns the number of days in the period.
        why: To access the day component of the duration.
        how: Extracts days from the `period` timedelta.
        when: When the duration in days is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Getting days from a time span.
        how, what, why and when to improve: N/A.
        """
        return self.period.days

    @property
    def seconds(self) -> int:
        """
        what: Returns the number of seconds in the period.
        why: To access the second component of the duration.
        how: Extracts seconds from the `period` timedelta.
        when: When the duration in seconds is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Getting seconds from a time span.
        how, what, why and when to improve: N/A.
        """
        return self.period.seconds

    def filter_by_month(self, year: int, month: int) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by year and month.
        why: To select Symbols within a specific month.
        how: Iterates and checks timestamp's year and month.
        when: When filtering by month.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting entries from a calendar.
        how, what, why and when to improve: Optimize for large collections.
        """
        result = [s for s in self._items
                  if SymbolTimeDimMixin._parse_timestamp(s).year == year and
                     SymbolTimeDimMixin._parse_timestamp(s).month == month]
        return SymbolHeadTailView(result)

    def filter_by_day(self, year: int, month: int, day: int) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by year, month, and day.
        why: To select Symbols within a specific day.
        how: Iterates and checks timestamp's year, month, and day.
        when: When filtering by day.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting entries from a calendar.
        how, what, why and when to improve: Optimize for large collections.
        """
        result = [s for s in self._items
                  if SymbolTimeDimMixin._parse_timestamp(s).year == year and
                     SymbolTimeDimMixin._parse_timestamp(s).month == month and
                     SymbolTimeDimMixin._parse_timestamp(s).day == day]
        return SymbolHeadTailView(result)

    def filter_by_hour(self, year: int, month: int, day: int, hour: int) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by year, month, day, and hour.
        why: To select Symbols within a specific hour.
        how: Iterates and checks timestamp's year, month, day, and hour.
        when: When filtering by hour.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting entries from a timeline.
        how, what, why and when to improve: Optimize for large collections.
        """
        result = [s for s in self._items
                  if SymbolTimeDimMixin._parse_timestamp(s).year == year and
                     SymbolTimeDimMixin._parse_timestamp(s).month == month and
                     SymbolTimeDimMixin._parse_timestamp(s).day == day and
                     SymbolTimeDimMixin._parse_timestamp(s).hour == hour]
        return SymbolHeadTailView(result)

    def filter_by_minute(self, year: int, month: int, day: int, hour: int, minute: int) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by year, month, day, hour, and minute.
        why: To select Symbols within a specific minute.
        how: Iterates and checks timestamp's year, month, day, hour, and minute.
        when: When filtering by minute.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting entries from a timeline.
        how, what, why and when to improve: Optimize for large collections.
        """
        result = [s for s in self._items
                  if SymbolTimeDimMixin._parse_timestamp(s).year == year and
                     SymbolTimeDimMixin._parse_timestamp(s).month == month and
                     SymbolTimeDimMixin._parse_timestamp(s).day == day and
                     SymbolTimeDimMixin._parse_timestamp(s).hour == hour and
                     SymbolTimeDimMixin._parse_timestamp(s).minute == minute]
        return SymbolHeadTailView(result)

    def filter_by_second(self, year: int, month: int, day: int, hour: int, minute: int, second: int) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by year, month, day, hour, minute, and second.
        why: To select Symbols within a specific second.
        how: Iterates and checks timestamp's year, month, day, hour, minute, and second.
        when: When filtering by second.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting entries from a timeline.
        how, what, why and when to improve: Optimize for large collections.
        """
        result = [s for s in self._items
                  if SymbolTimeDimMixin._parse_timestamp(s).year == year and
                     SymbolTimeDimMixin._parse_timestamp(s).month == month and
                     SymbolTimeDimMixin._parse_timestamp(s).day == day and
                     SymbolTimeDimMixin._parse_timestamp(s).hour == hour and
                     SymbolTimeDimMixin._parse_timestamp(s).minute == minute and
                     SymbolTimeDimMixin._parse_timestamp(s).second == second]
        return SymbolHeadTailView(result)

    def filter_by_weekday(self, weekday: int) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by weekday.
        why: To select Symbols occurring on a specific day of the week.
        how: Iterates and checks timestamp's weekday.
        when: When filtering by day of week.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting entries from a weekly schedule.
        how, what, why and when to improve: Optimize for large collections.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).weekday() == weekday]
        return SymbolHeadTailView(result)

    def filter_by_week_of_year(self, week_of_year: int) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by week of year.
        why: To select Symbols occurring in a specific week.
        how: Iterates and checks timestamp's ISO week number.
        when: When filtering by week of year.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting entries from a yearly planner.
        how, what, why and when to improve: Optimize for large collections.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).isocalendar()[1] == week_of_year]
        return SymbolHeadTailView(result)

    def filter_by_quarter(self, quarter: int) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by quarter.
        why: To select Symbols occurring in a specific quarter of the year.
        how: Iterates and checks timestamp's month to determine quarter.
        when: When filtering by quarter.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting entries from a quarterly report.
        how, what, why and when to improve: Optimize for large collections.
        """
        result = [s for s in self._items if (SymbolTimeDimMixin._parse_timestamp(s).month - 1) // 3 + 1 == quarter]
        return SymbolHeadTailView(result)

    def filter_by_year(self, year: int) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by year.
        why: To select Symbols occurring in a specific year.
        how: Iterates and checks timestamp's year.
        when: When filtering by year.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting entries from an annual record.
        how, what, why and when to improve: Optimize for large collections.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).year == year]
        return SymbolHeadTailView(result)

    def filter_by_time_of_day(self, time_of_day: str) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by general time of day.
        why: To categorize Symbols into morning, afternoon, etc.
        how: Checks timestamp's hour against predefined ranges.
        when: When categorizing Symbols by time of day.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Grouping events by part of day.
        how, what, why and when to improve: Allow custom time ranges.
        """
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
        """
        what: Filters Symbols by timezone.
        why: To select Symbols from a specific timezone.
        how: Returns empty list as naive datetimes are used.
        when: When timezone filtering is attempted.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Attempting to filter by unsupported criteria.
        how, what, why and when to improve: Implement timezone awareness in Symbol.
        """
        # datetime objects are naive by default, so this is not directly supported.
        # We will return an empty list.
        return SymbolHeadTailView([])

    def filter_by_dst(self, is_dst: bool) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by Daylight Saving Time status.
        why: To select Symbols based on DST.
        how: Returns empty list as naive datetimes are used.
        when: When DST filtering is attempted.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Attempting to filter by unsupported criteria.
        how, what, why and when to improve: Implement DST awareness in Symbol.
        """
        # datetime objects are naive by default, so this is not directly supported.
        # We will return an empty list.
        return SymbolHeadTailView([])

    def filter_by_leap_year(self, is_leap_year: bool) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by leap year status.
        why: To select Symbols occurring in a leap year.
        how: Checks if the timestamp's year is a leap year.
        when: When filtering by leap year.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting entries from a calendar.
        how, what, why and when to improve: N/A.
        """
        result = [s for s in self._items if self._is_leap(SymbolTimeDimMixin._parse_timestamp(s).year) == is_leap_year]
        return SymbolHeadTailView(result)

    def _is_leap(self, year: int) -> bool:
        """
        what: Checks if a given year is a leap year.
        why: Helper for leap year calculations.
        how: Applies leap year rules (divisible by 4, not 100 unless by 400).
        when: During leap year filtering.
        by (caller(s)): filter_by_leap_year, _days_in_month.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A simple date calculation.
        how, what, why and when to improve: N/A.
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def filter_by_start_of_month(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by start of month.
        why: To select Symbols occurring on the first day of a month.
        how: Checks if the timestamp's day is 1.
        when: When filtering by start of month.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting first-day entries.
        how, what, why and when to improve: N/A.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).day == 1]
        return SymbolHeadTailView(result)

    def filter_by_end_of_month(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by end of month.
        why: To select Symbols occurring on the last day of a month.
        how: Checks if the timestamp's day matches days in month.
        when: When filtering by end of month.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting last-day entries.
        how, what, why and when to improve: N/A.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).day == self._days_in_month(SymbolTimeDimMixin._parse_timestamp(s).year, SymbolTimeDimMixin._parse_timestamp(s).month)]
        return SymbolHeadTailView(result)

    def _days_in_month(self, year: int, month: int) -> int:
        """
        what: Returns the number of days in a given month.
        why: Helper for end-of-month calculations.
        how: Applies rules for 28, 29, 30, or 31 days.
        when: During end-of-month filtering.
        by (caller(s)): filter_by_end_of_month, filter_by_end_of_quarter.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A simple date calculation.
        how, what, why and when to improve: N/A.
        """
        if month == 2:
            return 29 if self._is_leap(year) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31

    def filter_by_start_of_year(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by start of year.
        why: To select Symbols occurring on the first day of a year.
        how: Checks if the timestamp's month is 1 and day is 1.
        when: When filtering by start of year.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting New Year entries.
        how, what, why and when to improve: N/A.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).month == 1 and SymbolTimeDimMixin._parse_timestamp(s).day == 1]
        return SymbolHeadTailView(result)

    def filter_by_end_of_year(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by end of year.
        why: To select Symbols occurring on the last day of a year.
        how: Checks if the timestamp's month is 12 and day is 31.
        when: When filtering by end of year.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting year-end entries.
        how, what, why and when to improve: N/A.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).month == 12 and SymbolTimeDimMixin._parse_timestamp(s).day == 31]
        return SymbolHeadTailView(result)

    def filter_by_start_of_quarter(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by start of quarter.
        why: To select Symbols occurring on the first day of a quarter.
        how: Checks month and day for quarter start.
        when: When filtering by start of quarter.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting quarter-start entries.
        how, what, why and when to improve: N/A.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).month in [1, 4, 7, 10] and SymbolTimeDimMixin._parse_timestamp(s).day == 1]
        return SymbolHeadTailView(result)

    def filter_by_end_of_quarter(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by end of quarter.
        why: To select Symbols occurring on the last day of a quarter.
        how: Checks month and day for quarter end.
        when: When filtering by end of quarter.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting quarter-end entries.
        how, what, why and when to improve: N/A.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).month in [3, 6, 9, 12] and SymbolTimeDimMixin._parse_timestamp(s).day == self._days_in_month(SymbolTimeDimMixin._parse_timestamp(s).year, SymbolTimeDimMixin._parse_timestamp(s).month)]
        return SymbolHeadTailView(result)

    def filter_by_start_of_week(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by start of week.
        why: To select Symbols occurring on the first day of a week.
        how: Checks if the timestamp's weekday is Monday (0).
        when: When filtering by start of week.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting weekly start entries.
        how, what, why and when to improve: Allow custom start day of week.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).weekday() == 0]
        return SymbolHeadTailView(result)

    def filter_by_end_of_week(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by end of week.
        why: To select Symbols occurring on the last day of a week.
        how: Checks if the timestamp's weekday is Sunday (6).
        when: When filtering by end of week.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting weekly end entries.
        how, what, why and when to improve: Allow custom end day of week.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).weekday() == 6]
        return SymbolHeadTailView(result)

    def filter_by_weekend(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by weekend.
        why: To select Symbols occurring on a Saturday or Sunday.
        how: Checks if the timestamp's weekday is 5 (Sat) or 6 (Sun).
        when: When filtering by weekend.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting weekend events.
        how, what, why and when to improve: N/A.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).weekday() >= 5]
        return SymbolHeadTailView(result)

    def filter_by_weekday(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by weekday (Monday to Friday).
        why: To select Symbols occurring on a weekday.
        how: Checks if the timestamp's weekday is less than 5.
        when: When filtering by weekday.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting workday events.
        how, what, why and when to improve: N/A.
        """
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).weekday() < 5]
        return SymbolHeadTailView(result)

    def filter_by_yesterday(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by yesterday's date.
        why: To select Symbols that occurred yesterday.
        how: Compares timestamp's date with yesterday's date.
        when: When filtering by yesterday.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting past day's entries.
        how, what, why and when to improve: N/A.
        """
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).date() == yesterday]
        return SymbolHeadTailView(result)

    def filter_by_today(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by today's date.
        why: To select Symbols that occurred today.
        how: Compares timestamp's date with today's date.
        when: When filtering by today.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting current day's entries.
        how, what, why and when to improve: N/A.
        """
        today = datetime.date.today()
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).date() == today]
        return SymbolHeadTailView(result)

    def filter_by_tomorrow(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by tomorrow's date.
        why: To select Symbols that will occur tomorrow.
        how: Compares timestamp's date with tomorrow's date.
        when: When filtering by tomorrow.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting next day's entries.
        how, what, why and when to improve: N/A.
        """
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).date() == tomorrow]
        return SymbolHeadTailView(result)

    def filter_by_future(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by future dates.
        why: To select Symbols that will occur in the future.
        how: Compares timestamp's date with current datetime.
        when: When filtering by future.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting upcoming events.
        how, what, why and when to improve: N/A.
        """
        now = datetime.datetime.now()
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s) > now]
        return SymbolHeadTailView(result)

    def filter_by_past(self) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by past dates.
        why: To select Symbols that occurred in the past.
        how: Compares timestamp's date with current datetime.
        when: When filtering by past.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting historical events.
        how, what, why and when to improve: N/A.
        """
        now = datetime.datetime.now()
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s) < now]
        return SymbolHeadTailView(result)

    def filter_by_same_day(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by same day as another.
        why: To select Symbols occurring on the same calendar day.
        how: Compares timestamp's date with other Symbol/datetime's date.
        when: When grouping Symbols by day.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Grouping events by date.
        how, what, why and when to improve: N/A.
        """
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).date() == other.date()]
        return SymbolHeadTailView(result)

    def filter_by_same_month(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by same month as another.
        why: To select Symbols occurring in the same calendar month.
        how: Compares timestamp's month and year with other Symbol/datetime.
        when: When grouping Symbols by month.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Grouping events by month.
        how, what, why and when to improve: N/A.
        """
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).month == other.month and SymbolTimeDimMixin._parse_timestamp(s).year == other.year]
        return SymbolHeadTailView(result)

    def filter_by_same_year(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by same year as another.
        why: To select Symbols occurring in the same calendar year.
        how: Compares timestamp's year with other Symbol/datetime's year.
        when: When grouping Symbols by year.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Grouping events by year.
        how, what, why and when to improve: N/A.
        """
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).year == other.year]
        return SymbolHeadTailView(result)

    def filter_by_same_quarter(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by same quarter as another.
        why: To select Symbols occurring in the same calendar quarter.
        how: Compares timestamp's quarter and year with other Symbol/datetime.
        when: When grouping Symbols by quarter.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Grouping events by quarter.
        how, what, why and when to improve: N/A.
        """
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if (SymbolTimeDimMixin._parse_timestamp(s).month - 1) // 3 == (other.month - 1) // 3 and SymbolTimeDimMixin._parse_timestamp(s).year == other.year]
        return SymbolHeadTailView(result)

    def filter_by_same_week(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by same week as another.
        why: To select Symbols occurring in the same calendar week.
        how: Compares timestamp's ISO week and year with other Symbol/datetime.
        when: When grouping Symbols by week.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Grouping events by week.
        how, what, why and when to improve: N/A.
        """
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).isocalendar()[1] == other.isocalendar()[1] and SymbolTimeDimMixin._parse_timestamp(s).year == other.year]
        return SymbolHeadTailView(result)

    def filter_by_same_weekday(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by same weekday as another.
        why: To select Symbols occurring on the same day of the week.
        how: Compares timestamp's weekday with other Symbol/datetime's weekday.
        when: When grouping Symbols by weekday.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Grouping events by day of week.
        how, what, why and when to improve: N/A.
        """
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).weekday() == other.weekday()]
        return SymbolHeadTailView(result)

    def filter_by_same_time(self, other: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols by same time as another.
        why: To select Symbols occurring at the same time of day.
        how: Compares timestamp's time with other Symbol/datetime's time.
        when: When grouping Symbols by time.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Grouping events by time of day.
        how, what, why and when to improve: N/A.
        """
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        result = [s for s in self._items if SymbolTimeDimMixin._parse_timestamp(s).time() == other.time()]
        return SymbolHeadTailView(result)

    def filter_by_between(self, start: Union['Symbol', datetime.datetime], end: Union['Symbol', datetime.datetime]) -> 'SymbolHeadTailView':
        """
        what: Filters Symbols within a datetime range.
        why: To select Symbols occurring between two points in time.
        how: Compares timestamp with start and end datetimes.
        when: When filtering by a time range.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Selecting events within a period.
        how, what, why and when to improve: N/A.
        """
        if isinstance(start, Symbol):
            start = SymbolTimeDimMixin._parse_timestamp(start)
        if isinstance(end, Symbol):
            end = SymbolTimeDimMixin._parse_timestamp(end)
        result = [s for s in self._items if start <= SymbolTimeDimMixin._parse_timestamp(s) <= end]
        return SymbolHeadTailView(result)

    def filter_by_closest(self, other: Union['Symbol', datetime.datetime]) -> 'Symbol':
        """
        what: Finds the Symbol closest to a given datetime.
        why: To identify the nearest event in time.
        how: Calculates absolute time difference, finds minimum.
        when: When finding the closest Symbol.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding the nearest point.
        how, what, why and when to improve: Optimize for large collections.
        """
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        return min(self._items, key=lambda s: abs(SymbolTimeDimMixin._parse_timestamp(s) - other))

    def filter_by_furthest(self, other: Union['Symbol', datetime.datetime]) -> 'Symbol':
        """
        what: Finds the Symbol furthest from a given datetime.
        why: To identify the most distant event in time.
        how: Calculates absolute time difference, finds maximum.
        when: When finding the furthest Symbol.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding the most distant point.
        how, what, why and when to improve: Optimize for large collections.
        """
        if isinstance(other, Symbol):
            other = SymbolTimeDimMixin._parse_timestamp(other)
        return max(self._items, key=lambda s: abs(SymbolTimeDimMixin._parse_timestamp(s) - other))

    def filter_by_average(self) -> datetime.datetime:
        """
        what: Calculates the average timestamp of Symbols.
        why: To find the central point in time for a collection.
        how: Sums timestamps, divides by count, converts to datetime.
        when: When the average timestamp is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding the mean time.
        how, what, why and when to improve: Optimize for large collections.
        """
        if not self._items:
            return datetime.datetime.now()
        return datetime.datetime.fromtimestamp(sum(s._parse_timestamp().timestamp() for s in self._items) / len(self._items))

    def filter_by_median(self) -> datetime.datetime:
        """
        what: Calculates the median timestamp of Symbols.
        why: To find the middle point in time for a collection.
        how: Sorts timestamps, finds middle value.
        when: When the median timestamp is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding the middle time.
        how, what, why and when to improve: Optimize for large collections.
        """
        if not self._items:
            return datetime.datetime.now()
        sorted_items = sorted(self._items, key=lambda s: s._parse_timestamp())
        mid = len(sorted_items) // 2
        if len(sorted_items) % 2 == 0:
            return datetime.datetime.fromtimestamp((sorted_items[mid - 1]._parse_timestamp().timestamp() + sorted_items[mid]._parse_timestamp().timestamp()) / 2)
        else:
            return sorted_items[mid]._parse_timestamp()

    def filter_by_mode(self) -> list[datetime.datetime]:
        """
        what: Finds the most frequent timestamp(s) of Symbols.
        why: To identify common occurrence times.
        how: Counts timestamp frequencies, finds max count.
        when: When identifying common timestamps.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding the most common time.
        how, what, why and when to improve: Optimize for large collections.
        """
        if not self._items:
            return []
        from collections import Counter
        counts = Counter(s._parse_timestamp() for s in self._items)
        max_count = max(counts.values())
        return [dt for dt, count in counts.items() if count == max_count]

    def filter_by_range(self) -> datetime.timedelta:
        """
        what: Returns the time range of Symbols.
        why: To get the total span of time covered by the collection.
        how: Delegates to the `period` property.
        when: When the time range is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Measuring the total duration.
        how, what, why and when to improve: N/A.
        """
        if not self._items:
            return datetime.timedelta(0)
        return self.period

    def filter_by_std(self) -> float:
        """
        what: Calculates the standard deviation of Symbol timestamps.
        why: To measure the dispersion of timestamps.
        how: Uses numpy's `std` on timestamps.
        when: When statistical analysis of timestamps is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Measuring time variability.
        how, what, why and when to improve: Optimize for large collections.
        """
        if not self._items:
            return 0.0
        import numpy as np
        return np.std([s._parse_timestamp().timestamp() for s in self._items])

    def filter_by_variance(self) -> float:
        """
        what: Calculates the variance of Symbol timestamps.
        why: To measure the spread of timestamps.
        how: Uses numpy's `var` on timestamps.
        when: When statistical analysis of timestamps is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Measuring time dispersion.
        how, what, why and when to improve: Optimize for large collections.
        """
        if not self._items:
            return 0.0
        import numpy as np
        return np.var([s._parse_timestamp().timestamp() for s in self._items])

    def filter_by_percentile(self, percentile: int) -> datetime.datetime:
        """
        what: Calculates a percentile of Symbol timestamps.
        why: To find a specific point in the distribution of timestamps.
        how: Uses numpy's `percentile` on timestamps.
        when: When percentile analysis of timestamps is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding a specific time rank.
        how, what, why and when to improve: Optimize for large collections.
        """
        if not self._items:
            return datetime.datetime.now()
        import numpy as np
        return datetime.datetime.fromtimestamp(np.percentile([s._parse_timestamp().timestamp() for s in self._items], percentile))

    def filter_by_quantile(self, quantile: float) -> datetime.datetime:
        """
        what: Calculates a quantile of Symbol timestamps.
        why: To find a specific point in the distribution of timestamps.
        how: Uses numpy's `quantile` on timestamps.
        when: When quantile analysis of timestamps is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding a specific time division.
        how, what, why and when to improve: Optimize for large collections.
        """
        if not self._items:
            return datetime.datetime.now()
        import numpy as np
        return datetime.datetime.fromtimestamp(np.quantile([s._parse_timestamp().timestamp() for s in self._items], quantile))

    def filter_by_first(self) -> 'Symbol':
        """
        what: Returns the first Symbol in the view.
        why: To access the earliest Symbol.
        how: Returns the first element of the internal list.
        when: When the earliest Symbol is needed.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Getting the first item.
        how, what, why and when to improve: N/A.
        """
        return self._items[0]

    def filter_by_last(self) -> 'Symbol':
        """
        what: Returns the last Symbol in the view.
        why: To access the latest Symbol.
        how: Returns the last element of the internal list.
        when: When the latest Symbol is needed.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Getting the last item.
        how, what, why and when to improve: N/A.
        """
        return self._items[-1]

    def filter_by_nth(self, n: int) -> 'Symbol':
        """
        what: Returns the nth Symbol in the view.
        why: To access a Symbol by its position.
        how: Returns the element at the specified index.
        when: When a Symbol at a specific position is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Getting an item by index.
        how, what, why and when to improve: N/A.
        """
        return self._items[n]

    def filter_by_sample(self, n: int) -> 'SymbolHeadTailView':
        """
        what: Returns a random sample of Symbols.
        why: To get a subset of Symbols for analysis or display.
        how: Uses `random.sample` on the internal list.
        when: When a random subset is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on sample size.
        what is it like: Picking random items.
        how, what, why and when to improve: N/A.
        """
        import random
        return SymbolHeadTailView(random.sample(self._items, n)) # nosec

    def filter_by_shuffle(self) -> 'SymbolHeadTailView':
        """
        what: Returns a shuffled view of Symbols.
        why: To randomize the order of Symbols.
        how: Shuffles a copy of the internal list.
        when: When a random order is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Randomizing a deck of cards.
        how, what, why and when to improve: N/A.
        """
        import random
        shuffled = list(self._items)
        random.shuffle(shuffled)
        return SymbolHeadTailView(shuffled)

    def filter_by_reverse(self) -> 'SymbolHeadTailView':
        """
        what: Returns a reversed view of Symbols.
        why: To process Symbols in reverse order.
        how: Reverses a copy of the internal list.
        when: When reverse order processing is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Playing a list backward.
        how, what, why and when to improve: N/A.
        """
        return SymbolHeadTailView(self._items[::-1])

    def filter_by_unique(self) -> 'SymbolHeadTailView':
        """
        what: Returns a view of unique Symbols.
        why: To remove duplicate Symbols from the view.
        how: Uses `dict.fromkeys` to preserve order while getting unique.
        when: When unique Symbols are needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Removing duplicates from a list.
        how, what, why and when to improve: N/A.
        """
        return SymbolHeadTailView(list(dict.fromkeys(self._items)))

    def filter_by_count(self) -> int:
        """
        what: Returns the number of Symbols in the view.
        why: To get the size of the collection.
        how: Returns the length of the internal list.
        when: When the count of Symbols is needed.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Counting elements.
        how, what, why and when to improve: N/A.
        """
        return len(self._items)

    def filter_by_is_empty(self) -> bool:
        """
        what: Checks if the view contains any Symbols.
        why: To determine if the collection is empty.
        how: Checks if the internal list is empty.
        when: When checking for an empty collection.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Checking if a container is empty.
        how, what, why and when to improve: N/A.
        """
        return not self._items

    def filter_by_any(self, pred: Callable[['Symbol'], bool]) -> bool:
        """
        what: Checks if any Symbol satisfies a predicate.
        why: To quickly determine if a condition is met by any Symbol.
        how: Uses `any()` with a generator expression.
        when: When checking for existence of a matching Symbol.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Checking for any match.
        how, what, why and when to improve: N/A.
        """
        return any(pred(s) for s in self._items)

    def filter_by_all(self, pred: Callable[['Symbol'], bool]) -> bool:
        """
        what: Checks if all Symbols satisfy a predicate.
        why: To quickly determine if a condition is met by all Symbols.
        how: Uses `all()` with a generator expression.
        when: When checking for universal matching.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Checking for all matches.
        how, what, why and when to improve: N/A.
        """
        return all(pred(s) for s in self._items)

    def filter_by_none(self, pred: Callable[['Symbol'], bool]) -> bool:
        """
        what: Checks if no Symbol satisfies a predicate.
        why: To quickly determine if no Symbol meets a condition.
        how: Uses `not any()` with a generator expression.
        when: When checking for absence of a matching Symbol.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Checking for no matches.
        how, what, why and when to improve: N/A.
        """
        return not any(pred(s) for s in self._items)

    def filter_by_map(self, fn: Callable[['Symbol'], Any]) -> list[Any]:
        """
        what: Applies a function to each Symbol.
        why: To transform each Symbol in the view.
        how: Uses a list comprehension to apply the function.
        when: When transforming a collection of Symbols.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Transforming a list.
        how, what, why and when to improve: Optimize for large collections.
        """
        return [fn(s) for s in self._items]

    def filter_by_reduce(self, fn: Callable[[Any, 'Symbol'], Any], initial: Any) -> Any:
        """
        what: Applies a function cumulatively to Symbols.
        why: To aggregate Symbols into a single result.
        how: Uses `functools.reduce` with the provided function.
        when: When aggregating Symbols.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Combining elements into one.
        how, what, why and when to improve: Optimize for large collections.
        """
        from functools import reduce
        return reduce(fn, self._items, initial)

    def filter_by_sum(self, fn: Callable[['Symbol'], Any]) -> Any:
        """
        what: Calculates the sum of a function applied to Symbols.
        why: To aggregate numerical values from Symbols.
        how: Uses `sum()` with a generator expression.
        when: When summing values from Symbols.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Summing numbers in a list.
        how, what, why and when to improve: Optimize for large collections.
        """
        return sum(fn(s) for s in self._items)

    def filter_by_max(self, fn: Callable[['Symbol'], Any]) -> Any:
        """
        what: Finds the maximum value of a function applied to Symbols.
        why: To identify the largest value among Symbols.
        how: Uses `max()` with a generator expression.
        when: When finding the maximum value.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding the largest number.
        how, what, why and when to improve: Optimize for large collections.
        """
        return max(fn(s) for s in self._items)

    def filter_by_min(self, fn: Callable[['Symbol'], Any]) -> Any:
        """
        what: Finds the minimum value of a function applied to Symbols.
        why: To identify the smallest value among Symbols.
        how: Uses `min()` with a generator expression.
        when: When finding the minimum value.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding the smallest number.
        how, what, why and when to improve: Optimize for large collections.
        """
        return min(fn(s) for s in self._items)

    def filter_by_average(self, fn: Callable[['Symbol'], Any]) -> Any:
        """
        what: Calculates the average of a function applied to Symbols.
        why: To find the mean value among Symbols.
        how: Sums values, divides by count.
        when: When calculating the average.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Calculating the mean.
        how, what, why and when to improve: Optimize for large collections.
        """
        return sum(fn(s) for s in self._items) / len(self._items)

    def filter_by_median(self, fn: Callable[['Symbol'], Any]) -> Any:
        """
        what: Calculates the median of a function applied to Symbols.
        why: To find the middle value among Symbols.
        how: Uses numpy's `median` on transformed values.
        when: When calculating the median.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding the middle value.
        how, what, why and when to improve: Optimize for large collections.
        """
        import numpy as np
        return np.median([fn(s) for s in self._items])

    def filter_by_mode(self, fn: Callable[['Symbol'], Any]) -> Any:
        """
        what: Finds the most frequent value(s) of a function applied to Symbols.
        why: To identify common values among Symbols.
        how: Counts frequencies, finds max count.
        when: When identifying common values.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding the most common item.
        how, what, why and when to improve: Optimize for large collections.
        """
        from collections import Counter
        counts = Counter(fn(s) for s in self._items)
        max_count = max(counts.values())
        return [item for item, count in counts.items() if count == max_count]

    def filter_by_std(self, fn: Callable[['Symbol'], Any]) -> Any:
        """
        what: Calculates the standard deviation of a function applied to Symbols.
        why: To measure the dispersion of values.
        how: Uses numpy's `std` on transformed values.
        when: When statistical analysis is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Measuring data spread.
        how, what, why and when to improve: Optimize for large collections.
        """
        import numpy as np
        return np.std([fn(s) for s in self._items])

    def filter_by_variance(self, fn: Callable[['Symbol'], Any]) -> Any:
        """
        what: Calculates the variance of a function applied to Symbols.
        why: To measure the spread of values.
        how: Uses numpy's `var` on transformed values.
        when: When statistical analysis is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Measuring data dispersion.
        how, what, why and when to improve: Optimize for large collections.
        """
        import numpy as np
        return np.var([fn(s) for s in self._items])

    def filter_by_percentile(self, fn: Callable[['Symbol'], Any], percentile: int) -> Any:
        """
        what: Calculates a percentile of a function applied to Symbols.
        why: To find a specific point in the distribution of values.
        how: Uses numpy's `percentile` on transformed values.
        when: When percentile analysis is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding a specific data rank.
        how, what, why and when to improve: Optimize for large collections.
        """
        import numpy as np
        return np.percentile([fn(s) for s in self._items], percentile)

    def filter_by_quantile(self, quantile: float) -> Any:
        """
        what: Calculates a quantile of a function applied to Symbols.
        why: To find a specific point in the distribution of values.
        how: Uses numpy's `quantile` on transformed values.
        when: When quantile analysis is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Finding a specific data division.
        how, what, why and when to improve: Optimize for large collections.
        """
        import numpy as np
        return np.quantile([fn(s) for s in self._items], quantile)

    def filter_by_first(self, fn: Callable[['Symbol'], Any]) -> Any:
        """
        what: Returns the first transformed Symbol.
        why: To access the transformed value of the earliest Symbol.
        how: Applies function to the first element.
        when: When the transformed earliest Symbol is needed.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Getting the first transformed item.
        how, what, why and when to improve: N/A.
        """
        return fn(self._items[0])

    def filter_by_last(self, fn: Callable[['Symbol'], Any]) -> Any:
        """
        what: Returns the last transformed Symbol.
        why: To access the transformed value of the latest Symbol.
        how: Applies function to the last element.
        when: When the transformed latest Symbol is needed.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Getting the last transformed item.
        how, what, why and when to improve: N/A.
        """
        return fn(self._items[-1])

    def filter_by_nth(self, fn: Callable[['Symbol'], Any], n: int) -> Any:
        """
        what: Returns the nth transformed Symbol.
        why: To access the transformed value of a Symbol by position.
        how: Applies function to the element at the specified index.
        when: When a transformed Symbol at a specific position is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Getting a transformed item by index.
        how, what, why and when to improve: N/A.
        """
        return fn(self._items[n])

    def filter_by_sample(self, fn: Callable[['Symbol'], Any], n: int) -> list[Any]:
        """
        what: Returns a random sample of transformed Symbols.
        why: To get a subset of transformed Symbols for analysis.
        how: Uses `random.sample` on the internal list, applies function.
        when: When a random subset of transformed Symbols is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on sample size.
        what is it like: Picking random transformed items.
        how, what, why and when to improve: N/A.
        """
        import random
        return [fn(s) for s in random.sample(self._items, n)] # nosec

    def filter_by_shuffle(self, fn: Callable[['Symbol'], Any]) -> list[Any]:
        """
        what: Returns a shuffled view of transformed Symbols.
        why: To randomize the order of transformed Symbols.
        how: Shuffles a copy of the internal list, applies function.
        when: When a random order of transformed Symbols is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Randomizing transformed items.
        how, what, why and when to improve: N/A.
        """
        import random
        shuffled = list(self._items)
        random.shuffle(shuffled)
        return [fn(s) for s in shuffled]

    def filter_by_reverse(self, fn: Callable[['Symbol'], Any]) -> list[Any]:
        """
        what: Returns a reversed view of transformed Symbols.
        why: To process transformed Symbols in reverse order.
        how: Reverses a copy of the internal list, applies function.
        when: When reverse order processing of transformed Symbols is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Playing transformed list backward.
        how, what, why and when to improve: N/A.
        """
        return [fn(s) for s in self._items[::-1]]

    def filter_by_unique(self, fn: Callable[['Symbol'], Any]) -> list[Any]:
        """
        what: Returns a view of unique transformed Symbols.
        why: To remove duplicate transformed Symbols.
        how: Uses `dict.fromkeys` on transformed values.
        when: When unique transformed Symbols are needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Removing duplicates from transformed list.
        how, what, why and when to improve: N/A.
        """
        return list(dict.fromkeys(fn(s) for s in self._items))

    def filter_by_count(self, fn: Callable[['Symbol'], Any]) -> int:
        """
        what: Returns the number of transformed Symbols.
        why: To get the size of the transformed collection.
        how: Returns the length of the transformed list.
        when: When the count of transformed Symbols is needed.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Counting transformed elements.
        how, what, why and when to improve: N/A.
        """
        return len(list(fn(s) for s in self._items))

    def filter_by_is_empty(self, fn: Callable[['Symbol'], Any]) -> bool:
        """
        what: Checks if the transformed view contains any Symbols.
        why: To determine if the transformed collection is empty.
        how: Checks if the transformed list is empty.
        when: When checking for an empty transformed collection.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: Checking if transformed container is empty.
        how, what, why and when to improve: N/A.
        """
        return not list(fn(s) for s in self._items)

    def filter_by_any(self, fn: Callable[['Symbol'], bool], pred: Callable[[Any], bool]) -> bool:
        """
        what: Checks if any transformed Symbol satisfies a predicate.
        why: To quickly determine if a condition is met by any transformed Symbol.
        how: Uses `any()` with a generator expression.
        when: When checking for existence of a matching transformed Symbol.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Checking for any transformed match.
        how, what, why and when to improve: N/A.
        """
        return any(pred(fn(s)) for s in self._items)

    def filter_by_all(self, fn: Callable[['Symbol'], bool], pred: Callable[[Any], bool]) -> bool:
        """
        what: Checks if all transformed Symbols satisfy a predicate.
        why: To quickly determine if a condition is met by all transformed Symbols.
        how: Uses `all()` with a generator expression.
        when: When checking for universal transformed matching.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Checking for all transformed matches.
        how, what, why and when to improve: N/A.
        """
        return all(pred(fn(s)) for s in self._items)

    def filter_by_none(self, fn: Callable[['Symbol'], bool], pred: Callable[[Any], bool]) -> bool:
        """
        what: Checks if no transformed Symbol satisfies a predicate.
        why: To quickly determine if no transformed Symbol meets a condition.
        how: Uses `not any()` with a generator expression.
        when: When checking for absence of a matching transformed Symbol.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Checking for no transformed matches.
        how, what, why and when to improve: N/A.
        """
        return not any(pred(fn(s)) for s in self._items)
