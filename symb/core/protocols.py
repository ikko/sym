"""This module defines the protocols that govern the behavior of Symbol objects.

These protocols establish a clear contract for extending the Symbol class with new functionality,
promoting a clean and maintainable architecture.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Iterator, List, Optional, Protocol, Union, Callable, Awaitable, runtime_checkable
import datetime



class SymbolPathProtocol(Protocol):
    @abstractmethod
    def path_to(self, target: 'Symbol') -> List['Symbol']:

        """Finds a path from this Symbol to a target Symbol."""
        ...

    @abstractmethod
    def match(self, predicate: Callable[[Symbol], bool], traversal: str = 'dfs') -> Iterator[Symbol]:
        """Finds Symbols matching a predicate using specified traversal."""
        ...


class SymbolTimeDimProtocol(Protocol):
    @property
    @abstractmethod
    def head(self) -> Any:
        """Returns a view of Symbols sorted chronologically (earliest first)."""
        ...

    @property
    @abstractmethod
    def tail(self) -> Any:
        """Returns a view of Symbols sorted in reverse chronological order (latest first)."""
        ...

    @property
    @abstractmethod
    def as_date(self) -> datetime.date:
        """Returns the date part of the Symbol's name as a date object."""
        ...

    @property
    @abstractmethod
    def as_time(self) -> datetime.time:
        """Returns the time part of the Symbol's name as a time object."""
        ...

    @property
    @abstractmethod
    def as_datetime(self) -> datetime.datetime:
        """Returns the full datetime object parsed from the Symbol's name."""
        ...

    @property
    @abstractmethod
    def day(self) -> int:
        """Returns the day component of the Symbol's datetime."""
        ...

    @property
    @abstractmethod
    def hour(self) -> int:
        """Returns the hour component of the Symbol's datetime."""
        ...

    @property
    @abstractmethod
    def minute(self) -> int:
        """Returns the minute component of the Symbol's datetime."""
        ...

    @property
    @abstractmethod
    def second(self) -> int:
        """Returns the second component of the Symbol's datetime."""
        ...

    @property
    @abstractmethod
    def period(self) -> datetime.timedelta:
        """Returns the time duration between the first and last Symbols in a sorted view."""
        ...

    @property
    @abstractmethod
    def as_period(self) -> datetime.timedelta:
        """Alias for the `period` property, returning the time duration."""
        ...

    @property
    @abstractmethod
    def duration(self) -> datetime.timedelta:
        """Alias for the `period` property, returning the time duration."""
        ...

    @property
    @abstractmethod
    def as_duration(self) -> datetime.timedelta:
        """Alias for the `as_period` property, returning the time duration."""
        ...

    @property
    @abstractmethod
    def delta(self) -> datetime.timedelta:
        """Alias for the `period` property, returning the time duration."""
        ...

    @property
    @abstractmethod
    def as_delta(self) -> datetime.timedelta:
        """Alias for the `as_period` property, returning the time duration."""
        ...


class SymbolVisualProtocol(Protocol):
    @abstractmethod
    def to_dot(self, mode: str = "tree") -> str:
        """Generates a DOT language string representation of the Symbol graph."""
        ...

    @abstractmethod
    def to_svg(self, mode: str = "tree") -> str:
        """Renders the Symbol graph to an SVG image string."""
        ...

    @abstractmethod
    def to_png(self, mode: str = "tree") -> bytes:
        """Renders the Symbol graph to a PNG image as bytes."""
        ...

    @abstractmethod
    def to_mmd(self, mode: str = "tree") -> str:
        """Generates a Mermaid diagram string representation of the Symbol graph."""
        ...

    @abstractmethod
    def to_ascii(self, mode: str = "tree") -> str:
        """Generates an ASCII art representation of the Symbol graph."""
        ...


@runtime_checkable
class MixinFunction(Protocol):
    async def __call__(self, *args: Any, new_process: bool = False, new_thread: bool = True, **params: Any) -> Union[Any, Awaitable[Any]]:
        """Formal interface for mixin functions, supporting async, process/thread execution, and return type casting."""
        ...