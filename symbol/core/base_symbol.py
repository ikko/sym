"""This module defines the foundational Symbol class and its core instantiation logic.

It serves as a base for the more extensive Symbol functionality defined elsewhere,
specifically designed to prevent circular import dependencies.
"""
import threading
from typing import Optional, Union, Callable, Any, TypeVar
from weakref import WeakValueDictionary

from ..builtins.avl_tree import AVLTree

T = TypeVar("T")

class Symbol:
    __slots__ = (
        'name',
        'origin',
        'parents',
        'children',
        'related_to',
        'related_how',
        '_position',
        '_next',
        '_prev',
        '_length_cache',
        '__weakref__',
        'node_shape',
    )

    _pool: WeakValueDictionary[str, 'Symbol'] = WeakValueDictionary()
    _numbered: AVLTree = AVLTree()
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
            obj.origin = origin
            obj.parents = []
            obj.children = []
            obj.related_to = []
            obj.related_how = []
            obj._position = cls._write_cursor
            obj._next = None
            obj._prev = None
            obj._length_cache = None
            obj.node_shape = None # Initialize node_shape
            cls._write_cursor += 1.0
            cls._pool[name] = obj
            cls._numbered.root = cls._numbered.insert(cls._numbered.root, obj, obj._position) # Insert into AVLTree
            return obj

    def __repr__(self):
        return f"Symbol('{self.name}')"

    def __str__(self):
        return self.name

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    # Basic comparison for numbered symbs, more complex logic in symb.py
    def __lt__(self, other):
        # Check if both symbs are in the numbered tree by searching for their positions
        if isinstance(other, Symbol) and \
           self._numbered.search(self._position) is not None and \
           other._numbered.search(other._position) is not None:
            return self._position < other._position
        raise TypeError("Unordered comparison not supported for non-numbered symbs")

    # Basic JSON serialization, more complex logic in symb.py
    def __orjson__(self):
        return self.name

def _to_symb(x: Any) -> 'Symbol':
    """Converts an object to a Symbol instance."""
    if isinstance(x, Symbol):
        return x
    elif isinstance(x, str):
        return Symbol(x)
    elif hasattr(x, 'name'):
        return Symbol(x.name)
    raise TypeError(f"Cannot convert {repr(x)} instance of {type(x)} to Symbol")


