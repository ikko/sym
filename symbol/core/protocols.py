"""This module defines the protocols that govern the behavior of Symbol objects.

These protocols establish a clear contract for extending the Symbol class with new functionality,
promoting a clean and maintainable architecture.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Iterator, List, Optional, Protocol, Union, Callable, Awaitable, runtime_checkable
import datetime
import enum

class MixinHealthState(enum.Enum):
    """
    what: Defines states for mixin health.
    why: To standardize health reporting for mixins.
    how: Enumerates possible health conditions.
    when: When reporting or checking mixin health.
    by (caller(s)): Mixin implementations, Symbol.stat, Symbol.ls.
    how often: Infrequently.
    how much: Minimal.
    what is it like: A status indicator.
    how, what, why and when to improve: Add more granular states if needed.
    """
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class SymbolPathProtocol(Protocol):
    @abstractmethod
    def path_to(self, target: 'Symbol') -> List['Symbol']:

        """
        what: Finds a path from this Symbol to a target Symbol.
        why: To define the contract for pathfinding operations.
        how: Abstract method, implementation varies.
        when: When a path between Symbols is needed.
        by (caller(s)): Implementations of SymbolPathProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for navigation.
        how, what, why and when to improve: N/A.
        """
        ...

    @abstractmethod
    def match(self, predicate: Callable[[Symbol], bool], traversal: str = 'dfs') -> Iterator[Symbol]:
        """
        what: Finds Symbols matching a predicate.
        why: To define the contract for filtering Symbols.
        how: Abstract method, implementation varies.
        when: When searching for specific Symbols.
        by (caller(s)): Implementations of SymbolPathProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for searching.
        how, what, why and when to improve: N/A.
        """
        ...


class SymbolTimeDimProtocol(Protocol):
    @property
    @abstractmethod
    def head(self) -> Any:
        """
        what: Returns a view of Symbols sorted chronologically.
        why: To define the contract for time-ordered views.
        how: Abstract property, implementation varies.
        when: When time-ordered Symbol views are needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for a timeline start.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def tail(self) -> Any:
        """
        what: Returns a view of Symbols sorted in reverse chronologically.
        why: To define the contract for reverse time-ordered views.
        how: Abstract property, implementation varies.
        when: When reverse time-ordered Symbol views are needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for a timeline end.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def as_date(self) -> datetime.date:
        """
        what: Returns the date part of the Symbol's name.
        why: To define the contract for date extraction.
        how: Abstract property, implementation varies.
        when: When the date component of a Symbol is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for date access.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def as_time(self) -> datetime.time:
        """
        what: Returns the time part of the Symbol's name.
        why: To define the contract for time extraction.
        how: Abstract property, implementation varies.
        when: When the time component of a Symbol is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for time access.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def as_datetime(self) -> datetime.datetime:
        """
        what: Returns the full datetime object from the Symbol's name.
        why: To define the contract for datetime extraction.
        how: Abstract property, implementation varies.
        when: When the full datetime of a Symbol is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for datetime access.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def day(self) -> int:
        """
        what: Returns the day component of the Symbol's datetime.
        why: To define the contract for day extraction.
        how: Abstract property, implementation varies.
        when: When the day of the month is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for day access.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def hour(self) -> int:
        """
        what: Returns the hour component of the Symbol's datetime.
        why: To define the contract for hour extraction.
        how: Abstract property, implementation varies.
        when: When the hour is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for hour access.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def minute(self) -> int:
        """
        what: Returns the minute component of the Symbol's datetime.
        why: To define the contract for minute extraction.
        how: Abstract property, implementation varies.
        when: When the minute is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for minute access.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def second(self) -> int:
        """
        what: Returns the second component of the Symbol's datetime.
        why: To define the contract for second extraction.
        how: Abstract property, implementation varies.
        when: When the second is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for second access.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def period(self) -> datetime.timedelta:
        """
        what: Returns the time duration between first and last Symbols.
        why: To define the contract for period calculation.
        how: Abstract property, implementation varies.
        when: When the duration of a Symbol sequence is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for time span.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def as_period(self) -> datetime.timedelta:
        """
        what: Alias for the `period` property.
        why: To define the contract for period alias.
        how: Abstract property, implementation varies.
        when: When the duration of a Symbol sequence is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for period alias.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def duration(self) -> datetime.timedelta:
        """
        what: Alias for the `period` property.
        why: To define the contract for duration alias.
        how: Abstract property, implementation varies.
        when: When the duration of a Symbol sequence is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for duration alias.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def as_duration(self) -> datetime.timedelta:
        """
        what: Alias for the `as_period` property.
        why: To define the contract for duration alias.
        how: Abstract property, implementation varies.
        when: When the duration of a Symbol sequence is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for duration alias.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def delta(self) -> datetime.timedelta:
        """
        what: Alias for the `period` property.
        why: To define the contract for delta alias.
        how: Abstract property, implementation varies.
        when: When the duration of a Symbol sequence is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for delta alias.
        how, what, why and when to improve: N/A.
        """
        ...

    @property
    @abstractmethod
    def as_delta(self) -> datetime.timedelta:
        """
        what: Alias for the `as_period` property.
        why: To define the contract for delta alias.
        how: Abstract property, implementation varies.
        when: When the duration of a Symbol sequence is needed.
        by (caller(s)): Implementations of SymbolTimeDimProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for delta alias.
        how, what, why and when to improve: N/A.
        """
        ...


