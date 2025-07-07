"""This module provides a Timeline class for representing a series of time periods.

It allows for adding, manipulating, and calculating overlaps between timelines.
"""
from typing import List, Tuple, Optional, Iterator
import datetime

class Timeline:
    """Represents a series of periods, typically associated with a Symbol."""
    def __init__(self, periods: Optional[List[Tuple[datetime.datetime, datetime.datetime]]] = None):
        self._periods = []
        if periods:
            for start, end in periods:
                self.add_period(start, end)

    def add_period(self, start: datetime.datetime, end: datetime.datetime) -> None:
        if start >= end:
            raise ValueError("Start datetime must be before end datetime.")
        self._periods.append((start, end))
        self._periods.sort()

    def __iter__(self) -> Iterator[Tuple[datetime.datetime, datetime.datetime]]:
        return iter(self._periods)

    def to_ascii(self, resolution: datetime.timedelta = datetime.timedelta(days=1)) -> str:
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