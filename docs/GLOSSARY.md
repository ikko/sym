# Glossary of Design and Algorithmic Patterns

This document outlines the key design, arithmetic, and algorithmic patterns employed within the Symbol project.

### Core Design Patterns

-   **Flyweight Pattern**
    -   **Description**: Ensures that a `Symbol` with a specific name is created only once. A central pool (`Symbol._pool`) stores and reuses symbol objects. This pattern is crucial for memory efficiency and for ensuring that identical symbols are referentially equal (`s.a is s.a`).
    -   **Implementation**: The `Symbol.__new__` method intercepts object creation, checks the pool for an existing instance with the given name, and returns it if found. Otherwise, it creates a new object and adds it to the pool.

-   **Mixin Architecture & Monkey-Patching**
    -   **Description**: The core `Symbol` class is intentionally lean. Extended functionalities (e.g., date/time operations, pathfinding) are defined in separate "mixin" classes. These functionalities are then dynamically "patched" onto the `Symbol` class at runtime, allowing for a highly modular and extensible system.
    -   **Implementation**: Modules like `symbol_datetime.py` define classes such as `SymbolDateTimeMixin`. The final lines of the `symbol.py` module explicitly assign methods and properties from these mixins to the `Symbol` class itself.

-   **Per-Instance Weighted Tree Indexing**
    -   **Description**: Each `Symbol` instance contains a `SymbolIndex` attribute, which is a self-contained, weighted binary search tree. This allows a symbol to maintain a private, ordered index of other symbols or functions, where the ordering is determined by a dynamic weight. The index is re-balanceable, with support for AVL and Red-Black tree algorithms to maintain performance.
    -   **Implementation**: `symbol_index.py` defines the `SymbolIndex` and `IndexNode` classes. An instance of `SymbolIndex` is created and assigned to `self.index` within `Symbol.__new__`.

-   **Proxy Pattern via `__getattr__`**
    -   **Description**: The `SymbolIndex` acts as a functional proxy. When an attribute is accessed on the index that doesn't exist on the `SymbolIndex` itself, the `__getattr__` method intercepts the call. It looks up the attribute in its internal function map and, if found, executes it, potentially with "before" and "after" hooks.
    -   **Implementation**: The `SymbolIndex.__getattr__` method provides this dynamic dispatch, enabling syntax like `my_symbol.index.some_function()`.

-   **Namespace-as-Factory**
    -   **Description**: To simplify the creation of symbols and enhance code readability, a special `SymbolNamespace` object (`S`) is provided. Accessing any attribute on this object (e.g., `s.my_new_symbol`) automatically creates a `Symbol` with that name.
    -   **Implementation**: The `SymbolNamespace` class implements `__getattr__` and `__getitem__` to intercept attribute access and instantiate a `Symbol` with the requested name.

### Algorithmic Patterns

-   **Self-Balancing Binary Search Trees (AVL & Red-Black)**
    -   **Description**: To ensure that the `SymbolIndex` remains efficient even with many entries, we use standard self-balancing tree algorithms. These algorithms automatically restructure the tree during insertions to keep its height logarithmic with respect to the number of nodes, guaranteeing `O(log n)` performance for search, insert, and delete operations.
    -   **Implementation**: `red_black_tree.py` and `avl_tree.py` (when complete) provide the core logic for these data structures, which are used by `SymbolIndex.rebalance`.

-   **Depth-First Search (DFS) Traversal**
    -   **Description**: The default graph traversal and pathfinding mechanism is a recursive Depth-First Search. It explores as far as possible along each branch before backtracking. It includes cycle detection to prevent infinite loops in non-tree graphs.
    -   **Implementation**: `graph_traversal.py` provides the `GraphTraversal` class, used by `Symbol.graph()` and `Symbol.tree()`.
