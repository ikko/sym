### Index Callable Weight Evaluation
- cause: `TypeError` when comparing callable weight with numerical value during SymbolIndex insertion.
- reason: The `_insert` function in `SymbolIndex` was attempting to directly compare a callable `weight` with `node.eval_weight()` without evaluating the callable first.
- resolution: Modified `_insert` to evaluate the `weight` using `weight(sym)` if it's callable before comparison, ensuring a numerical value is used.
- takeaway: Always ensure that values are of compatible types before comparison, especially when dealing with dynamic or callable attributes.

### Index Callable Weight Argument Mismatch
- cause: `AttributeError` in `dynamic_weight` function during `SymbolIndex` insertion test.
- reason: The `IndexNode.eval_weight` method was modified to pass `self.symb` to the callable weight, but the test's `dynamic_weight` function was still expecting an integer argument (e.g., `10`) instead of a `Symbol` object.
- resolution: Modified `dynamic_weight` in `tests/builtins/test_index.py` to accept a `Symbol` object and derive a numerical weight from its `name` attribute (e.g., `len(sym.name) * 2`). Also, updated the assertion in the test to reflect the correct expected value from `eval_weight()`.
- takeaway: When refactoring, ensure all dependent components (like test functions) are updated to reflect changes in function signatures or expected argument types.

### Mermaid Diagram Non-Deterministic Output
- cause: `AssertionError` in `test_to_mmd_simple_tree` due to non-deterministic order of edges in Mermaid output.
- reason: Although children were sorted before appending, the recursive `walk` function in `to_mmd` could still lead to variations in the final string due to the order of recursive calls.
- resolution: Modified the `to_mmd` function in `symb/builtins/visual.py` to collect all generated lines (excluding the header) and then sort them alphabetically before joining them into the final Mermaid string. The header is prepended after sorting.
- takeaway: For deterministic output from recursive functions that build strings, especially for visual representations, consider collecting all parts and sorting them before final assembly.

### Lazy Loading of Core Components
- cause: Import errors and circular dependencies when importing `symb` due to eager loading of submodules.
- reason: Initial design loaded all submodules directly in `symb/__init__.py`, leading to issues when certain modules depended on others that were not yet fully initialized or caused circular imports.
- resolution: Implemented lazy loading for core components (`Symbol`, `s`, `GraphTraversal`) and builtins submodules in `symb/__init__.py`. This defers the actual import until the component is first accessed, resolving import order issues and optimizing initial load times.
- takeaway: For complex Python packages with interdependencies, lazy loading can be an effective strategy to manage import order, prevent circular dependencies, and optimize initial load times. This requires careful consideration of `__getattr__` and `__all__` in `__init__.py` files.
