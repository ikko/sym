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
import os
import pkgutil
import importlib

from .base_symbol import Symbol as BaseSymbol
from ..builtins.collections import OrderedSymbolSet
from ..builtins.index import SymbolIndex
from ..core.maturing import DefDict, deep_del, _apply_merge_strategy
from ..core.mixinability import freeze, is_frozen, get_applied_mixins, apply_mixin_to_instance, _get_mixin_metrics

ENABLE_ORIGIN = True
MEMORY_AWARE_DELETE = True

T = TypeVar("T")


def _get_available_mixins():
    """
    what: Discovers all available mixin classes.
    why: To dynamically load and register mixins.
    how: Iterates through builtins and core packages, imports modules, finds classes.
    when: During Symbol initialization or when listing mixins.
    by (caller(s)): Symbol.ls, Symbol.stat.
    how often: Infrequently.
    how much: Moderate, involves file system and import operations.
    what is it like: Scanning for plugins.
    how, what, why and when to improve: Optimize discovery, cache results.
    """
    mixins = {}
    
    import symbol.builtins
    import symbol.core

    def find_mixins_in_path(path, package_name):
        for _, name, ispkg in pkgutil.iter_modules(path):
            if ispkg:
                continue
            
            module_name = f"{package_name}.{name}"
            try:
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if inspect.isclass(attr) and attr.__module__ == module_name:
                        # Heuristic to identify mixins: not a base class and not private
                        if attr_name not in ['Symbol', 'BaseSymbol', 'LazySymbol', 'GraphTraversal'] and not attr_name.startswith('_'):
                            mixins[attr_name] = attr
            except Exception as e:
                warnings.warn(f"Could not import module {module_name}: {e}")

    find_mixins_in_path(symbol.builtins.__path__, 'symbol.builtins')
    find_mixins_in_path(symbol.core.__path__, 'symbol.core')
    
    return mixins


