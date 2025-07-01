# Code Inventory: Symbol Project

This document provides a detailed inventory of all classes, functions, and methods within the `symbol` project, including their signatures, return types, and concise summaries.

## Overview

| Metric             | Value   |
| :----------------- | :------ |
| Total Python Files | 13      |
| Total Lines of Code| 589     |
| Estimated Tokens   | 1473    |

---

### File: `symbol/__init__.py`
Lines: 20
Bytes: 490
Estimated Tokens: 123
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Variable: `datetime`
    Summary: Alias for builtins.datetime, providing direct access to datetime functionalities.
  - Variable: `collections`
    Summary: Alias for builtins.collections, offering access to custom collection types.
  - Variable: `indexing`
    Summary: Alias for builtins.indexing, exposing indexing and tree-related features.
  - Variable: `path`
    Summary: Alias for builtins.path, enabling pathfinding and graph matching.
  - Variable: `visual`
    Summary: Alias for builtins.visual, providing visualization utilities.
  - Variable: `dt`
    Summary: Short alias for builtins.datetime, simplifying access to datetime functions.
  - Variable: `coll`
    Summary: Short alias for builtins.collections, for concise access to collection types.
  - Variable: `idx`
    Summary: Short alias for builtins.indexing, for quick access to indexing features.
  - Variable: `vis`
    Summary: Short alias for builtins.visual, for convenient access to visualization tools.
  - Function: `apply_builtins()`
    Summary: Applies all modular extensions to the core Symbol class.

### File: `symbol/builtins/__init__.py`
Lines: 24
Bytes: 890
Estimated Tokens: 223
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Function: `apply_builtins()`
    Summary: Applies various mixin functionalities to the Symbol class using register_patch.

### File: `symbol/builtins/avl_tree.py`
Lines: 1
Bytes: 1
Estimated Tokens: 1
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Summary: This file is currently empty and serves as a placeholder for AVL tree implementation.

### File: `symbol/builtins/collections.py`
Lines: 29
Bytes: 560
Estimated Tokens: 140
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Class: `OrderedSymbolSet`
    Summary: A collection that stores unique Symbol objects, maintaining insertion order.
  - Method: `OrderedSymbolSet.__init__(self, items=None)`
    Summary: Initializes the OrderedSymbolSet, optionally adding initial items.
  - Method: `OrderedSymbolSet.add(self, sym: 'Symbol')`
    Summary: Adds a Symbol to the set, patching it if already present.
  - Method: `OrderedSymbolSet.__iter__(self)`
    Summary: Returns an iterator over the Symbol objects in the set.
  - Method: `OrderedSymbolSet.__len__(self)`
    Summary: Returns the number of unique Symbol objects in the set.
  - Method: `OrderedSymbolSet.__contains__(self, sym)`
    Summary: Checks if a Symbol object is present in the set.

