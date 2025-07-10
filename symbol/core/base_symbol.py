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
        """
        what: Creates a new Symbol instance.
        why: To ensure proper initialization and uniqueness of Symbols.
        how: Checks for existing Symbol in pool, initializes attributes, inserts into AVLTree.
        when: Upon Symbol instantiation.
        by (caller(s)): Direct Symbol() calls, from_object.
        how often: Frequently.
        how much: Minimal.
        what is it like: Minting a unique identifier.
        how, what, why and when to improve: Optimize pool lookup for very large numbers of Symbols.
        """
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
        """
        what: Returns a developer-friendly string representation.
        why: For debugging and introspection.
        how: Formats the Symbol's name.
        when: When Symbol is printed in a debugger or console.
        by (caller(s)): Python's `repr()` function.
        how often: Frequently.
        how much: Minimal.
        what is it like: A technical label.
        how, what, why and when to improve: Include more internal state for complex debugging.
        """
        return f"Symbol('{self.name}')"

    def __str__(self):
        """
        what: Returns a user-friendly string representation.
        why: For display to end-users.
        how: Returns the Symbol's name.
        when: When Symbol is converted to a string.
        by (caller(s)): Python's `str()` function, print statements.
        how often: Frequently.
        how much: Minimal.
        what is it like: A simple label.
        how, what, why and when to improve: N/A.
        """
        return self.name

    def __eq__(self, other: Any) -> bool:
        """
        what: Compares two Symbol instances for equality.
        why: To determine if two Symbols represent the same entity.
        how: Compares based on their `name` attribute.
        when: When comparing Symbols.
        by (caller(s)): Python's equality operator (`==`).
        how often: Frequently.
        how much: Minimal.
        what is it like: Checking if two IDs are the same.
        how, what, why and when to improve: Consider more complex equality criteria.
        """
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self) -> int:
        """
        what: Computes the hash value for a Symbol.
        why: To allow Symbols to be used in hash-based collections (sets, dicts).
        how: Hashes based on the Symbol's `name`.
        when: When Symbol is added to a set or used as a dictionary key.
        by (caller(s)): Python's `hash()` function.
        how often: Frequently.
        how much: Minimal.
        what is it like: Generating a unique fingerprint.
        how, what, why and when to improve: N/A.
        """
        return hash(self.name)

    # Basic comparison for numbered symbols, more complex logic in symbol.py
    def __lt__(self, other):
        """
        what: Compares two Symbols for less than.
        why: To enable ordering of numbered Symbols.
        how: Compares based on their `_position` attribute.
        when: When sorting or comparing numbered Symbols.
        by (caller(s)): Python's less than operator (`<`).
        how often: Infrequently.
        how much: Minimal.
        what is it like: Ordering items by sequence number.
        how, what, why and when to improve: N/A.
        """
        # Check if both symbols are in the numbered tree by searching for their positions
        if isinstance(other, Symbol) and \
           self._numbered.search(self._position) is not None and \
           other._numbered.search(other._position) is not None:
            return self._position < other._position
        raise TypeError("Unordered comparison not supported for non-numbered symbols")

    # Basic JSON serialization, more complex logic in symbol.py
    def __orjson__(self):
        """
        what: Provides a custom serialization for orjson.
        why: To control how Symbols are serialized to JSON.
        how: Returns the Symbol's name.
        when: When using `orjson.dumps` on a Symbol.
        by (caller(s)): orjson library.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Custom JSON representation.
        how, what, why and when to improve: More complex serialization if needed.
        """
        return self.name

def _to_symbol(x: Any) -> 'Symbol':
    """
    what: Converts an object to a Symbol instance.
    why: To provide a utility for type conversion.
    how: Handles existing Symbols, strings, and objects with a `name` attribute.
    when: When an object needs to be represented as a Symbol.
    by (caller(s)): Internal Symbol operations.
    how often: Frequently.
    how much: Minimal.
    what is it like: Adapting an object to a specific type.
    how, what, why and when to improve: Handle more object types.
    """
    if isinstance(x, Symbol):
        return x
    elif isinstance(x, str):
        return Symbol(x)
    elif hasattr(x, 'name'):
        return Symbol(x.name)
    raise TypeError(f"Cannot convert {repr(x)} instance of {type(x)} to Symbol")


