"""This module provides a Timeline class for representing a series of time periods.

It allows for adding, manipulating, and calculating overlaps between timelines.
"""
from typing import List, Tuple, Optional, Iterator
import datetime

class Timeline:
    """Represents a series of periods, typically associated with a Symbol."""
    def __init__(self, periods: Optional[List[Tuple[datetime.datetime, datetime.datetime]]] = None):
        """
        what: Initializes a Timeline instance.
        why: To represent a series of time periods.
        how: Stores a list of (start, end) datetime tuples.
        when: When creating a new timeline.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Creating a schedule.
        how, what, why and when to improve: Handle overlapping periods automatically.
        """
        self._periods = []
        if periods:
            for start, end in periods:
                self.add_period(start, end)

    def add_period(self, start: datetime.datetime, end: datetime.datetime) -> None:
        """
        what: Adds a period to the timeline.
        why: To extend the timeline with new time intervals.
        how: Appends (start, end) tuple and sorts the periods.
        when: When a new time period needs to be added.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Adding an event to a calendar.
        how, what, why and when to improve: Optimize sorting for large number of periods.
        """
        if start >= end:
            raise ValueError("Start datetime must be before end datetime.")
        self._periods.append((start, end))
        self._periods.sort()

    def __iter__(self) -> Iterator[Tuple[datetime.datetime, datetime.datetime]]:
        """
        what: Provides an iterator for the timeline periods.
        why: To allow iteration over the time intervals.
        how: Returns an iterator over the internal list of periods.
        when: When iterating over the timeline.
        by (caller(s)): Python's iteration mechanism.
        how often: Frequently.
        how much: Minimal.
        what is it like: Looping through events.
        how, what, why and when to improve: N/A.
        """
        return iter(self._periods)

    def to_ascii(self, resolution: datetime.timedelta = datetime.timedelta(days=1)) -> str:
        """
        what: Generates an ASCII art representation of the timeline.
        why: To visualize the timeline in a text-based format.
        how: Creates a string with markers for active periods.
        when: When visualizing the timeline.
        by (caller(s)): External debugging tools.
        how often: Infrequently.
        how much: Depends on timeline duration.
        what is it like: Drawing a text-based Gantt chart.
        how, what, why and when to improve: Improve formatting, add more details.
        """
        if not self._periods:
            return ""

        min_time = min(p[0] for p in self._periods)
        max_time = max(p[1] for p in self._periods)

        # Adjust min_time to the start of the day for consistent alignment
        min_time = datetime.datetime(min_time.year, min_time.month, min_time.day)

        # Calculate total duration and number of steps
        total_duration = max_time - min_time
        num_steps = int(total_duration / resolution) + 1

        # Create a timeline string
        timeline_str = ""
        for i in range(num_steps):
            current_time = min_time + i * resolution
            marker = "-"
            for start, end in self._periods:
                if start <= current_time < end:
                    marker = "#"
                    break
            timeline_str += marker

        return timeline_str