class GraphTraversal:
    def __init__(self, root: 'Symbol', mode: str = 'graph'):
        """
        what: Initializes a graph traversal object.
        why: To prepare for traversing a Symbol graph.
        how: Stores root symbol, traversal mode, and initializes visited set.
        when: When a graph traversal is initiated.
        by (caller(s)): Symbol.graph, Symbol.tree, Symbol.to_ascii.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Setting up a map for navigation.
        how, what, why and when to improve: N/A.
        """
        self.root = root
        self.mode = mode  # 'graph' or 'tree'
        self.visited = set()
        self.result = []

    def traverse(self):
        """
        what: Traverses the Symbol graph.
        why: To collect all reachable symbols based on mode.
        how: Uses a stack-based depth-first traversal.
        when: When a graph or tree representation is needed.
        by (caller(s)): Symbol.graph, Symbol.tree.
        how often: Infrequently.
        how much: Depends on graph size.
        what is it like: Exploring a network.
        how, what, why and when to improve: Implement BFS option, optimize for large graphs.
        """
        stack = [self.root]
        while stack:
            symbol = stack.pop()
            if symbol in self.visited:
                continue
            self.visited.add(symbol)
            self.result.append(symbol)
            neighbors = symbol.children if self.mode == 'tree' else symbol.children
            # Push children in reverse order to maintain original order when popped
            for child in reversed(neighbors):
                stack.append(child)
        return self.result

    def to_ascii(self) -> str:
        """
        what: Generates an ASCII art representation of the graph.
        why: To visualize the graph in a text-based format.
        how: Recursively walks the graph, adding indented symbol names.
        when: When an ASCII visualization is requested.
        by (caller(s)): Symbol.to_ascii.
        how often: Infrequently.
        how much: Depends on graph size.
        what is it like: Drawing a text-based diagram.
        how, what, why and when to improve: Improve formatting, add more graph details.
        """
        lines = []
        visited_ascii = set()
        stack = [(self.root, "")] # (symbol, indent)

        while stack:
            symbol, indent = stack.pop()
            if symbol in visited_ascii:
                continue
            visited_ascii.add(symbol)
            lines.append(f"{indent}- {symbol.name}")
            # Push children in reverse order to maintain original order when popped
            for child in reversed(symbol.children):
                stack.append((child, indent + "  "))
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
        """
        what: Creates a new Symbol instance.
        why: To ensure proper initialization of Symbol attributes.
        how: Calls super().__new__, sets internal attributes, and origin.
        when: Upon Symbol instantiation.
        by (caller(s)): Direct Symbol() calls, from_object.
        how often: Frequently.
        how much: Minimal.
        what is it like: Constructing a basic building block.
        how, what, why and when to improve: N/A.
        """
        obj = super().__new__(cls, name, origin)
        if origin is None:
            obj.origin = f"{cls.__module__}.{cls.__name__}"
        obj._index = SENTINEL
        obj._metadata = SENTINEL
        obj._context = SENTINEL
        obj._elevated_attributes = {}
        return obj

    @property
    def index(self):
        """
        what: Provides access to the Symbol's index.
        why: To manage and query relationships within the Symbol's graph.
        how: Lazily initializes a SymbolIndex if not already present.
        when: When index operations are performed.
        by (caller(s)): Symbol.delete, internal graph operations.
        how often: Infrequently.
        how much: Minimal, lazy initialization.
        what is it like: Accessing a specialized database.
        how, what, why and when to improve: Optimize index creation for large graphs.
        """
        if self._index is SENTINEL:
            self._index = SymbolIndex(self)
        return self._index

    @property
    def metadata(self):
        """
        what: Provides access to the Symbol's metadata.
        why: To store arbitrary key-value data associated with the Symbol.
        how: Lazily initializes a DefDict if not already present.
        when: When metadata is accessed or modified.
        by (caller(s)): Symbol.elevate, external code.
        how often: Frequently.
        how much: Minimal, lazy initialization.
        what is it like: A flexible data container.
        how, what, why and when to improve: N/A.
        """
        if self._metadata is SENTINEL:
            self._metadata = DefDict()
        return self._metadata

    @property
    def context(self):
        """
        what: Provides access to the Symbol's context.
        why: To store transient or contextual data.
        how: Lazily initializes a DefDict if not already present.
        when: When context data is accessed or modified.
        by (caller(s)): Symbol.clear_context, external code.
        how often: Frequently.
        how much: Minimal, lazy initialization.
        what is it like: A scratchpad for temporary data.
        how, what, why and when to improve: N/A.
        """
        if self._context is SENTINEL:
            self._context = DefDict()
        return self._context

    def __getattr__(self, name: str) -> Any:
        """
        what: Custom attribute access for Symbol instances.
        why: To allow dynamic access to elevated attributes.
        how: Checks `_elevated_attributes` first, then falls back to default.
        when: When accessing an attribute not in `__slots__`.
        by (caller(s)): Python's attribute lookup mechanism.
        how often: Frequently.
        how much: Minimal.
        what is it like: A flexible attribute resolver.
        how, what, why and when to improve: N/A.
        """
        if name in self._elevated_attributes:
            return self._elevated_attributes[name]
        # Default behavior for __getattr__ if attribute is not found
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """
        what: Custom attribute assignment for Symbol instances.
        why: To store dynamic attributes in `_elevated_attributes`.
        how: Sets attributes in `__slots__` directly, others in `_elevated_attributes`.
        when: When assigning an attribute to a Symbol.
        by (caller(s)): Python's attribute assignment mechanism.
        how often: Frequently.
        how much: Minimal.
        what is it like: A flexible attribute setter.
        how, what, why and when to improve: N/A.
        """
        # If the attribute is in __slots__ (either in Symbol or BaseSymbol), set it directly
        if name in self.__slots__ or name in self.__class__.__bases__[0].__slots__:
            super().__setattr__(name, value)
        else:
            # Otherwise, store it in _elevated_attributes
            self._elevated_attributes[name] = value

    def __delattr__(self, name: str) -> None:
        """
        what: Custom attribute deletion for Symbol instances.
        why: To correctly remove attributes from `_elevated_attributes`.
        how: Deletes from `__slots__` or `_elevated_attributes`.
        when: When deleting an attribute from a Symbol.
        by (caller(s)): Python's attribute deletion mechanism.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Removing a dynamic property.
        how, what, why and when to improve: N/A.
        """
        if name in self.__slots__ or name in self.__class__.__bases__[0].__slots__:
            super().__delattr__(name)
        elif name in self._elevated_attributes:
            del self._elevated_attributes[name]
        else:
            super().__delattr__(name) # Raise AttributeError if not found

    def append(self, child: Union['Symbol', 'LazySymbol']) -> 'Symbol':
        """
        what: Appends a child Symbol to this Symbol.
        why: To build hierarchical relationships.
        how: Adds child to `children` and sets parent relationship.
        when: When establishing parent-child links.
        by (caller(s)): from_list, from_dict, from_tuple, from_set.
        how often: Frequently.
        how much: Minimal.
        what is it like: Adding a node to a tree.
        how, what, why and when to improve: Optimize for large numbers of children.
        """
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
        """
        what: Adds a child Symbol if not already present.
        why: To ensure unique child relationships.
        how: Checks for existence, then calls `append`.
        when: When adding a child, ensuring no duplicates.
        by (caller(s)): Internal graph operations.
        how often: Frequently.
        how much: Minimal.
        what is it like: Adding a unique element to a set.
        how, what, why and when to improve: N/A.
        """
        # Ensure child is a Symbol instance
        if not isinstance(child, Symbol):
            child = Symbol.from_object(child)

        if child not in self.children:
            return self.append(child)
        return self

    def insert(self, child: 'Symbol', at: float = None) -> 'Symbol':
        """
        what: Inserts a child Symbol at a specific position.
        why: To maintain ordered relationships.
        how: Removes existing child, assigns position, appends.
        when: When precise ordering of children is required.
        by (caller(s)): Internal graph operations.
        how often: Infrequently.
        how much: Moderate, involves list manipulation.
        what is it like: Inserting an element into a sorted list.
        how, what, why and when to improve: Optimize for large lists.
        """
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
        """
        what: Connects children of a removed Symbol to its parents.
        why: To maintain graph connectivity during deletion.
        how: Iterates parents, removes self, adds self's children.
        when: During Symbol deletion.
        by (caller(s)): Symbol.delete.
        how often: Infrequently.
        how much: Depends on number of parents and children.
        what is it like: Rerouting connections in a network.
        how, what, why and when to improve: Optimize for complex graph structures.
        """
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
        """
        what: Rebinds linear sequence pointers.
        why: To maintain integrity of linked list-like structures.
        how: Updates `_prev` and `_next` pointers of adjacent symbols.
        when: During Symbol deletion.
        by (caller(s)): Symbol.delete.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Adjusting links in a chain.
        how, what, why and when to improve: N/A.
        """
        with self._lock:
            if self._prev:
                self._prev._next = self._next
            if self._next:
                self._next._prev = self._prev
            self._prev = None
            self._next = None

    def delete(self) -> None:
        """
        what: Deletes the Symbol from its hierarchy.
        why: To remove a Symbol and clean up its relationships.
        how: Reparents children, rebinds linear sequence, removes from index, severs relationships.
        when: When a Symbol is no longer needed.
        by (caller(s)): Symbol.pop, Symbol.popleft.
        how often: Infrequently.
        how much: Depends on graph complexity.
        what is it like: Decommissioning a component.
        how, what, why and when to improve: Optimize for very large graphs.
        """
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
            except Exception as e:
                log.debug(f"Error during object cleanup: {e}")

    def pop(self) -> 'Symbol':
        """
        what: Safely removes the symbol from its hierarchy.
        why: To extract a symbol while preserving graph integrity.
        how: Calls `delete` and returns the symbol.
        when: When a symbol needs to be extracted.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on graph complexity.
        what is it like: Extracting a part from a machine.
        how, what, why and when to improve: N/A.
        """
        self.delete()
        return self

    def popleft(self) -> Optional['Symbol']:
        """
        what: Removes the first child of the Symbol.
        why: To manage ordered child collections.
        how: Pops the first child, calls its `delete` method.
        when: When managing a queue-like child structure.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Dequeuing an element.
        how, what, why and when to improve: N/A.
        """
        if self.children:
            self._length_cache = None
            popped_child = self.children.pop(0)
            popped_child.delete() # Ensure full cleanup of the popped child
            return popped_child
        return None

    def graph(self):
        """
        what: Returns a graph traversal object for this Symbol.
        why: To enable graph-based operations.
        how: Instantiates `GraphTraversal` in 'graph' mode.
        when: When graph traversal is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Getting a map of connections.
        how, what, why and when to improve: N/A.
        """
        return GraphTraversal(self, mode='graph').traverse()

    def tree(self):
        """
        what: Returns a tree traversal object for this Symbol.
        why: To enable tree-based operations.
        how: Instantiates `GraphTraversal` in 'tree' mode.
        when: When tree traversal is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Getting a map of a hierarchy.
        how, what, why and when to improve: N/A.
        """
        return GraphTraversal(self, mode='tree').traverse()

    def to_mmd(self) -> str:
        """
        what: Generates a Mermaid diagram string.
        why: To visualize the Symbol graph in Mermaid format.
        how: Traverses the graph, formats nodes and edges.
        when: When a Mermaid visualization is requested.
        by (caller(s)): External tools, documentation.
        how often: Infrequently.
        how much: Depends on graph size.
        what is it like: Drawing a diagram.
        how, what, why and when to improve: Optimize for large graphs.
        """
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

            for i, related_sym in enumerate(sym.related_to):
                how = sym.related_how[i]
                if not how.startswith("_inverse_"):
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

    def to_ascii(self) -> str:
        """
        what: Generates an ASCII art representation of the Symbol.
        why: To visualize the Symbol's structure in text.
        how: Delegates to `GraphTraversal.to_ascii`.
        when: When a text-based visualization is requested.
        by (caller(s)): External tools, debugging.
        how often: Infrequently.
        how much: Depends on graph size.
        what is it like: Drawing a text-based diagram.
        how, what, why and when to improve: N/A.
        """
        return GraphTraversal(self, mode='tree').to_ascii()

    def patch(self, other: 'Symbol') -> 'Symbol':
        """
        what: Patches this Symbol with attributes from another.
        why: To merge properties from another Symbol.
        how: Copies origin, appends children, parents, related_to.
        when: When combining Symbol data.
        by (caller(s)): Internal operations.
        how often: Infrequently.
        how much: Depends on number of attributes.
        what is it like: Applying an update.
        how, what, why and when to improve: More sophisticated merge strategies.
        """
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
        """
        what: Establishes a bidirectional relationship.
        why: To define connections between Symbols.
        how: Appends to `related_to` and `related_how` lists for both Symbols.
        when: When defining graph relationships.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Drawing a line between two points.
        how, what, why and when to improve: Optimize for many relationships.
        """
        with self._lock:
            # Check if this specific relationship already exists
            relationship_exists = False
            for i, existing_other in enumerate(self.related_to):
                if existing_other == other and self.related_how[i] == how:
                    relationship_exists = True
                    break

            if not relationship_exists:
                self.related_to.append(other)
                self.related_how.append(how)
            
            # Establish inverse relationship
            inverse_how = f"_inverse_{how}"
            inverse_relationship_exists = False
            for i, existing_self in enumerate(other.related_to):
                if existing_self == self and other.related_how[i] == inverse_how:
                    inverse_relationship_exists = True
                    break

            if not inverse_relationship_exists:
                other.related_to.append(self)
                other.related_how.append(inverse_how)
        return self

    def unrelate(self, other: 'Symbol', how: Optional[str] = None) -> 'Symbol':
        """
        what: Removes a bidirectional relationship.
        why: To break connections between Symbols.
        how: Filters `related_to` and `related_how` lists for both Symbols.
        when: When a relationship is no longer needed.
        by (caller(s)): Symbol.delete, external code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Erasing a line between two points.
        how, what, why and when to improve: Optimize for many relationships.
        """
        with self._lock:
            # Remove forward relationship
            relationships_to_keep_self = []
            for i, related_sym in enumerate(self.related_to):
                if related_sym == other:
                    # This is the 'other' symbol we are trying to unrelate
                    if how is None:
                        # If 'how' is None, remove all relationships with 'other'
                        continue
                    elif self.related_how[i] == how:
                        # If 'how' is specified and matches, remove this specific relationship
                        continue
                    else:
                        # If 'how' is specified but doesn't match, keep this relationship
                        relationships_to_keep_self.append((related_sym, self.related_how[i]))
                else:
                    # Keep relationships with other symbols (not 'other')
                    relationships_to_keep_self.append((related_sym, self.related_how[i]))

            self.related_to = [r[0] for r in relationships_to_keep_self]
            self.related_how = [r[1] for r in relationships_to_keep_self]

            # Remove inverse relationship
            relationships_to_keep_other = []
            for i, related_sym in enumerate(other.related_to):
                if related_sym == self:
                    # This is 'self' in the context of 'other's relationships
                    expected_inverse_how = f"_inverse_{how}" if how is not None else None
                    if how is None:
                        # If 'how' is None, remove all inverse relationships with 'self'
                        continue
                    elif other.related_how[i] == expected_inverse_how:
                        # If 'how' is specified and matches, remove this specific inverse relationship
                        continue
                    else:
                        # If 'how' is specified but doesn't match, keep this inverse relationship
                        relationships_to_keep_other.append((related_sym, other.related_how[i]))
                else:
                    # Keep relationships with other symbols (not 'self')
                    relationships_to_keep_other.append((related_sym, other.related_how[i]))

            other.related_to = [r[0] for r in relationships_to_keep_other]
            other.related_how = [r[1] for r in relationships_to_keep_other]
        return self

    @property
    def ref(self) -> Optional[Any]:
        """
        what: Alias for the Symbol's origin.
        why: To provide a more intuitive name for the source.
        how: Returns the value of the `origin` attribute.
        when: When accessing the Symbol's original source.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Minimal.
        what is it like: A shortcut to the source.
        how, what, why and when to improve: N/A.
        """
        return self.origin

    def head(self, up_to_position: float = 5.0):
        """
        what: Returns a Symbol at or before a given position.
        why: To navigate linear sequences.
        how: Traverses `_prev` pointers until position is met.
        when: When navigating ordered Symbol sequences.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on distance to head.
        what is it like: Finding a point in a linked list.
        how, what, why and when to improve: Optimize for very long sequences.
        """
        cur = self
        while cur._prev and cur._prev._position >= up_to_position:
            cur = cur._prev
        return cur

    def tail(self, from_position: float = -10.0):
        """
        what: Returns a Symbol at or after a given position.
        why: To navigate linear sequences.
        how: Traverses `_next` pointers until position is met.
        when: When navigating ordered Symbol sequences.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on distance to tail.
        what is it like: Finding a point in a linked list.
        how, what, why and when to improve: Optimize for very long sequences.
        """
        cur = self
        while cur._next and cur._next._position <= from_position:
            cur = cur._next
        return cur

    @classmethod
    def auto_date(cls) -> 'Symbol':
        """
        what: Creates a Symbol with today's date as its name.
        why: For quick creation of date-based Symbols.
        how: Uses `datetime.date.today().isoformat()`.
        when: When a Symbol representing today's date is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Stamping a date.
        how, what, why and when to improve: N/A.
        """
        iso = datetime.date.today().isoformat()
        return cls(iso)

    @classmethod
    def auto_datetime(cls) -> 'Symbol':
        """
        what: Creates a Symbol with the current datetime as its name.
        why: For quick creation of datetime-based Symbols.
        how: Uses `datetime.datetime.now().isoformat()`.
        when: When a Symbol representing the current datetime is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Stamping a datetime.
        how, what, why and when to improve: N/A.
        """
        iso = datetime.datetime.now().isoformat()
        return cls(iso)

    @classmethod
    def auto_time(cls) -> 'Symbol':
        """
        what: Creates a Symbol with the current time as its name.
        why: For quick creation of time-based Symbols.
        how: Uses `datetime.datetime.now().time().isoformat()`.
        when: When a Symbol representing the current time is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Stamping a time.
        how, what, why and when to improve: N/A.
        """
        iso = datetime.datetime.now().time().isoformat()
        return cls(iso)

    @classmethod
    def next(cls) -> 'Symbol':
        """
        what: Creates the next Symbol in a sequence.
        why: To generate sequential Symbols.
        how: Increments a counter, creates new Symbol, links to previous.
        when: When generating ordered Symbols.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Generating the next number in a series.
        how, what, why and when to improve: Optimize for high-frequency generation.
        """
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
        """
        what: Retrieves the previous Symbol in a sequence.
        why: To navigate sequential Symbols backward.
        how: Decrements counter, searches AVLTree for Symbol.
        when: When navigating ordered Symbol sequences.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on AVLTree depth.
        what is it like: Finding the prior element.
        how, what, why and when to improve: Optimize AVLTree search.
        """
        with cls._lock:
            if cls._auto_counter <= 0:
                return None
            cls._auto_counter -= 1
            # Search for the symbol at the decremented position
            node = cls._numbered.search(cls._auto_counter)
            return node.symbol if node else None

    @classmethod
    def first(cls) -> Optional['Symbol']:
        """
        what: Retrieves the first Symbol in the collection.
        why: To access the initial Symbol.
        how: Uses AVLTree's min_node.
        when: When the first Symbol is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Getting the first item.
        how, what, why and when to improve: N/A.
        """
        node = cls._numbered.min_node()
        return node.value if node else None

    @classmethod
    def last(cls) -> Optional['Symbol']:
        """
        what: Retrieves the last Symbol in the collection.
        why: To access the final Symbol.
        how: Uses AVLTree's max_node.
        when: When the last Symbol is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Getting the last item.
        how, what, why and when to improve: N/A.
        """
        node = cls._numbered.max_node()
        return node.value if node else None

    @classmethod
    def len(cls) -> int:
        """
        what: Returns the number of Symbols in the collection.
        why: To get the size of the Symbol collection.
        how: Uses AVLTree's size method.
        when: When the count of Symbols is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Counting elements.
        how, what, why and when to improve: N/A.
        """
        return cls._numbered.size()

    @classmethod
    def from_object(cls, obj: Any) -> 'Symbol':
        """
        what: Converts an object to a Symbol.
        why: To provide a unified way to create Symbols from various types.
        how: Uses a type map and specialized conversion functions.
        when: When creating Symbols from arbitrary Python objects.
        by (caller(s)): Symbol.append, Symbol.add, Symbol.insert.
        how often: Frequently.
        how much: Depends on object complexity.
        what is it like: A universal adapter.
        how, what, why and when to improve: Add more type conversions, optimize for large objects.
        """
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
        """
        what: Seeks a Symbol by its position.
        why: To retrieve a specific Symbol in an ordered collection.
        how: Uses AVLTree's search method.
        when: When direct access by position is needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on AVLTree depth.
        what is it like: Finding an element by index.
        how, what, why and when to improve: Optimize AVLTree search.
        """
        node = cls._numbered.search(pos)
        return node.value if node else None

    @classmethod
    def each(cls, start: Union[float, 'Symbol', None] = None) -> Iterator['Symbol']:
        """
        what: Iterates through Symbols in order.
        why: To process Symbols sequentially.
        how: Traverses AVLTree in-order.
        when: When iterating over all or a subset of Symbols.
        by (caller(s)): External code.
        how often: Frequently.
        how much: Depends on number of Symbols.
        what is it like: Looping through a list.
        how, what, why and when to improve: Optimize traversal for large collections.
        """
        if start is None:
            # Iterate through all symbols in order
            for node in cls._numbered.inorder_traverse():
                yield node.value
        elif isinstance(start, (int, float)):
            # Find the symbol at or after the given position and iterate from there
            for node in cls._numbered.inorder_traverse(start_key=start):
                yield node.value
        elif isinstance(start, Symbol):
            # Find the starting symbol and iterate from there
            for node in cls._numbered.inorder_traverse(start_key=start._position):
                yield node.value
        else:
            raise TypeError(f"Invalid start parameter {repr(start)} instance of {type(start)} in each")

    def each_parents(self) -> Iterator['Symbol']:
        """
        what: Iterates through the Symbol's parents.
        why: To access direct parent relationships.
        how: Returns an iterator over the `parents` list.
        when: When navigating up the Symbol hierarchy.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Listing direct ancestors.
        how, what, why and when to improve: N/A.
        """
        return iter(self.parents)

    def each_children(self) -> Iterator['Symbol']:
        """
        what: Iterates through the Symbol's children.
        why: To access direct child relationships.
        how: Returns an iterator over the `children` list.
        when: When navigating down the Symbol hierarchy.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Listing direct descendants.
        how, what, why and when to improve: N/A.
        """
        return iter(self.children)

    def __enter__(self):
        """
        what: Enters the runtime context for the Symbol.
        why: To support `with` statement usage.
        how: Returns self.
        when: When using Symbol as a context manager.
        by (caller(s)): Python's `with` statement.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Opening a resource.
        how, what, why and when to improve: N/A.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        what: Exits the runtime context for the Symbol.
        why: To support `with` statement usage.
        how: Does nothing.
        when: When exiting Symbol's context manager.
        by (caller(s)): Python's `with` statement.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Closing a resource.
        how, what, why and when to improve: Implement cleanup logic if needed.
        """
        pass

    def elevate(self, merge_strategy: Literal['overwrite', 'patch', 'copy', 'deepcopy', 'pipe', 'update', 'extend', 'smooth'] = 'smooth') -> Set[str]:
        """
        what: Elevates metadata to instance attributes.
        why: To make metadata directly accessible as attributes.
        how: Iterates metadata, applies merge strategy, sets attributes.
        when: During maturing process or explicit elevation.
        by (caller(s)): Symbol.immute.
        how often: Infrequently.
        how much: Depends on metadata size.
        what is it like: Promoting data to a higher level.
        how, what, why and when to improve: Optimize for large metadata.
        """
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
        """
        what: Removes non-protected dynamic attributes.
        why: To reduce memory footprint and simplify Symbol state.
        how: Iterates attributes, deletes non-protected ones.
        when: During maturing process or explicit slimming.
        by (caller(s)): Symbol.immute.
        how often: Infrequently.
        how much: Depends on number of dynamic attributes.
        what is it like: Trimming unnecessary parts.
        how, what, why and when to improve: Optimize for many dynamic attributes.
        """
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

        gc.collect()  # Explicitly call garbage collector after deletions

    def immute(self, merge_strategy: Literal['overwrite', 'patch', 'copy', 'deepcopy', 'pipe', 'update', 'extend', 'smooth'] = 'smooth') -> None:
        """
        what: Orchestrates the Symbol maturing process.
        why: To finalize Symbol state and prevent further changes.
        how: Calls `elevate`, `slim`, and `freeze`.
        when: When a Symbol's state should become immutable.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on Symbol complexity.
        what is it like: Finalizing a design.
        how, what, why and when to improve: N/A.
        """
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
        """
        what: Clears the Symbol's context.
        why: To free up memory associated with transient data.
        how: Deletes all entries from the `context` DefDict.
        when: When context data is no longer needed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on context size.
        what is it like: Wiping a temporary workspace.
        how, what, why and when to improve: N/A.
        """
        if is_frozen():
            warnings.warn(f"Cannot clear context on frozen Symbol {self.name}")
            return

        # Iterate over a copy of keys to allow modification during iteration
        for key in list(self.context.keys()):
            # DefDict's __delitem__ will handle logging and potential deep_del for nested DefDicts
            del self.context[key]

    def to(self, target_type: Type[T]) -> T:
        """
        what: Converts the Symbol to a specified type.
        why: To facilitate interoperability with other data structures.
        how: Attempts to parse Symbol name as JSON.
        when: When converting Symbol to a primitive type.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Type casting.
        how, what, why and when to improve: Add more conversion methods.
        """
        try:
            return orjson.loads(self.name)
        except orjson.JSONDecodeError:
            raise TypeError(f"Cannot convert Symbol '{self.name}' to {target_type}")

    @classmethod
    def ps(cls):
        """
        what: Lists all loaded Symbols.
        why: To provide an overview of active Symbols in memory.
        how: Iterates through the Symbol pool, calculates footprint, displays metrics.
        when: When inspecting the Symbol runtime environment.
        by (caller(s)): User command.
        how often: Infrequently.
        how much: Depends on number of Symbols.
        what is it like: Listing running processes.
        how, what, why and when to improve: Add more detailed metrics, filtering.
        """
        total_footprint = 0
        output = ["{:<30} {:<15} {:<50} {:<10} {:<20} {:<10}".format("Name", "Footprint (b)", "Origin", "State", "Uptime", "Healthy")]
        output.append("-" * 135)

        for name, symbol in sorted(cls._pool.items()):
            footprint = symbol.footprint()
            total_footprint += footprint
            origin = symbol.origin
            if origin is None:
                origin_str = f"{symbol.__class__.__module__}.{symbol.__class__.__name__}"
            else:
                origin_str = str(origin)
            
            # For Symbol instances, we can't directly get mixin metrics without knowing which mixins are applied.
            # This would require iterating through applied_mixins or having a direct link.
            # For now, we'll just show UNKNOWN for state, uptime, healthy.
            state = "unknown"
            uptime = "N/A"
            healthy = "N/A"

            output.append("{:<30} {:<15} {:<50} {:<10} {:<20} {:<10}".format(name, footprint, origin_str, state, uptime, healthy))

        output.append("-" * 135)
        output.append("{:<30} {:<15}".format("Total", total_footprint))
        print("\n".join(output))

    @classmethod
    def ls(cls):
        """
        what: Lists all available mixins.
        why: To provide an overview of extendable capabilities.
        how: Discovers mixins, calculates metrics, displays formatted output.
        when: When exploring available Symbol extensions.
        by (caller(s)): User command.
        how often: Infrequently.
        how much: Moderate, involves mixin discovery.
        what is it like: Listing available plugins.
        how, what, why and when to improve: Add filtering, more details.
        """
        mixins = _get_available_mixins()
        output = ["Available Mixins:"]
        output.append("{:<30} {:<15} {:<15} {:<10} {:<20} {:<10}".format("Mixin Name", "Footprint (b)", "Slim Tag", "State", "Uptime", "Healthy"))
        output.append("-" * 100)

        for name, mixin_cls in sorted(mixins.items()):
            # Create a dummy instance to get metrics
            metrics = _get_mixin_metrics(mixin_cls() if inspect.isclass(mixin_cls) else mixin_cls, Symbol)
            
            footprint = metrics['footprint']
            is_slim_tag = metrics['slim_tag']
            state = metrics['state']
            uptime = str(metrics['uptime']).split('.')[0] # Format timedelta
            healthy = metrics['healthy']

            tag = "slim tag" if is_slim_tag else ""
            output.append("{:<30} {:<15} {:<15} {:<10} {:<20} {:<10}".format(name, footprint, tag, state, uptime, healthy))

        output.append("-" * 100)
        print("\n".join(output))

    def stat(self):
        """
        what: Provides detailed Symbol statistics.
        why: To understand Symbol's memory usage and mixin impact.
        how: Calculates footprint, analyzes applied mixins, displays formatted output.
        when: When debugging memory or mixin behavior.
        by (caller(s)): User command.
        how often: Infrequently.
        how much: Moderate, involves dummy Symbol creation.
        what is it like: Running a diagnostic report.
        how, what, why and when to improve: More granular memory analysis, performance metrics.
        """
        
        all_mixins = _get_available_mixins()
        output = [f"Statistics for Symbol: '{self.name}'"]
        output.append("\n--- Mixin Analysis ---")
        output.append("{:<30} {:<15} {:<15} {:<10} {:<20} {:<10}".format("Mixin Name", "Footprint (b)", "Slim Tag", "State", "Uptime", "Healthy"))
        output.append("-" * 100)

        footprint_all_loaded = 0
        footprint_after_slim = 0
        slim_mixins = []

        for name, mixin_cls in sorted(all_mixins.items()):
            # Create a temporary dummy symbol to measure mixin size and get metrics
            dummy_symbol = Symbol(f"dummy_for_{name}")
            apply_mixin_to_instance(dummy_symbol, mixin_cls)
            
            metrics = _get_mixin_metrics(mixin_cls() if inspect.isclass(mixin_cls) else mixin_cls, Symbol)
            
            footprint = metrics['footprint']
            is_slim_tag = metrics['slim_tag']
            state = metrics['state']
            uptime = str(metrics['uptime']).split('.')[0] # Format timedelta
            healthy = metrics['healthy']

            footprint_all_loaded += footprint

            tag = "slim tag" if is_slim_tag else ""
            if is_slim_tag:
                footprint_after_slim += footprint
            else:
                slim_mixins.append(name)
                
            output.append("{:<30} {:<15} {:<15} {:<10} {:<20} {:<10}".format(name, footprint, tag, state, uptime, healthy))

        output.append("-" * 100)

        # 2. Self stats
        current_footprint = self.footprint()
        output.append("\n--- Symbol Footprint ---")
        output.append(f"Current Footprint: {current_footprint} bytes")
        output.append(f"Footprint after .slim(): {footprint_after_slim} bytes")
        output.append(f"  (Would remove: {', '.join(slim_mixins)})")
        output.append(f"Footprint with all mixins loaded: {footprint_all_loaded} bytes")

        print("\n".join(output))

    def footprint(self) -> int:
        """
        what: Calculates Symbol's memory footprint.
        why: To understand memory consumption.
        how: Recursively sums sizes of object attributes and descendants.
        when: When memory usage analysis is needed.
        by (caller(s)): Symbol.ps, Symbol.stat.
        how often: Infrequently.
        how much: Depends on graph size.
        what is it like: Measuring an object's size.
        how, what, why and when to improve: More accurate deep sizing.
        """
        
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
                # The size of the symbol object itself is already counted.
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


