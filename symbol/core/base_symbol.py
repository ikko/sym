"""This module defines the foundational Symbol class and its core instantiation logic.

It serves as a base for the more extensive Symbol functionality defined elsewhere,
specifically designed to prevent circular import dependencies.
"""
import threading
from typing import Any, Optional, TypeVar

T = TypeVar("T")

class Symbol:
    _pool: dict[str, 'Symbol'] = {}
    _numbered: list['Symbol'] = []
    _auto_counter: int = 0
    _read_cursor: float = 0.0
    _write_cursor: float = 0.0
    _lock = threading.RLock()

    def __new__(cls, name: str, origin: Optional[Any] = None):
        with cls._lock:
            if not isinstance(name, str):
                raise TypeError("Symbol name must be a string")
            if name in cls._pool:
                return cls._pool[name]
            obj = super().__new__(cls)
            obj.name = name
            obj.origin = origin # ENABLE_ORIGIN will be handled by symbol.py
            obj.parents: list['Symbol'] = []
            obj.children: list['Symbol'] = []
            obj.related_to: list['Symbol'] = []
            obj.related_how: list[str] = []
            obj._position: float = cls._write_cursor
            obj._next: Optional['Symbol'] = None
            obj._prev: Optional['Symbol'] = None
            # Index and metadata will be added by symbol.py
            obj._length_cache: Optional[int] = None
            cls._write_cursor += 1.0
            cls._pool[name] = obj
            cls._numbered.append(obj) # Add the new symbol to the _numbered list
            return obj

    def __repr__(self):
        return f"Symbol('{self.name}')"

    def __str__(self):
        return self.name

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    # Basic comparison for numbered symbols, more complex logic in symbol.py
    def __lt__(self, other):
        if self in self._numbered and other in self._numbered:
            return self._position < other._position
        raise TypeError("Unordered comparison not supported for non-numbered symbols")

    # Basic JSON serialization, more complex logic in symbol.py
    def __orjson__(self):
        return self.name

def _to_symbol(x: Any) -> 'Symbol':
    """Converts an object to a Symbol instance."""
    if isinstance(x, Symbol):
        return x
    elif isinstance(x, str):
        return Symbol(x)
    elif hasattr(x, 'name'):
        return Symbol(x.name)
    raise TypeError(f"Cannot convert {repr(x)} instance of {type(x)} to Symbol")


