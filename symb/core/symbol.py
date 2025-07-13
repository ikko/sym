import datetime
import inspect
import warnings
from typing import Any, Iterator, Literal, Optional, Set, Type, Union
from weakref import WeakValueDictionary

import orjson
import toml
import yaml

from builtin.index import SymbolIndex
from core.lazy import SENTINEL
from core.lazy_symb import LazySymbol
from core.maturing import _apply_merge_strategy, deep_del, DefDict
from builtin.avl_tree import AVLTree

from .base_symb import BaseSymbol
from .mixinability import apply_mixin_to_instance, freeze, is_frozen
from .relations import Relations
from .graph_traversal import GraphTraversal
from .type_var_t import T

MEMORY_AWARE_DELETE = True


class Symbol(BaseSymbol):
    _pool: WeakValueDictionary[str, 'Symbol'] = WeakValueDictionary() # Override BaseSymbol's pool
    _numbered: AVLTree = AVLTree() # Override BaseSymbol's numbered tree

    def __repr__(self):
        return f"Symbol('{self.name}')"
    __slots__ = (
        '_index',
        '_metadata',
        '_context',
        '_elevated_attributes',
        '_relations', # New slot for lazy relations
    )

    def __new__(cls, name: str, origin: Optional[Any] = None):
        with cls._lock:
            if not isinstance(name, str):
                raise TypeError("Symbol name must be a string")

            # Check if an object with this name already exists in the pool
            if name in cls._pool:
                existing_obj = cls._pool[name]
                # If the existing object is already an instance of the current class (Symbol or its subclass),
                # return it directly.
                if isinstance(existing_obj, cls):
                    return existing_obj
                # If the existing object is a BaseSymbol (but not a Symbol),
                # we need to "upgrade" it to a Symbol.
                elif isinstance(existing_obj, BaseSymbol):
                    # Create a new instance of the current class (Symbol) using object.__new__
                    # to bypass any custom __new__ in the hierarchy.
                    obj = object.__new__(cls)
                    # Copy attributes from the existing BaseSymbol to the new Symbol instance.
                    # This ensures that properties like name, parents, children, etc., are preserved.
                    for attr in existing_obj.__slots__:
                        if hasattr(existing_obj, attr):
                            object.__setattr__(obj, attr, getattr(existing_obj, attr))
                    
                    # Initialize Symbol-specific attributes on the newly created Symbol instance.
                    # These are attributes that are part of Symbol's __slots__ but not BaseSymbol's.
                    object.__setattr__(obj, '_elevated_attributes', {})
                    object.__setattr__(obj, '_index', SENTINEL)
                    object.__setattr__(obj, '_metadata', SENTINEL)
                    object.__setattr__(obj, '_context', SENTINEL)
                    object.__setattr__(obj, '_relations', SENTINEL) # Lazy relations initialization
                    
                    # Set the origin if it's not already set.
                    if origin is None and obj.origin is None:
                        object.__setattr__(obj, 'origin', f"{cls.__module__}.{cls.__name__}")
                    
                    # Update the pool to store the new Symbol instance instead of the old BaseSymbol.
                    cls._pool[name] = obj
                    return obj
            
            # If no object with this name exists in the pool, create a brand new Symbol instance.
            obj = object.__new__(cls)
            
            # Initialize BaseSymbol-specific attributes directly.
            object.__setattr__(obj, 'name', name)
            object.__setattr__(obj, 'origin', origin)
            object.__setattr__(obj, 'parents', [])
            object.__setattr__(obj, 'children', [])
            
            # Initialize attributes related to positioning and linked list structure.
            object.__setattr__(obj, '_position', cls._write_cursor)
            object.__setattr__(obj, '_next', None)
            object.__setattr__(obj, '_prev', None)
            object.__setattr__(obj, '_length_cache', None)
            object.__setattr__(obj, 'node_shape', None)
            cls._write_cursor += 1.0
            
            # Initialize Symbol-specific attributes.
            object.__setattr__(obj, '_elevated_attributes', {})
            object.__setattr__(obj, '_index', SENTINEL)
            object.__setattr__(obj, '_metadata', SENTINEL)
            object.__setattr__(obj, '_context', SENTINEL)
            object.__setattr__(obj, '_relations', SENTINEL) # Lazy relations initialization
            
            # Set the origin if it's not already set.
            if origin is None and obj.origin is None:
                object.__setattr__(obj, 'origin', f"{cls.__module__}.{cls.__name__}")
            
            # Add the newly created Symbol instance to the global pool and numbered tree.
            cls._pool[name] = obj
            cls._numbered.root = cls._numbered.insert(cls._numbered.root, obj, obj._position)

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

    @property
    def relations(self):
        if self._relations is SENTINEL:
            object.__setattr__(self, '_relations', Relations(self))
        return self._relations

    def __getattr__(self, name: str) -> Any:
        if name in self._elevated_attributes:
            return self._elevated_attributes[name]
        try:
            # Try to get the attribute from the base class (which checks __slots__)
            return super().__getattr__(name)
        except AttributeError:
            # If not found in base class or _elevated_attributes, delegate to relations
            return getattr(self.relations, name) # This will now call the property

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
        return child

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
        """Rebinds the _prev and _next pointers of adjacent symbs in the linear sequence."""
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

    def pop(self) -> 'Symbol':
        """Safely removes the symb from its hierarchy, re-parenting its children.

        Returns:
            The popped symb.
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
        return GraphTraversal(self, graph_mode='dfs').traverse()

    def tree(self):
        return GraphTraversal(self, mode='tree').traverse()

    def to_mmd(self, mode: str = "tree") -> str:
        lines = ["graph LR"]
        visited_nodes = set()
        visited_edges = set()

        def get_node_id(sym: 'Symbol') -> str:
            return sym.name.replace(" ", "_")

        def get_node_declaration(sym: 'Symbol') -> str:
            node_id = get_node_id(sym)
            if sym.node_shape == "round":
                return f"{node_id}({sym.name})"
            elif sym.node_shape == "stadium":
                return f"{node_id}([{sym.name}])"
            elif sym.node_shape == "subroutine":
                return f"{node_id}[{sym.name}]"
            elif sym.node_shape == "cylindrical":
                return f"{node_id}[({sym.name})]"
            elif sym.node_shape == "circle":
                return f"{node_id}(({sym.name}))"
            elif sym.node_shape == "asymmetric":
                return f"{node_id}> {sym.name}]"
            elif sym.node_shape == "rhombus":
                return f"{node_id}{{{sym.name}}}"
            elif sym.node_shape == "hexagon":
                return f"{node_id}{{{{ {sym.name} }}}}"
            elif sym.node_shape == "parallelogram":
                return f"{node_id}[/{sym.name}/]"
            elif sym.node_shape == "parallelogram_alt":
                return f"{node_id}[\\{sym.name}\\]"
            elif sym.node_shape == "trapezoid":
                return f"{node_id}[/{sym.name}\\]"
            elif sym.node_shape == "trapezoid_alt":
                return f"{node_id}[\\{sym.name}/]"
            elif sym.node_shape == "double_circle":
                return f"{node_id}(({sym.name}))"
            else:
                return f"{node_id}[{sym.name}]"

        def walk(sym: 'Symbol'):
            if sym in visited_nodes:
                return
            visited_nodes.add(sym)

            for child in sym.children:
                edge = (sym, child, "-->", "")
                if edge not in visited_edges:
                    lines.append(f"    {get_node_id(sym)} --> {get_node_id(child)}")
                    visited_edges.add(edge)
                walk(child)

            for how, related_syms in sym.relations.items():
                if not how.startswith("_inverse_"):
                    for related_sym in related_syms:
                        edge = (sym, related_sym, "--", how)
                        if edge not in visited_edges:
                            lines.append(f"    {get_node_id(sym)} -- {how} --> {get_node_id(related_sym)}")
                            visited_edges.add(edge)
                        walk(related_sym)

        walk(self)

        node_declarations = set()
        for sym in visited_nodes:
            node_declarations.add(get_node_declaration(sym))

        final_lines = ["graph LR"]
        final_lines.extend(sorted(list(node_declarations)))
        final_lines.extend(lines[1:])

        return "\n".join(final_lines)

    def to_ascii(self, traverse_mode: Literal["dfs", "bfs"] = "dfs",
                 family_mode: Literal["children_first", "parents_first"] = "children_first",
                 graph_mode: Literal["dfs", "bfs"] = "dfs") -> str:
        """
         what: Generates an ASCII art representation of the Symbol.
         why: To visualize the Symbol's structure in text.
         how: Delegates to `GraphTraversal.to_ascii`.
         when: When a text-based visualization is requested.
         by caller: External tools, debugging.
         how often: Infrequently.
         how much: Depends on graph size.
         it is like: Drawing a text-based diagram.
         improve: N/A.
         """
        return GraphTraversal(self, traverse_mode=traverse_mode, family_mode=family_mode, graph_mode=graph_mode).to_ascii()

    def to_yaml(self) -> str:
        """
        Serializes the Symbol graph to a YAML string.
        """
        nodes_data = []
        # Collect all symbols from the pool
        all_symbols = list(Symbol._pool.values())

        # Sort symbols by name for consistent output
        all_symbols.sort(key=lambda s: s.name)

        for sym in all_symbols:
            node_info = {
                "name": sym.name,
                "children": sorted([child.name for child in sym.children]), # Sort children for consistent output
                "relations": {how: sorted([related_sym.name for related_sym in related_syms])
                              for how, related_syms in sym.relations.items() if not how.startswith('_inverse_')}
            }
            nodes_data.append(node_info)

        return yaml.dump(nodes_data, sort_keys=False, default_flow_style=False)

    @classmethod
    def from_yaml(cls, yaml_string: str) -> 'Symbol':
        """
        Reconstructs a Symbol graph from a YAML string.
        """
        loaded_data = yaml.safe_load(yaml_string)

        # First pass: Create all Symbol instances
        symbols = {} # type: ignore
        for node_data in loaded_data:
            name = node_data["name"]
            symbols[name] = cls(name)

        # Second pass: Establish children and relations
        for node_data in loaded_data:
            name = node_data["name"]
            current_sym = symbols[name]

            for child_name in node_data.get("children", []):
                child_sym = symbols.get(child_name)
                if child_sym:
                    current_sym.append(child_sym)

            for how, related_names in node_data.get("relations", {}).items():
                for related_name in related_names:
                    related_sym = symbols.get(related_name)
                    if related_sym:
                        current_sym.relate(related_sym, how=how)

        # Determine root symbols (those with no parents among the parsed symbols)
        all_symbols = set(symbols.values())
        child_symbols = set()
        for sym in all_symbols:
            for child in sym.children:
                if child in all_symbols:
                    child_symbols.add(child)
            for how, related_syms in sym.relations.items():
                if not how.startswith('_inverse_'):
                    for related_sym in related_syms:
                        if related_sym in all_symbols:
                            child_symbols.add(related_sym)

        root_symbols = [sym for sym in all_symbols if sym not in child_symbols]

        if not root_symbols:
            if all_symbols:
                return next(iter(all_symbols))
            else:
                raise ValueError("No symbols found in the YAML string.")

        return root_symbols[0]

    def to_json(self) -> str:
        """
        Serializes the Symbol graph to a JSON string using orjson.
        """
        nodes_data = []
        all_symbols = list(Symbol._pool.values())
        all_symbols.sort(key=lambda s: s.name)

        for sym in all_symbols:
            node_info = {
                "name": sym.name,
                "children": sorted([child.name for child in sym.children]),
                "relations": {how: sorted([related_sym.name for related_sym in related_syms])
                              for how, related_syms in sym.relations.items() if not how.startswith('_inverse_')}
            }
            nodes_data.append(node_info)

        return orjson.dumps(nodes_data, option=orjson.OPT_INDENT_2).decode("utf-8")

    @classmethod
    def from_json(cls, json_string: str) -> 'Symbol':
        """
        Reconstructs a Symbol graph from a JSON string using orjson.
        """
        loaded_data = orjson.loads(json_string)

        symbols = {} # type: ignore
        for node_data in loaded_data:
            name = node_data["name"]
            symbols[name] = cls(name)

        for node_data in loaded_data:
            name = node_data["name"]
            current_sym = symbols[name]

            for child_name in node_data.get("children", []):
                child_sym = symbols.get(child_name)
                if child_sym:
                    current_sym.append(child_sym)

            for how, related_names in node_data.get("relations", {}).items():
                for related_name in related_names:
                    related_sym = symbols.get(related_name)
                    if related_sym:
                        current_sym.relate(related_sym, how=how)

        all_symbols = set(symbols.values())
        child_symbols = set()
        for sym in all_symbols:
            for child in sym.children:
                if child in all_symbols:
                    child_symbols.add(child)
            for how, related_syms in sym.relations.items():
                if not how.startswith('_inverse_'):
                    for related_sym in related_syms:
                        if related_sym in all_symbols:
                            child_symbols.add(related_sym)

        root_symbols = [sym for sym in all_symbols if sym not in child_symbols]

        if not root_symbols:
            if all_symbols:
                return next(iter(all_symbols))
            else:
                raise ValueError("No symbols found in the JSON string.")

        return root_symbols[0]

    def to_toml(self) -> str:
        """
        Serializes the Symbol graph to a TOML string.
        """
        nodes_data = []
        all_symbols = list(Symbol._pool.values())
        all_symbols.sort(key=lambda s: s.name)

        for sym in all_symbols:
            node_info = {
                "name": sym.name,
                "children": sorted([child.name for child in sym.children]),
                "relations": {how: sorted([related_sym.name for related_sym in related_syms])
                              for how, related_syms in sym.relations.items() if not how.startswith('_inverse_')}
            }
            nodes_data.append(node_info)

        # TOML does not directly support lists of tables without a key
        # So, we wrap it in a dictionary with a top-level key
        return toml.dumps({"symbols": nodes_data})

    @classmethod
    def from_toml(cls, toml_string: str) -> 'Symbol':
        """
        Reconstructs a Symbol graph from a TOML string.
        """
        loaded_data = toml.loads(toml_string)
        nodes_data = loaded_data.get("symbols", [])

        # First pass: Create all Symbol instances
        symbols = {} # type: ignore
        for node_data in nodes_data:
            name = node_data["name"]
            symbols[name] = cls(name)

        # Second pass: Establish children and relations
        for node_data in nodes_data:
            name = node_data["name"]
            current_sym = symbols[name]

            for child_name in node_data.get("children", []):
                child_sym = symbols.get(child_name)
                if child_sym:
                    current_sym.append(child_sym)

            for how, related_names in node_data.get("relations", {}).items():
                for related_name in related_names:
                    related_sym = symbols.get(related_name)
                    if related_sym:
                        current_sym.relate(related_sym, how=how)

        all_symbols = set(symbols.values())
        child_symbols = set()
        for sym in all_symbols:
            for child in sym.children:
                if child in all_symbols:
                    child_symbols.add(child)
            for how, related_syms in sym.relations.items():
                if not how.startswith('_inverse_'):
                    for related_sym in related_syms:
                        if related_sym in all_symbols:
                            child_symbols.add(related_sym)

        root_symbols = [sym for sym in all_symbols if sym not in child_symbols]

        if not root_symbols:
            if all_symbols:
                return next(iter(all_symbols))
            else:
                raise ValueError("No symbols found in the TOML string.")

        return root_symbols[0]

    @classmethod
    def from_ascii(cls, ascii_string: str) -> 'Symbol':
        """
        Reconstructs a Symbol graph from an ASCII string.
        """
        import re
        lines = ascii_string.strip().split('\n')

        symbols = {}  # name -> Symbol instance
        # Stack to keep track of parent-child relationships based on indentation
        # Stores (indentation_level, Symbol_instance)
        parent_stack = []

        # First pass: Parse symbols and their hierarchy
        for line in lines:
            if not line.strip() or line.strip().startswith("---"):
                continue

            symbol_match = re.match(r'^(\s*)- (.+)$', line)
            if symbol_match:
                indent = len(symbol_match.group(1))
                name = symbol_match.group(2)

                # Create the symbol if it doesn't exist
                if name not in symbols:
                    symbols[name] = cls(name)

                # Determine parent based on indentation
                while parent_stack and parent_stack[-1][0] >= indent:
                    parent_stack.pop()

                # If we have a parent, establish the relationship
                if parent_stack:
                    parent_level, parent_symbol = parent_stack[-1]
                    parent_symbol.append(symbols[name])

                # Add current symbol to the stack
                parent_stack.append((indent, symbols[name]))

        # Second pass: Parse relations if they exist
        relation_section = False
        for line in lines:
            if line.strip() == "--- Relations ---":
                relation_section = True
                continue

            if relation_section:
                relation_match = re.match(r'^(.+) --(.+)--> (.+)$', line.strip())
                if relation_match:
                    source_name = relation_match.group(1)
                    relation_type = relation_match.group(2)
                    target_name = relation_match.group(3)

                    if source_name in symbols and target_name in symbols:
                        symbols[source_name].relate(symbols[target_name], how=relation_type)

        # Find the root symbol (one with no parents or the first one if all have parents)
        root_symbols = [s for s in symbols.values() if not s.parents]
        if root_symbols:
            return root_symbols[0]
        else:
            # If no clear root, return the first symbol
            return next(iter(symbols.values()))

    def patch(self, other: 'Symbol') -> 'Symbol':
        """
        Patches this Symbol with attributes from another Symbol.
        """
        if other.origin and not self.origin:
            self.origin = other.origin
        for attr in ("children", "parents"):
            existing = getattr(self, attr)
            new = getattr(other, attr)
            for e in new:
                if e not in existing:
                    existing.append(e)
        # Patch relations
        for how, related_symbols in other.relations.items():
            for related_sym in related_symbols:
                self.relate(related_sym, how=how)
        return self
    def relate(self, other: 'Symbol', how: str = 'related') -> 'Symbol':
        """Establishes a bidirectional relationship with another Symbol."""
        with self._lock:
            # Add forward relationship
            self.relations.add(how, other)

            # Establish inverse relationship
            inverse_how = f"_inverse_{how}"
            other.relations.add(inverse_how, self)
        return self

    def unrelate(self, other: 'Symbol', how: Optional[str] = None) -> 'Symbol':
        """Removes a bidirectional relationship with another Symbol."""
        with self._lock:
            # Remove forward relationship
            if how is None:
                # Remove all relationships with 'other'
                hows_to_remove = [h for h, syms in self.relations.items() if other in syms]
                for h in hows_to_remove:
                    self.relations.remove(h, other)
            else:
                self.relations.remove(how, other)

            # Remove inverse relationship
            if how is None:
                hows_to_remove_inverse = [h for h, syms in other.relations.items() if self in syms and h.startswith('_inverse_')]
                for h in hows_to_remove_inverse:
                    other.relations.remove(h, self)
            else:
                inverse_how = f"_inverse_{how}"
                other.relations.remove(inverse_how, self)
        return self

    @property
    def ref(self) -> Optional[Any]:
        """Alias for .origin, representing the original source or reference of the Symbol."""
        return self.origin

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
        with cls._lock:
            last = cls.last()
            name = f"sym_{cls._auto_counter}"
            sym = cls(name)
            sym._position = cls._auto_counter  # Set position for AVLTree
            cls._numbered.insert(cls._numbered.root, sym, sym._position) # Insert into AVLTree
            if last:
                last._next = sym
                sym._prev = last
            cls._auto_counter += 1
        return sym

    @classmethod
    def prev(cls) -> Optional['Symbol']:
        with cls._lock:
            if cls._auto_counter <= 0:
                return None
            cls._auto_counter -= 1
            # Search for the symb at the decremented position
            node = cls._numbered.search(cls._auto_counter)
            return node.symb if node else None

    @classmethod
    def first(cls) -> Optional['Symbol']:
        node = cls._numbered.min_node()
        return node.value if node else None

    @classmethod
    def last(cls) -> Optional['Symbol']:
        node = cls._numbered.max_node()
        return node.value if node else None

    @classmethod
    def len(cls) -> int:
        return cls._numbered.size()

    @classmethod
    def from_object(cls, obj: Any) -> 'Symbol':
        """Converts an object to a Symbol, acting as a central router."""
        if isinstance(obj, Symbol):
            return obj
        if isinstance(obj, LazySymbol):
            return obj._symb

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
            except (TypeError, orjson.JSONEncodeError) as e:
                import logging
                logging.error(f"Cannot convert {obj_type} to Symbol: {repr(e)}", exc_info=True)
                raise TypeError(f"Cannot convert {obj_type} to Symbol: {repr(e)}")

    @classmethod
    def seek(cls, pos: float) -> Optional['Symbol']:
        node = cls._numbered.search(pos)
        return node.value if node else None

    @classmethod
    def each(cls, start: Union[float, 'Symbol', None] = None) -> Iterator['Symbol']:
        if start is None:
            # Iterate through all symbs in order
            for node in cls._numbered.inorder_traverse():
                yield node.value
        elif isinstance(start, (int, float)):
            # Find the symb at or after the given position and iterate from there
            for node in cls._numbered.inorder_traverse(start_key=start):
                yield node.value
        elif isinstance(start, Symbol):
            # Find the starting symb and iterate from there
            for node in cls._numbered.inorder_traverse(start_key=start._position):
                yield node.value
        else:
            raise TypeError(f"Invalid start parameter {repr(start)} instance of {type(start)} in each")

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

        # Combine attributes from __dict__ (if it exists) and __slots__
        all_attributes = list(getattr(self, '__dict__', {}).keys()) \
                       + list(self.__slots__) \
                       + list(self.__class__.__bases__[0].__slots__)

        for attr_name in all_attributes:
            if attr_name not in protected_attributes and not attr_name.startswith('__'):
                try:
                    value = getattr(self, attr_name)
                    if value is SENTINEL:
                        # Use deep_del for a safer deletion
                        deep_del(self, attr_name)
                except AttributeError:
                    # Attribute might not be set, which is fine
                    pass

        # Clean up elevated attributes that are SENTINEL
        for attr_name in list(self._elevated_attributes.keys()):
            if self._elevated_attributes[attr_name] is SENTINEL and attr_name not in protected_attributes:
                del self._elevated_attributes[attr_name]

        # # this is not the solution, we must delete directly with deep_del
        # gc.collect()  # Explicitly call garbage collector after deletions

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

    def to(self, target_type: Type[T]) -> T:
        """Converts the Symbol to an object of the specified type."""
        try:
            return orjson.loads(self.name)
        except orjson.JSONDecodeError:
            raise TypeError(f"Cannot convert Symbol '{self.name}' to {target_type}")

    @classmethod
    def ps(cls):
        """Lists all loaded symbs with their name, footprint, and origin."""
        total_footprint = 0
        output = ["{:<30} {:<15} {:<50}".format("Name", "Footprint (b)", "Origin")]
        output.append("-" * 95)

        for name, symb in sorted(cls._pool.items()):
            footprint = symb.footprint()
            total_footprint += footprint
            origin = symb.origin
            if origin is None:
                origin_str = f"{symb.__class__.__module__}.{symb.__class__.__name__}"
            else:
                origin_str = str(origin)
            output.append("{:<30} {:<15} {:<50}".format(name, footprint, origin_str))

        output.append("-" * 95)
        output.append("{:<30} {:<15}".format("Total", total_footprint))
        print("\n".join(output))

    @classmethod
    def ls(cls):
        """Lists all available mixin modules."""
        mixins = _get_available_mixins()
        print("Available Mixins:")
        for name in sorted(mixins.keys()):
            print(f"- {name}")

    def stat(self):
        """Provides detailed statistics about the symb and its mixins."""

        all_mixins = _get_available_mixins()
        output = [f"Statistics for Symbol: '{self.name}'"]
        output.append("\n--- Mixin Analysis ---")
        output.append("{:<30} {:<15} {:<15}".format("Mixin Name", "Footprint (b)", "Slim Tag"))
        output.append("-" * 60)

        footprint_all_loaded = 0
        footprint_after_slim = 0
        slim_mixins = []

        for name, mixin_cls in sorted(all_mixins.items()):
            is_slim_tag = False

            # Create a temporary dummy symb to measure mixin size
            dummy_symb = Symbol(f"dummy_for_{name}")
            apply_mixin_to_instance(dummy_symb, mixin_cls)

            footprint = dummy_symb.footprint()
            footprint_all_loaded += footprint

            # Check for non-sentinel values to determine slim tag
            for attr_name in dir(dummy_symb):
                if not attr_name.startswith('__') and not callable(getattr(dummy_symb, attr_name)):
                    try:
                        value = getattr(dummy_symb, attr_name)
                        if value is not SENTINEL:
                            is_slim_tag = True
                            break
                    except AttributeError:
                        pass

            tag = "slim tag" if is_slim_tag else ""
            if is_slim_tag:
                footprint_after_slim += footprint
            else:
                slim_mixins.append(name)

            output.append("{:<30} {:<15} {:<15}".format(name, footprint, tag))

        output.append("-" * 60)

        # 2. Self stats
        current_footprint = self.footprint()
        output.append("\n--- Symbol Footprint ---")
        output.append(f"Current Footprint: {current_footprint} bytes")
        output.append(f"Footprint after .slim(): {footprint_after_slim} bytes")
        output.append(f"  (Would remove: {', '.join(slim_mixins)})")
        output.append(f"Footprint with all mixins loaded: {footprint_all_loaded} bytes")

        print("\n".join(output))

    def footprint(self) -> int:
        """Calculates the memory footprint of the symb and its descendants in bytes."""

        memo = set()

        def get_size(obj):
            if id(obj) in memo:
                return 0
            memo.add(id(obj))

            size = getsizeof(obj)
            if isinstance(obj, dict):
                size += sum(get_size(k) + get_size(v) for k, v in obj.items())
            elif isinstance(obj, (list, tuple, set, frozenset)):
                size += sum(get_size(i) for i in obj)
            elif hasattr(obj, '__dict__'):
                size += get_size(obj.__dict__)

            if hasattr(obj, '__slots__'):
                size += sum(get_size(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))

            # Special handling for Symbol children to avoid recounting
            if isinstance(obj, Symbol):
                # The size of the symb object itself is already counted.
                # Now, add the sizes of its direct attributes and mixins.
                if obj._index is not SENTINEL:
                    size += get_size(obj._index)
                if obj._metadata is not SENTINEL:
                    size += get_size(obj._metadata)
                if obj._context is not SENTINEL:
                    size += get_size(obj._context)
                size += get_size(obj._elevated_attributes)

                # Recursively calculate footprint of children, but avoid double counting
                for child in obj.children:
                    if id(child) not in memo:
                        size += child.footprint()

            return size

        return get_size(self)
