"""
This module defines the core Symbol class and its extended functionalities.

It builds upon the foundational Symbol defined in base_symbol.py,
adding graph traversal, index, maturing, and serialization capabilities.
"""

import datetime
import enum
import orjson
import threading
import inspect
import warnings
import gc
import copy
from sys import getsizeof
from typing import Any, Union, Iterator, Optional, Literal, Set, Type, TypeVar

from .base_symbol import Symbol as BaseSymbol
from ..builtins.collections import OrderedSymbolSet
from ..builtins.index import SymbolIndex
from ..core.maturing import DefDict, deep_del, _apply_merge_strategy
from ..core.mixinability import freeze, is_frozen, get_applied_mixins

ENABLE_ORIGIN = True
MEMORY_AWARE_DELETE = True

T = TypeVar("T")


class GraphTraversal:
    def __init__(self, root: 'Symbol', mode: str = 'graph'):
        self.root = root
        self.mode = mode  # 'graph' or 'tree'
        self.visited = set()
        self.result = []

    def traverse(self):
        self._walk(self.root)
        return self.result

    def _walk(self, symbol: 'Symbol'):
        if symbol in self.visited:
            warnings.warn(f"Cycle detected in {self.mode} at {symbol}")
            return
        self.visited.add(symbol)
        self.result.append(symbol)
        neighbors = symbol.children if self.mode == 'tree' else symbol.children
        for child in neighbors:
            self._walk(child)

    def to_ascii(self) -> str:
        lines = []
        visited_ascii = set()

        def _walk_ascii(symbol: 'Symbol', indent: str = ""):
            if symbol in visited_ascii:
                return
            visited_ascii.add(symbol)
            lines.append(f"{indent}- {symbol.name}")
            for child in symbol.children:
                _walk_ascii(child, indent + "  ")

        _walk_ascii(self.root)
        return "\n".join(lines)


from ..core.lazy import SENTINEL
from .lazy_symbol import LazySymbol