### File: `symbol/builtins/datetime.py`
Lines: 90
Bytes: 2400
Estimated Tokens: 600
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Class: `SymbolDateTimeMixin`
    Summary: Provides date and time related properties and methods for Symbol objects.
  - Method: `SymbolDateTimeMixin._parse_timestamp(self, s: 'Symbol') -> datetime.datetime`
    Summary: Parses a Symbol's name into a datetime object, handling potential errors.
  - Method: `SymbolDateTimeMixin._sorted_by_time(self) -> list['Symbol']`
    Summary: Returns a list of Symbols sorted by their parsed datetime.
  - Method: `SymbolDateTimeMixin.head(self) -> 'SymbolHeadTailView'`
    Summary: Property returning a view of Symbols sorted chronologically (earliest first).
  - Method: `SymbolDateTimeMixin.tail(self) -> 'SymbolHeadTailView'`
    Summary: Property returning a view of Symbols sorted in reverse chronological order (latest first).
  - Method: `SymbolDateTimeMixin.as_date(self) -> datetime.date`
    Summary: Property returning the date part of the Symbol's name as a date object.
  - Method: `SymbolDateTimeMixin.as_time(self) -> datetime.time`
    Summary: Property returning the time part of the Symbol's name as a time object.
  - Method: `SymbolDateTimeMixin.as_datetime(self) -> datetime.datetime`
    Summary: Property returning the full datetime object parsed from the Symbol's name.
  - Method: `SymbolDateTimeMixin.day(self) -> int`
    Summary: Property returning the day component of the Symbol's datetime.
  - Method: `SymbolDateTimeMixin.hour(self) -> int`
    Summary: Property returning the hour component of the Symbol's datetime.
  - Method: `SymbolDateTimeMixin.minute(self) -> int`
    Summary: Property returning the minute component of the Symbol's datetime.
  - Method: `SymbolDateTimeMixin.second(self) -> int`
    Summary: Property returning the second component of the Symbol's datetime.
  - Method: `SymbolDateTimeMixin.period(self) -> datetime.timedelta`
    Summary: Property returning the time duration between the first and last Symbols in a sorted view.
  - Method: `SymbolDateTimeMixin.as_period(self) -> datetime.timedelta`
    Summary: Alias for the `period` property, returning the time duration.
  - Method: `SymbolDateTimeMixin.duration(self) -> datetime.timedelta`
    Summary: Alias for the `period` property, returning the time duration.
  - Method: `SymbolDateTimeMixin.as_duration(self) -> datetime.timedelta`
    Summary: Alias for the `as_period` property, returning the time duration.
  - Method: `SymbolDateTimeMixin.delta(self) -> datetime.timedelta`
    Summary: Alias for the `period` property, returning the time duration.
  - Method: `SymbolDateTimeMixin.as_delta(self) -> datetime.timedelta`
    Summary: Alias for the `as_period` property, returning the time duration.
  - Class: `SymbolHeadTailView`
    Summary: A view class for Symbol lists, enabling time-based filtering and period calculations.
  - Method: `SymbolHeadTailView.__init__(self, items: list['Symbol'])`
    Summary: Initializes the SymbolHeadTailView with a list of Symbols.
  - Method: `SymbolHeadTailView.__getitem__(self, item)`
    Summary: Allows indexing and slicing of the Symbol list within the view.
  - Method: `SymbolHeadTailView.__iter__(self) -> Iterator['Symbol']`
    Summary: Returns an iterator for the Symbols in the view.
  - Method: `SymbolHeadTailView.__len__(self)`
    Summary: Returns the number of Symbols in the view.
  - Method: `SymbolHeadTailView.period(self) -> datetime.timedelta`
    Summary: Calculates the time difference between the first and last Symbols in the view.
  - Method: `SymbolHeadTailView.as_period(self) -> datetime.timedelta`
    Summary: Alias for the `period` property.
  - Method: `SymbolHeadTailView.days(self) -> int`
    Summary: Returns the number of days in the calculated period.
  - Method: `SymbolHeadTailView.seconds(self) -> int`
    Summary: Returns the number of seconds in the calculated period.
  - Method: `SymbolHeadTailView.filter_by_month(self, year: int, month: int) -> 'SymbolHeadTailView'`
    Summary: Filters Symbols in the view by a specific year and month.

