"""
This module defines the core Symbol class and its extended functionalities.

It builds upon the foundational Symbol defined in base_symbol.py,
adding graph traversal, index, maturing, and serialization capabilities.
"""

import pendulum
import enum
import orjson
import threading
import inspect
import warnings
import gc
import copy
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


class Symbol(BaseSymbol):
    def __new__(cls, name: str, origin: Optional[Any] = None):
        obj = super().__new__(cls, name, origin)
        if not hasattr(obj, 'index'): # Initialize only if not already initialized by BaseSymbol
            obj.index = SymbolIndex(obj)
            obj.metadata = DefDict()
            obj.context = DefDict()
        if ENABLE_ORIGIN:
            obj.origin = origin
        return obj

    def append(self, child: 'Symbol') -> 'Symbol':
        # Ensure child is a Symbol instance
        if not isinstance(child, Symbol):
            child = Symbol.from_object(child)

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

    def delete(self) -> None:
        for p in self.parents:
            if self in p.children:
                p.children.remove(self)
        for c in self.children:
            if self in c.parents:
                c.parents.remove(self)
        self.parents.clear()
        self.children.clear()
        if self in self._numbered:
            self._numbered.remove(self)
        with self._lock:
            if self.name in self._pool:
                del self._pool[self.name]
        if MEMORY_AWARE_DELETE:
            try:
                pass # Removed 'del self' due to potential object corruption
            except Exception:
                pass

    def pop(self) -> Optional['Symbol']:
        if self.children:
            self._length_cache = None
            return self.children.pop()
        return None

    def popleft(self) -> Optional['Symbol']:
        if self.children:
            self._length_cache = None
            return self.children.pop(0)
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
        iso = pendulum.today().to_iso8601_string()
        return cls(iso)

    @classmethod
    def auto_datetime(cls) -> 'Symbol':
        iso = pendulum.now().to_iso8601_string()
        return cls(iso)

    @classmethod
    def auto_time(cls) -> 'Symbol':
        iso = pendulum.now().time().to_iso8601_string()
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
    def from_enum(cls, enum_cls: enum.EnumMeta) -> list['Symbol']:
        return [cls(member.name) for member in enum_cls]

    @classmethod
    def from_int(cls, value: int) -> 'Symbol':
        return cls(str(value), origin=value)

    @classmethod
    def from_float(cls, value: float) -> 'Symbol':
        return cls(str(value), origin=value)

    @classmethod
    def from_str(cls, value: str) -> 'Symbol':
        return cls(value, origin=value)

    @classmethod
    def from_bool(cls, value: bool) -> 'Symbol':
        return cls(str(value), origin=value)

    @classmethod
    def from_none(cls, value: None) -> 'Symbol':
        return cls('None', origin=value)

    @classmethod
    def from_list(cls, value: list) -> 'Symbol':
        sym = cls('list', origin=copy.deepcopy(value))
        for item in value:
            sym.append(Symbol.from_object(item))
        return sym

    @classmethod
    def from_dict(cls, value: dict) -> 'Symbol':
        sym = cls('dict', origin=copy.deepcopy(value))
        for k, v in value.items():
            key_sym = Symbol.from_object(k)
            val_sym = Symbol.from_object(v)
            sym.append(key_sym)
            key_sym.append(val_sym)
        return sym

    @classmethod
    def from_tuple(cls, value: tuple) -> 'Symbol':
        sym = cls('tuple', origin=copy.deepcopy(value))
        for item in value:
            sym.append(Symbol.from_object(item))
        return sym

    @classmethod
    def from_set(cls, value: set) -> 'Symbol':
        sym = cls('set', origin=copy.deepcopy(value))
        for item in value:
            sym.append(Symbol.from_object(item))
        return sym

    @classmethod
    def from_object(cls, obj: Any) -> 'Symbol':
        """Converts an object to a Symbol, acting as a central router."""
        if isinstance(obj, Symbol):
            return obj

        # Try to find a specific from_ method
        type_name = type(obj).__name__
        factory_method_name = f"from_{type_name}"
        factory_method = getattr(cls, factory_method_name, None)

        if factory_method:
            return factory_method(obj)
        elif obj is None:
            return cls('None', origin=None)
        elif isinstance(obj, (int, float, str, bool)):
            return cls(str(obj), origin=obj)
        else:
            try:
                name = orjson.dumps(obj).decode()
                return cls(name, origin=obj)
            except (TypeError, orjson.JSONEncodeError):
                raise TypeError(f"Cannot convert {type(obj)} to Symbol")

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
            if hasattr(self, key):
                current_value = getattr(self, key)
                # Check if it's an internal method/attribute
                if key.startswith('__') or inspect.ismethod(current_value) or inspect.isfunction(current_value):
                    warnings.warn(f"Overwriting internal attribute/method '{key}' on Symbol {self.name}")

                merged_value = _apply_merge_strategy(current_value, value, merge_strategy)
                setattr(self, key, merged_value)
                elevated_keys.add(key)
                keys_to_remove.append(key)
            else:
                setattr(self, key, value)
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
                # Check if the attribute actually exists on this instance before attempting to delete
                if hasattr(self, attr_name):
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