class Symbol(BaseSymbol):
    __slots__ = (
        '_index',
        '_metadata',
        '_context',
        '_elevated_attributes',
    )

    def __new__(cls, name: str, origin: Optional[Any] = None):
        obj = super().__new__(cls, name, origin)
        obj._index = SENTINEL
        obj._metadata = SENTINEL
        obj._context = SENTINEL
        obj._elevated_attributes = {}
        return obj

    @property
    def index(self):
        if self._index is SENTINEL:
            self._index = SymbolIndex(self)
        return self._index

    @property
    def metadata(self):
        if self._metadata is SENTINEL:
            self._metadata = DefDict()
        return self._metadata

    @property
    def context(self):
        if self._context is SENTINEL:
            self._context = DefDict()
        return self._context

    def __getattr__(self, name: str) -> Any:
        if name in self._elevated_attributes:
            return self._elevated_attributes[name]
        # Default behavior for __getattr__ if attribute is not found
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        # If the attribute is in __slots__ (either in Symbol or BaseSymbol), set it directly
        if name in self.__slots__ or name in self.__class__.__bases__[0].__slots__:
            super().__setattr__(name, value)
        else:
            # Otherwise, store it in _elevated_attributes
            self._elevated_attributes[name] = value

    def __delattr__(self, name: str) -> None:
        if name in self.__slots__ or name in self.__class__.__bases__[0].__slots__:
            super().__delattr__(name)
        elif name in self._elevated_attributes:
            del self._elevated_attributes[name]
        else:
            super().__delattr__(name) # Raise AttributeError if not found

    def append(self, child: Union['Symbol', 'LazySymbol']) -> 'Symbol':
        # Ensure child is a Symbol or LazySymbol instance
        if not isinstance(child, (Symbol, LazySymbol)):
            child = Symbol.from_object(child)

        with self._lock:
            if child not in self.children:
                self.children.append(child)
                self._length_cache = None
            if self not in child.parents:
                child.parents.append(self)
        return self

    def add(self, child: 'Symbol') -> 'Symbol':
        # Ensure child is a Symbol instance
        if not isinstance(child, Symbol):
            child = Symbol.from_object(child)

        if child not in self.children:
            return self.append(child)
        return self

    def insert(self, child: 'Symbol', at: float = None) -> 'Symbol':
        # Ensure child is a Symbol instance
        if not isinstance(child, Symbol):
            child = Symbol.from_object(child)

        with self._lock:
            if child in self.children:
                self.children.remove(child)
            if at is None:
                at = self._write_cursor
                self._write_cursor += 1.0
            child._position = at
            self.children.append(child)
            child.parents.append(self)
            self._length_cache = len(self.children)
        return self

    def reparent(self) -> None:
        """Connects the children of the removed Symbol to its parents."""
        with self._lock:
            for parent in self.parents:
                # Remove self from parent's children
                if self in parent.children:
                    parent.children.remove(self)
                # Add self's children to parent's children
                for child in self.children:
                    if child not in parent.children:
                        parent.children.append(child)
                    # Update child's parents
                    if self in child.parents:
                        child.parents.remove(self)
                    if parent not in child.parents:
                        child.parents.append(parent)

    def rebind_linear_sequence(self) -> None:
        """Rebinds the _prev and _next pointers of adjacent symbols in the linear sequence."""
        with self._lock:
            if self._prev:
                self._prev._next = self._next
            if self._next:
                self._next._prev = self._prev
            self._prev = None
            self._next = None

    def delete(self) -> None:
        self.reparent()
        self.rebind_linear_sequence()
        if self._index is not SENTINEL:
            self.index.remove(self)

        # Sever all relationships
        for related_sym in list(self.related_to): # Iterate over a copy as list will be modified
            self.unrelate(related_sym)

        self.parents.clear()
        self.children.clear()
        with self._lock:
            if self._position in self._numbered:
                self._numbered.remove(self._position)
            if self.name in self._pool:
                del self._pool[self.name]
        if MEMORY_AWARE_DELETE:
            try:
                pass # Removed 'del self' due to potential object corruption
            except Exception:
                pass
        gc.collect()

    def pop(self) -> 'Symbol':
        """Safely removes the symbol from its hierarchy, re-parenting its children.

        Returns:
            The popped symbol.
        """
        self.delete()
        return self

    def popleft(self) -> Optional['Symbol']:
        if self.children:
            self._length_cache = None
            popped_child = self.children.pop(0)
            popped_child.delete() # Ensure full cleanup of the popped child
            return popped_child
        return None

    def graph(self):
        return GraphTraversal(self, mode='graph').traverse()

    def tree(self):
        return GraphTraversal(self, mode='tree').traverse()

    def to_mmd(self) -> str:
        lines = ["graph TD"]
        visited = set()

        def walk(sym):
            if sym in visited:
                return
            visited.add(sym)
            for c in sym.children:
                lines.append(f"    {sym.name} --> {c.name}")
                walk(c)

        walk(self)
        return "\n".join(lines)

    def to_ascii(self) -> str:
        return GraphTraversal(self, mode='tree').to_ascii()

    def patch(self, other: 'Symbol') -> 'Symbol':
        if other.origin and not self.origin:
            self.origin = other.origin
        for attr in ("children", "parents", "related_to"):
            existing = getattr(self, attr)
            new = getattr(other, attr)
            for e in new:
                if e not in existing:
                    existing.append(e)
        return self

    def relate(self, other: 'Symbol', how: str = 'related') -> 'Symbol':
        """Establishes a bidirectional relationship with another Symbol."""
        with self._lock:
            if other not in self.related_to:
                self.related_to.append(other)
                self.related_how.append(how)
            
            # Establish inverse relationship
            if self not in other.related_to:
                other.related_to.append(self)
                other.related_how.append(f"_inverse_{how}")
        return self

    def unrelate(self, other: 'Symbol', how: Optional[str] = None) -> 'Symbol':
        """Removes a bidirectional relationship with another Symbol."""
        with self._lock:
            # Remove forward relationship
            if other in self.related_to:
                idx = self.related_to.index(other)
                if how is None or self.related_how[idx] == how:
                    self.related_to.pop(idx)
                    self.related_how.pop(idx)

            # Remove inverse relationship
            if self in other.related_to:
                idx = other.related_to.index(self)
                if how is None or other.related_how[idx] == f"_inverse_{how}":
                    other.related_to.pop(idx)
                    other.related_how.pop(idx)
        return self

    @property
    def ref(self) -> Optional[Any]:
        """Alias for .origin, representing the original source or reference of the Symbol."""
        return self.origin

    @ref.setter
    def ref(self, value: Any):
        self.origin = value

    def head(self, up_to_position: float = 5.0):
        cur = self
        while cur._prev and cur._prev._position >= up_to_position:
            cur = cur._prev
        return cur

    def tail(self, from_position: float = -10.0):
        cur = self
        while cur._next and cur._next._position <= from_position:
            cur = cur._next
        return cur

    @classmethod
    def auto_date(cls) -> 'Symbol':
        iso = datetime.date.today().isoformat()
        return cls(iso)

    @classmethod
    def auto_datetime(cls) -> 'Symbol':
        iso = datetime.datetime.now().isoformat()
        return cls(iso)

    @classmethod
    def auto_time(cls) -> 'Symbol':
        iso = datetime.datetime.now().time().isoformat()
        return cls(iso)

    @classmethod
    def next(cls) -> 'Symbol':
        name = f"sym_{cls._auto_counter}"
        sym = cls(name)
        if sym not in cls._numbered:
            if cls._numbered:
                last = cls._numbered[-1]
                last._next = sym
                sym._prev = last
            cls._numbered.append(sym)
        cls._auto_counter += 1
        return sym

    @classmethod
    def prev(cls) -> Optional['Symbol']:
        if cls._auto_counter <= 0:
            return None
        cls._auto_counter -= 1
        return cls(f"sym_{cls._auto_counter}")

    @classmethod
    def first(cls) -> Optional['Symbol']:
        return cls._numbered[0] if cls._numbered else None

    @classmethod
    def last(cls) -> Optional['Symbol']:
        return cls._numbered[-1] if cls._numbered else None

    @classmethod
    def len(cls) -> int:
        return len(cls._numbered)

    @classmethod
    def from_object(cls, obj: Any) -> 'Symbol':
        """Converts an object to a Symbol, acting as a central router."""
        if isinstance(obj, Symbol):
            return obj
        if isinstance(obj, LazySymbol):
            return obj._symbol

        # Conversion functions for different types
        def from_list(value: list) -> 'Symbol':
            sym = cls('list', origin=value)
            for item in value:
                sym.append(LazySymbol(item))
            return sym

        def from_dict(value: dict) -> 'Symbol':
            sym = cls('dict', origin=value)
            for k, v in value.items():
                key_sym = LazySymbol(k)
                val_sym = LazySymbol(v)
                sym.append(key_sym)
                key_sym.append(val_sym)
            return sym

        def from_tuple(value: tuple) -> 'Symbol':
            sym = cls('tuple', origin=value)
            for item in value:
                sym.append(LazySymbol(item))
            return sym

        def from_set(value: set) -> 'Symbol':
            sym = cls('set', origin=value)
            for item in value:
                sym.append(LazySymbol(item))
            return sym
        
        type_map = {
            list: from_list,
            dict: from_dict,
            tuple: from_tuple,
            set: from_set,
            int: lambda v: cls(str(v), origin=v),
            float: lambda v: cls(str(v), origin=v),
            str: lambda v: cls(v, origin=v),
            bool: lambda v: cls(str(v), origin=v),
            type(None): lambda v: cls('None', origin=v)
        }

        # Try to find a specific from_ method
        obj_type = type(obj)
        if obj_type in type_map:
            return type_map[obj_type](obj)
        else:
            try:
                name = orjson.dumps(obj).decode()
                return cls(name, origin=obj)
            except (TypeError, orjson.JSONEncodeError):
                raise TypeError(f"Cannot convert {obj_type} to Symbol")

    @classmethod
    def seek(cls, pos: float) -> Optional['Symbol']:
        for sym in cls._numbered:
            if sym._position == pos:
                return sym
        return None

    @classmethod
    def each(cls, start: Union[int, 'Symbol', None] = None) -> Iterator['Symbol']:
        if start is None:
            idx = 0
        elif isinstance(start, int):
            idx = start
        elif isinstance(start, Symbol):
            idx = cls._numbered.index(start)
        else:
            raise TypeError(f"Invalid start parameter {repr(start)} instance of {type(start)} in each")
        for sym in cls._numbered[idx:]:
            yield sym

    def each_parents(self) -> Iterator['Symbol']:
        return iter(self.parents)

    def each_children(self) -> Iterator['Symbol']:
        return iter(self.children)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def elevate(self, merge_strategy: Literal['overwrite', 'patch', 'copy', 'deepcopy', 'pipe', 'update', 'extend', 'smooth'] = 'smooth') -> Set[str]:
        """Elevates metadata entries to instance attributes/methods based on a merge strategy."""
        if is_frozen():
            warnings.warn(f"Cannot elevate on frozen Symbol {self.name}")
            return set()

        elevated_keys = set()
        keys_to_remove = []

        for key, value in list(self.metadata.items()): # Iterate over a copy to allow modification
            if hasattr(self, key) and key not in self.__slots__ and key not in self.__class__.__bases__[0].__slots__:
                # This means it's an existing attribute not in slots, likely from a mixin or dynamic assignment
                current_value = getattr(self, key)
                if key.startswith('__') or inspect.ismethod(current_value) or inspect.isfunction(current_value):
                    warnings.warn(f"Overwriting internal attribute/method '{key}' on Symbol {self.name}")
                merged_value = _apply_merge_strategy(current_value, value, merge_strategy)
                setattr(self, key, merged_value)
            elif key in self.__slots__ or key in self.__class__.__bases__[0].__slots__:
                # Attribute is part of __slots__, directly set it
                current_value = getattr(self, key)
                if key.startswith('__') or inspect.ismethod(current_value) or inspect.isfunction(current_value):
                    warnings.warn(f"Overwriting internal attribute/method '{key}' on Symbol {self.name}")
                merged_value = _apply_merge_strategy(current_value, value, merge_strategy)
                setattr(self, key, merged_value)
            else:
                # Dynamically add to _elevated_attributes
                self._elevated_attributes[key] = value
            elevated_keys.add(key)
            keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.metadata[key]

        return elevated_keys

    def slim(self, protected_attributes: Optional[Set[str]] = None) -> None:
        """Removes dynamically applied attributes/methods that are not explicitly protected."""
        if is_frozen():
            warnings.warn(f"Cannot slim on frozen Symbol {self.name}")
            return

        if protected_attributes is None:
            protected_attributes = set()

        applied_mixins = get_applied_mixins()
        for attr_name in list(applied_mixins.keys()): # Iterate over a copy
            if attr_name not in protected_attributes:
                # Check if the attribute is in _elevated_attributes and remove it
                if attr_name in self._elevated_attributes:
                    del self._elevated_attributes[attr_name]
                # If it's a slot attribute and was set to SENTINEL, deep_del it
                elif hasattr(self, attr_name) and getattr(self, attr_name) is SENTINEL:
                    deep_del(self, attr_name)

        gc.collect() # Explicitly call garbage collector after deletions

    def immute(self, merge_strategy: Literal['overwrite', 'patch', 'copy', 'deepcopy', 'pipe', 'update', 'extend', 'smooth'] = 'smooth') -> None:
        """Orchestrates the maturing process: elevates metadata, slims down, and freezes the Symbol."""
        if is_frozen():
            warnings.warn(f"Symbol {self.name} is already frozen. No action taken.")
            return

        # 1. Elevate metadata
        elevated_keys = self.elevate(merge_strategy=merge_strategy)

        # 2. Slim down
        self.slim(protected_attributes=elevated_keys)

        # 3. Freeze the Symbol class (global state)
        freeze()

    def clear_context(self) -> None:
        """Clears the context DefDict, performing memory-aware deletion of its contents."""
        if is_frozen():
            warnings.warn(f"Cannot clear context on frozen Symbol {self.name}")
            return

        # Iterate over a copy of keys to allow modification during iteration
        for key in list(self.context.keys()):
            # DefDict's __delitem__ will handle logging and potential deep_del for nested DefDicts
            del self.context[key]
        gc.collect() # Explicitly call garbage collector after deletions

    def to(self, target_type: Type[T]) -> T:
        """Converts the Symbol to an object of the specified type."""
        try:
            return orjson.loads(self.name)
        except orjson.JSONDecodeError:
            raise TypeError(f"Cannot convert Symbol '{self.name}' to {target_type}")

    def footprint(self, visited: Optional[Set['Symbol']] = None) -> int:
        """Calculates the memory footprint of the symbol and its descendants in bytes."""
        if visited is None:
            visited = set()

        if self in visited:
            return 0

        visited.add(self)

        size = getsizeof(self)
        for child in self.children:
            size += child.footprint(visited)

        # Add the size of the index and metadata
        if self._index is not SENTINEL:
            size += getsizeof(self._index)
        if self._metadata is not SENTINEL:
            size += getsizeof(self._metadata)

        return size


def to_sym(obj: Any) -> 'Symbol':
    """Converts an object to a Symbol."""
    return Symbol.from_object(obj)


class SymbolNamespace:
    """Provides a convenient way to create Symbol instances via attribute access."""
    def __getattr__(self, name):
        return Symbol(name)

    def __getitem__(self, name):
        return Symbol(name)

    def __setitem__(self, name, value):
        raise TypeError(f"SymbolNamespace is read-only, cannot set {name} to {value}")

    def __setattr__(self, name, value):
        raise TypeError(f"SymbolNamespace is read-only, cannot set {name} to {value}")

s = SymbolNamespace()