### File: `symbol/builtins/indexing.py`
Lines: 140
Bytes: 4000
Estimated Tokens: 1000
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Variable: `ENABLE_ORIGIN`
    Summary: Global flag to enable or disable origin tracking for Symbols.
  - Variable: `MEMORY_AWARE_DELETE`
    Summary: Global flag to enable or disable memory-aware deletion for Symbols.
  - Class: `IndexNode`
    Summary: Represents a node within the SymbolIndex, holding a Symbol and its associated weight.
  - Method: `IndexNode.__init__(self, symbol: 'Symbol', weight: Union[float, Callable[[Any], float]] = 0.0)`
    Summary: Initializes an IndexNode with a Symbol and its weight.
  - Method: `IndexNode.eval_weight(self, *args, **kwargs) -> float`
    Summary: Evaluates the weight of the node, supporting callable weights.
  - Class: `SymbolIndex`
    Summary: Manages a weighted binary search tree for a Symbol, enabling efficient lookup and rebalancing.
  - Method: `SymbolIndex.__init__(self, owner: 'Symbol')`
    Summary: Initializes the SymbolIndex for a given owner Symbol.
  - Method: `SymbolIndex.insert(self, symbol: 'Symbol', weight: Union[float, Callable])`
    Summary: Inserts a Symbol into the index with a specified weight.
  - Function: `_insert(node: Optional[IndexNode], sym: Symbol) -> IndexNode`
    Summary: Recursively inserts a Symbol into the index tree.
  - Method: `SymbolIndex.map(self, fn: Callable[['Symbol'], Any]) -> list[Any]`
    Summary: Applies a function to each Symbol in the index and returns the results.
  - Method: `SymbolIndex.filter(self, pred: Callable[['Symbol'], bool]) -> list['Symbol']`
    Summary: Filters Symbols in the index based on a given predicate function.
  - Method: `SymbolIndex.traverse(self, order: Literal["in", "pre", "post"] = "in") -> list['Symbol']`
    Summary: Traverses the index in specified order (in-order, pre-order, post-order).
  - Function: `_walk(node: Optional[IndexNode])`
    Summary: Recursively walks the index tree for `traverse` method.
  - Method: `SymbolIndex.rebalance(self, strategy: Literal['avl', 'red_black', 'weight', 'hybrid'] = 'weight') -> None`
    Summary: Rebalances the index using various tree balancing strategies.
  - Function: `build_balanced(sorted_syms)`
    Summary: Recursively builds a balanced binary search tree from sorted symbols.
  - Function: `copy_from_avl(node: Optional[AVLNode]) -> Optional[IndexNode]`
    Summary: Copies nodes from an AVL tree to an IndexNode structure.
  - Function: `copy_from_rbt(node: Optional[RedBlackNode]) -> Optional[IndexNode]`
    Summary: Copies nodes from a Red-Black tree to an IndexNode structure.
  - Function: `hybrid_weight(sym: 'Symbol')`
    Summary: Calculates a hybrid weight for a Symbol based on its original weight and age.
  - Method: `SymbolIndex.__getattr__(self, name: str)`
    Summary: Intercepts attribute access to dynamically call functions associated with indexed Symbols.
  - Function: `wrapped(*args, **kwargs)`
    Summary: A wrapper function for dynamically called methods, including before/after hooks.
  - Method: `SymbolIndex.before(self, *args, **kwargs)`
    Summary: Placeholder method executed before an indexed function call.
  - Method: `SymbolIndex.after(self, *args, **kwargs)`
    Summary: Placeholder method executed after an indexed function call.
  - Method: `SymbolIndex.ascii(self)`
    Summary: Generates an ASCII representation of the index tree.
  - Function: `_walk(node: Optional[IndexNode], depth: int = 0)`
    Summary: Recursively walks the index tree to generate ASCII representation.

### File: `symbol/builtins/path.py`
Lines: 44
Bytes: 1100
Estimated Tokens: 275
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Class: `SymbolPathMixin`
    Summary: Provides methods for pathfinding and matching within a Symbol graph.
  - Method: `SymbolPathMixin.path_to(self, target: 'Symbol') -> list['Symbol']`
    Summary: Finds a path from the current Symbol to a target Symbol using DFS.
  - Function: `dfs(node: 'Symbol') -> bool`
    Summary: Performs a Depth-First Search to find a path to a target.
  - Method: `SymbolPathMixin.match(self, predicate: Callable[['Symbol'], bool], traversal: str = 'dfs') -> Iterator['Symbol']`
    Summary: Finds and yields Symbols matching a predicate using DFS or BFS traversal.
  - Function: `dfs(node: 'Symbol')`
    Summary: Performs a Depth-First Search to find matching symbols.
  - Function: `bfs(start: 'Symbol')`
    Summary: Performs a Breadth-First Search to find matching symbols.

