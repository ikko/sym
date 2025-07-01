# TODO - Project Symbol

This document tracks the development and refactoring tasks for the project.

### Phase 1: Refactoring and Consolidation

-   [x] **Reorganize Directory Structure**:
    -   [x] Create a `core` directory for essential components (`symbol.py`, `graph.py`).
    -   [x] Create a `builtins` directory for modular extensions (`datetime.py`, `indexing.py`, `visual.py`, `collections.py`).
    -   [x] Move existing files into the new structure.
-   [x] **Consolidate Redundant Code**:
    -   [x] Merge `symbol_render.py` and `symbol_visual.py` into a single `builtins/visual.py`.
    -   [x] Delete `symbol_backup_phase_one.py`.
    -   [x] Delete `symbol_datetime_arithmetics.py` and `symbol_datetime_grouping.py` (merged into `builtins/datetime.py`).
-   [x] **Complete `avl_tree.py` implementation**.

### Phase 2: API Refinement and Mixinability

-   [x] **Implement Runtime Mixinability**:
    -   [x] Create `symbol/core/mixinability.py` with `freeze()`, `immute()`, and `is_frozen()`.
    -   [x] Integrate `register_mixin()` in `symbol/builtins/__init__.py` to track applied mixins.
    -   [x] Expose `freeze`, `immute`, `is_frozen` at the top-level `symbol` package.
-   [x] **Refine User-Facing API**:
    -   [x] Rename global `S` instance to `s`.
    -   [x] Create top-level aliases for built-in modules (e.g., `symbol.datetime`, `symbol.dt`).

### Phase 3: Documentation and Tooling

-   [x] **Generate Code Inventory**:
    -   [x] Create `scripts/generate_code_inventory.py` using `ast` module for precise analysis.
    -   [x] Generate and save comprehensive code inventory to `docs/methods.md` with LLM-generated summaries for undocumented items.
-   [ ] **Update `README.md`**:
    -   [ ] Add project summary and core concepts.
    -   [ ] Add user-facing examples for all major features.
    -   [ ] Add the ESG/Sustainability example.
    -   [ ] Add a Mermaid diagram visualizing the architecture.
-   [ ] **Update `AGENT_CONTEXT.md`**:
    -   [ ] Reflect the new, refactored structure of the project.
-   [ ] **Finalize `GLOSSARY.md`**:
    -   [ ] Review and expand definitions as new patterns are introduced.

### Phase 4: Advanced Features and Standards

-   [x] **Formalize Mixin Interfaces**:
    -   [x] Create `symbol/core/protocols.py` with `Protocol` definitions for mixins.
    -   [x] Update mixin classes to inherit from their respective protocols.
-   [x] **Establish Asynchronous Strategy**:
    -   [x] Implement `a_` prefixed async functions with synchronous wrappers in `symbol/builtins/visual.py`.
    -   [x] Ensure heavy dependencies like `graphviz` are optional.
    -   [x] All graph constructs (`GraphTraversal`, `Symbol`, `SymbolIndex`, `RedBlackTree`, `AVLTree`) must have a working `.to_ascii` method.
    -   [x] Proxy all non-hidden functions from `symbol.builtins.visual` to `symbol.visual`.

### Phase 5: Maturing and Memory Management

-   [x] **Introduce `.maturing` Module**:
    -   [x] Create `symbol/core/maturing.py`.
    -   [x] Implement `DefDict` (defaultdict of defaultdict) for `symbol.metadata`.
    -   [x] Implement `deep_del()` for memory-aware cleanup.
-   [x] **Implement `elevate()` Method**:
    -   [x] Takes keys from `metadata` and defines them as instance methods/attributes of `Symbol`.
    -   [x] Supports various `merge_strategy` options (e.g., `symbol.patch`, `copy`, `deepcopy`, `pipe`, `update`, `extend`, `smooth`).
    -   [x] `smooth` merge: BFS walk, for dicts add as sibling, recursive for subdirs.
    -   [x] On successful `elevate`, clear corresponding keys from `metadata`.
    -   [x] Issue warnings for internal method overwrites.
-   [x] **Implement `symbol.context` Attribute**:
    -   [x] A `DefDict` attribute that mirrors `metadata` but is subject to `deep_del` on Symbol changes.
    -   [x] Implement `clear_context()` for explicit memory-aware deletion.
-   [x] **Refine `immute()` Method**:
    -   [x] Orchestrates `elevate()`, `slim()`, and `freeze()`.
    -   [x] `slim()`: Identifies and detaches unused mixins/attributes, performing `del` before unassignment.

### Phase 6: Advanced Type Handling and Mixin Interface

-   [x] **Rename Terminology**: Replace "pluggable" with "mixinable" and "plugins" with "mixins" throughout codebase and documentation.
-   [x] **Origin Ref Task**: Add `.ref` as alias of `.origin`.
-   [x] **Introduce `Symbolable` Type**:
    -   [x] Create `symbol/core/symbolable.py`.
    -   [x] Define `Symbolable` Protocol for callable objects.
    -   [x] Implement `symbol/core/mixin_validator.py` using `LibCST` for static analysis.
    -   [x] Integrate `validate_mixin_callable` into `register_mixin` for robust validation.
    -   [x] **Robustness**: Implement `try-except` for third-party code, ensure graceful degradation (warnings, state restoration).
    -   [x] **Monitoring**: Initial monitoring during integration (logging success/failure of mixin application).
-   [x] **Formalize Mixin Interface**:
    -   [x] Define `MixinFunction` Protocol in `symbol/core/protocols.py`.
    -   [x] Enhance `register_mixin` to enforce `MixinFunction` protocol.
    -   [x] **Developer Experience**: Design for easy, unambiguous, self-explanatory mixin registration.
    -   [x] **Debugger Friendly**: Construct a debugger-friendly, inspectable process with well-instructed error handling.
-   [x] **New Feature: `.timeline` Module**:
    -   [x] Create `symbol/builtins/timeline.py`.
    -   [x] Define `Timeline` as a series of periods, structurable with existing hierarchies.
    -   [x] Implement meaningful constructors and operations (e.g., `overlap`).
    -   [x] Implement conversions and operations with other point-in-time and time-delta objects.
    -   [x] Add arithmetic operators to a separate file (e.g., `symbol/core/time_arithmetics.py`) to cover foundational methods for meeting organizers, calendars, etc.
-   [x] **Batch Processing**: Implement a more general concept of batch transforming, handling batches consistently throughout the module.
-   [x] **Mixin Manipulation of Symbol**: Confirm implicit `self` manipulation for mixins.
