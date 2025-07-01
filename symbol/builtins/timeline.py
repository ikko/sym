from typing import List, Tuple, Optional, Iterator
import datetime

from ..core.symbol import Symbol

class Timeline:
    """Represents a series of periods, typically associated with a Symbol."""
    def __init__(self, periods: Optional[List[Tuple[datetime.datetime, datetime.datetime]]] = None):
        self._periods = []
        if periods:
            for start, end in periods:
                self.add_period(start, end)

    def add_period(self, start: datetime.datetime, end: datetime.datetime) -> None:
        """Adds a period to the timeline, ensuring periods are ordered and non-overlapping (if possible)."""
        if start >= end:
            raise ValueError("Period start must be before end.")
        # For simplicity, we'll just append for now. Overlap handling will be more complex.
        self._periods.append((start, end))
        self._periods.sort() # Keep periods sorted

    def __len__(self) -> int:
        return len(self._periods)

    def __iter__(self) -> Iterator[Tuple[datetime.datetime, datetime.datetime]]:
        return iter(self._periods)

    def overlap(self, other: 'Timeline') -> 'Timeline':
        """Calculates the overlapping periods between this timeline and another."""
        overlaps = []
        i, j = 0, 0
        while i < len(self._periods) and j < len(other._periods):
            self_start, self_end = self._periods[i]
            other_start, other_end = other._periods[j]

            # Find the intersection of the two periods
            max_start = max(self_start, other_start)
            min_end = min(self_end, other_end)

            if max_start < min_end: # There is an overlap
                overlaps.append((max_start, min_end))

            # Move to the next period in the timeline that ends earlier
            if self_end < other_end:
                i += 1
            else:
                j += 1
        return Timeline(overlaps)

    def to_ascii(self, resolution: datetime.timedelta = datetime.timedelta(days=1)) -> str:
        """Generates an ASCII representation of the timeline."""
        if not self._periods:
            return "(Empty Timeline)"

        min_date = min(p[0] for p in self._periods).date()
        max_date = max(p[1] for p in self._periods).date()

        lines = []
        current_date = min_date
        while current_date <= max_date:
            line = f"{current_date.isoformat()}: "
            for start, end in self._periods:
                if start.date() <= current_date <= end.date():
                    line += "#" # Represents an active period
                else:
                    line += "-" # Represents an inactive period
            lines.append(line)
            current_date += resolution

        return "\n".join(lines)
