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
    -   [x] Create `symbol/core/pluggability.py` with `freeze()`, `immute()`, and `is_frozen()`.
    -   [x] Integrate `register_patch()` in `symbol/builtins/__init__.py` to track applied patches.
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

-   [ ] **Rename Terminology**: Replace "pluggable" with "mixinable" and "plugins" with "mixins" throughout codebase and documentation.
-   [ ] **Origin Ref Task**: Add `.ref` as alias of `.origin`.
-   [ ] **Introduce `Symbolable` Type**:
    -   [ ] Replaces current callable handling.
    -   [ ] Official interface for callables, enabling lambdas.
    -   [ ] Explore `LibCST` for implementation.
-   [ ] **Formalize Mixin Interface**:
    -   [ ] `async def a_function(function_name, *args, new_process=False, new_thread=True, **params, returns, returns_type) -> TODO: work on it.`
    -   [ ] Cast returns to `returns_type` before returning.
-   [ ] **Batch Processing**: Implement a more general concept of batch transforming, handling batches consistently throughout the module.
-   [ ] **Mixin Manipulation of Symbol**: Confirm implicit `self` manipulation for mixins.