def to_sym(obj: Any) -> 'Symbol':
    """
    what: Converts an object to a Symbol.
    why: To provide a convenient global conversion function.
    how: Delegates to `Symbol.from_object`.
    when: When converting arbitrary objects to Symbols.
    by (caller(s)): External code.
    how often: Frequently.
    how much: Depends on object complexity.
    what is it like: A universal Symbol factory.
    how, what, why and when to improve: N/A.
    """
    return Symbol.from_object(obj)


class SymbolNamespace:
    """Provides a convenient way to create Symbol instances via attribute access."""
    def __getattr__(self, name):
        """
        what: Allows creating Symbols via attribute access.
        why: For a more convenient and readable Symbol creation syntax.
        how: Returns a new Symbol instance with the attribute name.
        when: When accessing an attribute on the `s` (SymbolNamespace) object.
        by (caller(s)): Python's attribute lookup.
        how often: Frequently.
        how much: Minimal.
        what is it like: A dynamic Symbol factory.
        how, what, why and when to improve: N/A.
        """
        return Symbol(name)

    def __getitem__(self, name):
        """
        what: Allows creating Symbols via item access.
        why: For a more convenient and readable Symbol creation syntax.
        how: Returns a new Symbol instance with the item name.
        when: When accessing an item on the `s` (SymbolNamespace) object.
        by (caller(s)): Python's item lookup.
        how often: Frequently.
        how much: Minimal.
        what is it like: A dynamic Symbol factory.
        how, what, why and when to improve: N/A.
        """
        return Symbol(name)

    def __setitem__(self, name, value):
        """
        what: Prevents setting items on SymbolNamespace.
        why: To enforce read-only behavior.
        how: Raises a TypeError.
        when: When attempting to assign to an item on `s`.
        by (caller(s)): Python's item assignment.
        how often: Rarely, only on misuse.
        how much: Minimal.
        what is it like: A read-only proxy.
        how, what, why and when to improve: N/A.
        """
        raise TypeError(f"SymbolNamespace is read-only, cannot set {name} to {value}")

    def __setattr__(self, name, value):
        """
        what: Prevents setting attributes on SymbolNamespace.
        why: To enforce read-only behavior.
        how: Raises a TypeError.
        when: When attempting to assign to an attribute on `s`.
        by (caller(s)): Python's attribute assignment.
        how often: Rarely, only on misuse.
        how much: Minimal.
        what is it like: A read-only proxy.
        how, what, why and when to improve: N/A.
        """
        raise TypeError(f"SymbolNamespace is read-only, cannot set {name} to {value}")

s = SymbolNamespace()
