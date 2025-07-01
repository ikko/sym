# Unit Testing - Happy Path Plan

This document outlines the plan for implementing happy path unit tests for the `symbol` library. The goal is to ensure core functionalities work as expected under typical, valid input conditions.

## Objective
Ensure the core functionalities of the `symbol` library and its primary built-in extensions work as expected under typical, valid input conditions.

## Scope
*   `symbol.core.symbol.Symbol`: Core Symbol creation, manipulation, and basic graph operations.
*   `symbol.core.mixinability`: Freezing and unfreezing Symbol class.
*   `symbol.builtins.collections.OrderedSymbolSet`: Basic set operations.
*   `symbol.builtins.datetime.SymbolDateTimeMixin`: Date/time parsing and basic time-based queries.
*   `symbol.builtins.index.SymbolIndex`: Basic index and traversal.
*   `symbol.builtins.path.SymbolPathMixin`: Basic pathfinding and matching.
*   `symbol.builtins.visual.SymbolRender`: Basic Mermaid diagram generation.

## Approach
1.  For each module/class/function in scope, identify the primary "happy path" scenarios.
2.  Write unit tests that cover these scenarios, asserting expected outcomes.
3.  Utilize `pytest` as the testing framework.
4.  Maintain this `docs/TODO.md` file to track progress.

## Test Cases and Progress

### Phase 1: Core Symbol Functionality (`symbol/core/symbol.py`)
*   [x] Test `Symbol` creation and interning (`Symbol("name")`).
*   [x] Test `Symbol` equality (`==`) and hashing (`hash()`).
*   [x] Test `Symbol` string representation (`__str__`, `__repr__`).
*   [x] Test `Symbol` basic graph operations: `append`, `add`, `children`, `parents`.
*   [x] Test `SymbolNamespace` (`s.name`, `s["name"]`).

### Phase 2: Mixinability (`symbol/core/mixinability.py`)
*   [x] Test `freeze()` and `is_frozen()` states.
*   [x] Test `register_patch()` (basic application).

### Phase 3: Built-in Collections (`symbol/builtins/collections.py`)
*   [x] Test `OrderedSymbolSet` creation and `add` method.
*   [x] Test `OrderedSymbolSet` iteration, length, and containment.

### Phase 4: Built-in Datetime (`symbol/builtins/datetime.py`)
*   [ ] Test `SymbolDateTimeMixin._parse_timestamp` with valid timestamps.
*   [ ] Test `SymbolDateTimeMixin.as_date`, `as_time`, `as_datetime`.
*   [ ] Test `SymbolDateTimeMixin.head` and `tail` with simple sequences.

### Phase 5: Built-in Indexing (`symbol/builtins/index.py`)
*   [ ] Test `SymbolIndex` insertion (`insert`).
*   [ ] Test `SymbolIndex.traverse` (in-order) with a simple tree.

### Phase 6: Built-in Path (`symbol/builtins/path.py`)
*   [ ] Test `SymbolPathMixin.path_to` for a direct path.
*   [ ] Test `SymbolPathMixin.match` with a simple predicate.

### Phase 7: Built-in Visual (`symbol/builtins/visual.py`)
*   [ ] Test `SymbolRender.to_mmd` for a simple Symbol graph.