### File: `symbol/builtins/red_black_tree.py`
Lines: 100
Bytes: 2800
Estimated Tokens: 700
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Variable: `RED`
    Summary: Constant representing the color red in a Red-Black tree.
  - Variable: `BLACK`
    Summary: Constant representing the color black in a Red-Black tree.
  - Class: `RedBlackNode`
    Summary: Represents a node in a Red-Black tree, storing a Symbol, weight, and color.
  - Method: `RedBlackNode.__init__(self, symbol: 'Symbol', weight: Union[float, Callable[[Any], float]], color=RED)`
    Summary: Initializes a RedBlackNode with a Symbol, weight, and color.
  - Method: `RedBlackNode.eval_weight(self, *args, **kwargs) -> float`
    Summary: Evaluates the weight of the node, supporting callable weights.
  - Class: `RedBlackTree`
    Summary: Implements a self-balancing Red-Black tree for efficient insertion and traversal.
  - Method: `RedBlackTree.__init__(self)`
    Summary: Initializes an empty RedBlackTree.
  - Method: `RedBlackTree.insert(self, symbol: 'Symbol', weight: Union[float, Callable])`
    Summary: Inserts a Symbol with a given weight into the Red-Black tree.
  - Method: `RedBlackTree._bst_insert(self, z: RedBlackNode)`
    Summary: Performs a standard Binary Search Tree insertion for a RedBlackNode.
  - Method: `RedBlackTree._fix_insert(self, z: RedBlackNode)`
    Summary: Restores Red-Black tree properties after an insertion.
  - Method: `RedBlackTree._left_rotate(self, x: RedBlackNode)`
    Summary: Performs a left rotation operation on the Red-Black tree.
  - Method: `RedBlackTree._right_rotate(self, x: RedBlackNode)`
    Summary: Performs a right rotation operation on the Red-Black tree.
  - Method: `RedBlackTree.traverse_inorder(self, node: Optional[RedBlackNode] = None) -> list['Symbol']`
    Summary: Traverses the tree in-order, returning a list of Symbols.
  - Function: `_walk(n: Optional[RedBlackNode])`
    Summary: Recursively walks the Red-Black tree for in-order traversal.

### File: `symbol/builtins/visual.py`
Lines: 68
Bytes: 1800
Estimated Tokens: 450
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Class: `SymbolRender`
    Summary: Provides methods for rendering Symbol graphs into various visual formats.
  - Method: `SymbolRender.__init__(self, root: Symbol)`
    Summary: Initializes SymbolRender with the root Symbol for visualization.
  - Method: `SymbolRender.to_dot(self, mode: Literal["tree", "graph"] = "tree") -> str`
    Summary: Generates a DOT language string representation of the Symbol graph.
  - Function: `escape(sym)`
    Summary: Escapes a Symbol's name for use in DOT language.
  - Function: `walk(sym)`
    Summary: Recursively walks the Symbol graph to build the DOT string.
  - Method: `SymbolRender.to_svg(self, mode: Literal["tree", "graph"] = "tree") -> str`
    Summary: Renders the Symbol graph to an SVG image string.
  - Method: `SymbolRender.to_png(self, mode: Literal["tree", "graph"] = "tree") -> bytes`
    Summary: Renders the Symbol graph to a PNG image as bytes.
  - Function: `to_mmd(self: Symbol, mode: Literal["tree", "graph"] = "tree") -> str`
    Summary: Generates a Mermaid diagram string representation of the Symbol graph.
  - Function: `esc(sym)`
    Summary: Escapes a Symbol's name for use in Mermaid diagrams.
  - Function: `walk(sym)`
    Summary: Recursively walks the Symbol graph to build the Mermaid string.

### File: `symbol/core/__init__.py`
Lines: 1
Bytes: 1
Estimated Tokens: 1
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Summary: This file is currently empty and serves as a package initializer.