class SymbolVisualProtocol(Protocol):
    @abstractmethod
    def to_dot(self, mode: str = "tree") -> str:
        """
        what: Generates a DOT language string.
        why: To define the contract for DOT graph representation.
        how: Abstract method, implementation varies.
        when: When a DOT representation is needed.
        by (caller(s)): Implementations of SymbolVisualProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for graph definition.
        how, what, why and when to improve: N/A.
        """
        ...

    @abstractmethod
    def to_svg(self, mode: str = "tree") -> str:
        """
        what: Renders the Symbol graph to an SVG image string.
        why: To define the contract for SVG rendering.
        how: Abstract method, implementation varies.
        when: When an SVG representation is needed.
        by (caller(s)): Implementations of SymbolVisualProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for SVG rendering.
        how, what, why and when to improve: N/A.
        """
        ...

    @abstractmethod
    def to_png(self, mode: str = "tree") -> bytes:
        """
        what: Renders the Symbol graph to a PNG image as bytes.
        why: To define the contract for PNG rendering.
        how: Abstract method, implementation varies.
        when: When a PNG representation is needed.
        by (caller(s)): Implementations of SymbolVisualProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for PNG rendering.
        how, what, why and when to improve: N/A.
        """
        ...

    @abstractmethod
    def to_mmd(self, mode: str = "tree") -> str:
        """
        what: Generates a Mermaid diagram string.
        why: To define the contract for Mermaid graph representation.
        how: Abstract method, implementation varies.
        when: When a Mermaid representation is needed.
        by (caller(s)): Implementations of SymbolVisualProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for Mermaid definition.
        how, what, why and when to improve: N/A.
        """
        ...

    @abstractmethod
    def to_ascii(self, mode: str = "tree") -> str:
        """
        what: Generates an ASCII art representation.
        why: To define the contract for ASCII graph representation.
        how: Abstract method, implementation varies.
        when: When an ASCII representation is needed.
        by (caller(s)): Implementations of SymbolVisualProtocol.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for ASCII definition.
        how, what, why and when to improve: N/A.
        """
        ...


@runtime_checkable
class MixinFunction(Protocol):
    async def __call__(self, *args: Any, new_process: bool = False, new_thread: bool = True, **params: Any) -> Union[Any, Awaitable[Any]]:
        """
        what: Formal interface for mixin functions.
        why: To define the contract for mixin function execution.
        how: Abstract method, implementation varies.
        when: When a mixin function is called.
        by (caller(s)): Implementations of MixinFunction.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A blueprint for function execution.
        how, what, why and when to improve: N/A.
        """
        ...