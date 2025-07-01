import datetime
import enum
import orjson
import threading
import inspect
import warnings
import gc
from typing import Any, Union, Iterator, Optional, Literal, Set

from ..core.graph import GraphTraversal
from ..builtins.collections import OrderedSymbolSet
from ..builtins.indexing import SymbolIndex
from ..core.maturing import DefDict, deep_del, _apply_merge_strategy
from ..core.pluggability import freeze, is_frozen, get_applied_patches

ENABLE_ORIGIN = True
MEMORY_AWARE_DELETE = True


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
            obj.origin = origin if ENABLE_ORIGIN else None
            obj.parents: list['Symbol'] = []
            obj.children: list['Symbol'] = []
            obj.related_to: list['Symbol'] = []
            obj.related_how: list[str] = []
            obj._position: float = cls._write_cursor
            obj._next: Optional['Symbol'] = None
            obj._prev: Optional['Symbol'] = None
            obj.index = SymbolIndex(obj)
            obj._length_cache: Optional[int] = None
            obj.metadata = DefDict() # Initialize metadata as DefDict
            obj.context = DefDict() # Initialize context as DefDict
            cls._write_cursor += 1.0
            cls._pool[name] = obj
            return obj

    def __repr__(self):
        return f" :{self.name}"

    def __str__(self):
        return self.name

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __lt__(self, other):
        if self in self._numbered and other in self._numbered:
            return self._position < other._position
        raise TypeError("Unordered comparison not supported for non-numbered symbols")

    def __add__(self, other: 'Symbol') -> OrderedSymbolSet:
        return OrderedSymbolSet([self, other])

    def __orjson__(self):
        return self.name

    def append(self, child: 'Symbol') -> 'Symbol':
        child = _to_symbol(child)
        if child not in self.children:
            self.children.append(child)
            child.parents.append(self)
            self._length_cache = None
        return self

    def add(self, child: 'Symbol') -> 'Symbol':
        if child not in self.children:
            return self.append(child)
        return self

    def insert(self, child: 'Symbol', at: float = None) -> 'Symbol':
        child = _to_symbol(child)
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
                del self
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
    def from_enum(cls, enum_cls: enum.EnumMeta) -> list['Symbol']:
        return [cls(member.name) for member in enum_cls]

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
        for sym in cls._numbered[idx:]:n            yield sym

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

        applied_patches = get_applied_patches()
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


def _to_symbol(x: Any) -> 'Symbol':
    if isinstance(x, Symbol):
        return x
    elif isinstance(x, str):
        return Symbol(x)
    elif hasattr(x, 'name'):
        return Symbol(x.name)
    raise TypeError(f"Cannot convert {repr(x)} instance of {type(x)} to Symbol")


class SymbolNamespace:
    def __getattr__(self, name):
        return Symbol(name)

    def __getitem__(self, name):
        return Symbol(name)

    def __setitem__(self, name, value):
        raise TypeError(f"SymbolNamespace is read-only, cannot set {name} to {value}")

s = SymbolNamespace()