### File: `symbol/core/graph.py`
Lines: 26
Bytes: 500
Estimated Tokens: 125
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Class: `GraphTraversal`
    Summary: Implements graph and tree traversal algorithms for Symbol objects.
  - Method: `GraphTraversal.__init__(self, root: 'Symbol', mode: str = 'graph')`
    Summary: Initializes the GraphTraversal with a root Symbol and traversal mode.
  - Method: `GraphTraversal.traverse(self)`
    Summary: Initiates the graph traversal and returns the ordered list of visited Symbols.
  - Method: `GraphTraversal._walk(self, symbol: 'Symbol')`
    Summary: Recursively walks the graph, detecting and warning about cycles.

### File: `symbol/core/pluggability.py`
Lines: 60
Bytes: 1800
Estimated Tokens: 450
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Variable: `_is_frozen`
    Summary: Global flag indicating if the Symbol class is frozen.
  - Variable: `_applied_patches`
    Summary: Dictionary storing information about dynamically applied patches.
  - Variable: `log`
    Summary: Logger instance for logging pluggability-related events.
  - Function: `freeze() -> None`
    Summary: Freezes the Symbol class, preventing further runtime modifications.
  - Function: `immute() -> None`
    Summary: Makes the Symbol class immutable by removing dynamically applied methods and reclaiming memory.
  - Function: `is_frozen() -> bool`
    Summary: Returns True if the Symbol class is currently frozen.
  - Function: `register_patch(target_class: type, name: str, value: Any) -> None`
    Summary: Registers and applies a patch to a target class, tracking it for immutability.

### File: `symbol/core/symbol.py`
Lines: 170
Bytes: 4800
Estimated Tokens: 1200
Last Modified: 2025-07-01 12:00:00 (timedelta: 0:00:00)

  - Variable: `ENABLE_ORIGIN`
    Summary: Boolean flag to enable or disable origin tracking for Symbols.
  - Variable: `MEMORY_AWARE_DELETE`
    Summary: Boolean flag to enable or disable memory-aware deletion for Symbols.
  - Variable: `s`
    Summary: Global instance of SymbolNamespace for convenient Symbol creation.
  - Class: `Symbol`
    Summary: The core class representing a symbolic entity, acting as a node in a graph.
  - Method: `Symbol.__new__(cls, name: str, origin: Optional[Any] = None)`
    Summary: Creates a new Symbol instance, ensuring uniqueness based on name (Flyweight pattern).
  - Method: `Symbol.__repr__(self)`
    Summary: Returns a string representation of the Symbol for debugging.
  - Method: `Symbol.__str__(self)`
    Summary: Returns the name of the Symbol as a string.
  - Method: `Symbol.__eq__(self, other: Any) -> bool`
    Summary: Compares two Symbols for equality based on their names.
  - Method: `Symbol.__hash__(self) -> int`
    Summary: Returns the hash of the Symbol's name.
  - Method: `Symbol.__lt__(self, other)`
    Summary: Compares two Symbols based on their position for ordered collections.
  - Method: `Symbol.__add__(self, other: 'Symbol') -> OrderedSymbolSet`
    Summary: Combines two Symbols into an OrderedSymbolSet.
  - Method: `Symbol.__orjson__(self)`
    Summary: Returns the Symbol's name for orjson serialization.
  - Method: `Symbol.append(self, child: 'Symbol') -> 'Symbol'`
    Summary: Appends a child Symbol to the current Symbol's children list.
  - Method: `Symbol.add(self, child: 'Symbol') -> 'Symbol'`
    Summary: Adds a child Symbol if it's not already present.
  - Method: `Symbol.insert(self, child: 'Symbol', at: float = None) -> 'Symbol'`
    Summary: Inserts a child Symbol at a specific position.
  - Method: `Symbol.delete(self) -> None`
    Summary: Deletes the Symbol from the pool and removes its references from parents and children.
  - Method: `Symbol.pop(self) -> Optional['Symbol']`
    Summary: Removes and returns the last child Symbol.
  - Method: `Symbol.popleft(self) -> Optional['Symbol']`
    Summary: Removes and returns the first child Symbol.
  - Method: `Symbol.graph(self)`
    Summary: Traverses the Symbol's graph and returns a list of visited Symbols.
  - Method: `Symbol.tree(self)`
    Summary: Traverses the Symbol's tree structure and returns a list of visited Symbols.
  - Method: `Symbol.to_mmd(self) -> str`
    Summary: Generates a Mermaid diagram string for the Symbol's graph.
  - Function: `walk(sym)`
    Summary: Recursively walks the Symbol graph to build the Mermaid string.
  - Method: `Symbol.patch(self, other: 'Symbol') -> 'Symbol'`
    Summary: Patches the current Symbol with attributes from another Symbol.
  - Method: `Symbol.head(self, up_to_position: float = 5.0)`
    Summary: Returns the head of a sequence of numbered Symbols.
  - Method: `Symbol.tail(self, from_position: float = -10.0)`
    Summary: Returns the tail of a sequence of numbered Symbols.
  - Method: `Symbol.auto_date(cls) -> 'Symbol'`
    Summary: Class method to create a Symbol with the current date as its name.
  - Method: `Symbol.auto_datetime(cls) -> 'Symbol'`
    Summary: Class method to create a Symbol with the current datetime as its name.
  - Method: `Symbol.auto_time(cls) -> 'Symbol'`
    Summary: Class method to create a Symbol with the current time as its name.
  - Method: `Symbol.next(cls) -> 'Symbol'`
    Summary: Class method to create the next sequentially numbered Symbol.
  - Method: `Symbol.prev(cls) -> Optional['Symbol']`
    Summary: Class method to retrieve the previous sequentially numbered Symbol.
  - Method: `Symbol.first(cls) -> Optional['Symbol']`
    Summary: Class method to retrieve the first numbered Symbol.
  - Method: `Symbol.last(cls) -> Optional['Symbol']`
    Summary: Class method to retrieve the last numbered Symbol.
  - Method: `Symbol.len(cls) -> int`
    Summary: Class method to get the total count of numbered Symbols.
  - Method: `Symbol.from_enum(cls, enum_cls: enum.EnumMeta) -> list['Symbol']`
    Summary: Class method to create Symbols from an Enum's members.
  - Method: `Symbol.seek(cls, pos: float) -> Optional['Symbol']`
    Summary: Class method to find a numbered Symbol by its position.
  - Method: `Symbol.each(cls, start: Union[int, 'Symbol', None] = None) -> Iterator['Symbol']`
    Summary: Class method to iterate through numbered Symbols from a given start point.
  - Method: `Symbol.each_parents(self) -> Iterator['Symbol']`
    Summary: Iterates through the parent Symbols of the current Symbol.
  - Method: `Symbol.each_children(self) -> Iterator['Symbol']`
    Summary: Iterates through the child Symbols of the current Symbol.
  - Method: `Symbol.__enter__(self)`
    Summary: Context manager entry point for Symbol.
  - Method: `Symbol.__exit__(self, exc_type, exc_value, traceback)`
    Summary: Context manager exit point for Symbol.
  - Function: `_to_symbol(x: Any) -> 'Symbol'`
    Summary: Converts an input (Symbol, string, or object with 'name' attribute) into a Symbol.
  - Class: `SymbolNamespace`
    Summary: A utility class providing a convenient way to create Symbol instances.
  - Method: `SymbolNamespace.__getattr__(self, name)`
    Summary: Dynamically creates a Symbol when an attribute is accessed on the namespace.
  - Method: `SymbolNamespace.__getitem__(self, name)`
    Summary: Allows Symbol creation using dictionary-like item access on the namespace.
  - Method: `SymbolNamespace.__setitem__(self, name, value)`
    Summary: Prevents setting items on the SymbolNamespace, ensuring it remains read-only.
