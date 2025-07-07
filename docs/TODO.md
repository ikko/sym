$ cat docs/TODO.md
# Test Coverage TODO List

This document outlines tests that were removed or skipped, indicating areas where test coverage needs to be re-evaluated and potentially re-implemented. It also tracks the progress towards achieving 75% overall test coverage.

Update coverage info, may be updated

## Current Coverage: 37%

## Target Coverage: 55%

## Plan to Increase Coverage to 55%

To achieve the target coverage, I will focus on adding tests for the following modules and functionalities, prioritizing core components and areas with very low coverage:

### Phase 1: Core Symbol and Data Structures

1. [ ]  **`symbol/core/symbol.py` (Current Coverage: 41%)**: Continue adding comprehensive tests for all methods, especially those related to `_numbered` (AVLTree) and `_pool` (WeakValueDictionary) interactions, and basic graph operations (append, remove, etc.).
2. [ ]  **`symbol/core/base_symbol.py` (Current Coverage: 96%)**: Review existing tests and add any missing edge cases or scenarios to reach 100% coverage. (Already high, will revisit if needed after other modules).
3. [ ]  **`symbol/builtins/avl_tree.py` (Current Coverage: 64%)**: Implement detailed tests for insertion, deletion, rebalancing, and traversal methods of the AVLTree.
4. [ ]  **`symbol/builtins/red_black_tree.py` (Current Coverage: 57%)**: Implement comprehensive tests for all Red-Black Tree operations.
5. [ ]  **`symbol/builtins/index.py` (Current Coverage: 90%)**: Add tests for various indexing scenarios and methods.

### Phase 2: Key Features and Utilities

1. [ ]  **`symbol/core/maturing.py` (Current Coverage: 95%)**: Develop extensive tests for the merge algorithm, covering different merge strategies and complex data structures.
2. [ ]  **`symbol/core/schedule.py` (Current Coverage: 0%)**: Add more tests for scheduling various types of jobs (one-off, recurring, async, sync) and edge cases.
3. [ ]  **`symbol/core/batch_processing.py` (Current Coverage: 31%)**: Re-implement and expand tests for synchronous and asynchronous batch processing, including new thread/process scenarios.
4. [ ]  **`symbol/builtins/time_dim.py` (Current Coverage: 36%)**: Add tests for remaining time dimension functionalities, including filtering and time-based operations.
5. [ ]  **`symbol/builtins/visual.py` (Current Coverage: 24%)**: Add more tests for visual rendering, especially for different graph modes and output formats.
6. [ ]  **`symbol/core/lazy_symbol.py` (Current Coverage: 52%)**: Add more tests for lazy evaluation and its interactions with other Symbol functionalities.
7. [ ]  **`symbol/core/symbolable.py` (Current Coverage: 0%)**: Investigate the purpose of this module and add appropriate tests.
8. [ ]  **`symbol/core/time_arithmetics.py` (Current Coverage: 22%)**: Add tests for all time arithmetic operations.

### Ongoing Tasks

* [ ]  **Address Skipped Tests**: Install Graphviz to enable `test_a_to_svg_simple_tree`. Re-evaluate and enable `test_recurring_async_job` in `test_async_schedule.py`.
* [ ]  **Review and Refactor**: Continuously review existing tests for clarity, efficiency, and completeness. Refactor as needed.


Tests to assemble: Test happy path ONLY! Aim for simplicity. Planned files represent functionality that should eventually be tested with a more robust approach.

* [ ] **`tests/builtins/test_time_dim.py`**: * `test_symbol_head_and_tail`: This test covered the
    `time_head` and `time_tail` properties of `SymbolTimeDimMixin`, which provide chronological
    views of symbols. * `test_symbol_period_properties`: This test covered various period-related
    properties (`period`, `as_period`, `duration`, `as_duration`, `delta`, `as_delta`) of
    `SymbolTimeDimMixin`.

* [ ] **`tests/builtins/test_visual.py`**: * `test_a_to_png_simple_tree`: This test shpuld cover the
    asynchronous PNG rendering functionality of `SymbolRender`. Skip if cannot install package dependencies with `uv add pypthon-package`

* [ ]   **`tests/core/test_async_schedule.py`**:
    * [ ]   `test_async_job_scheduling`: This test will cover the scheduling of asynchronous jobs within the `Scheduler`.

* [ ]   **`tests/core/test_batch_processing.py`**:
    * [ ]   `test_a_process_batch_async_direct`: This test will cover asynchronous batch processing with direct execution.
    * [ ]   `test_a_process_batch_async_new_thread`: This test will cover asynchronous batch processing with execution in new threads.
    * [ ]   `test_a_process_batch_sync_func_async_context`: This test will cover synchronous functions executed within an asynchronous context during batch processing.

* [ ] **`tests/core/test_symbol_pop.py`**:
    * [ ]`test_pop_reparents_children`: This test should cover the `pop()` method's functionality to reparent children when a symbol is removed.

* [ ] **`tests/test_conversion/test_conversions.py`**:
    * [ ]`test_nested_conversion`: This test will cover the conversion of nested data structures (dictionaries and lists) into Symbol objects.

* [ ] **`tests/core/test_base_symbol.py`**:
    * [ ]`test_symbol_less_than_comparison_type_error`: Test and type of `__lt__`, ensure  `__slots__` and `WeakValueDictionary`.

* [ ] **`tests/builtins/test_index.py`**:
    * [ ]`test_symbol_index_remove`: Analyse the AVLTree, with it's remove operation. Then write test.
    * [ ]`test_symbol_index_remove_non_existent`: Use knowledge from `test_symbol_index_remove`.

* [ ] **`tests/builtins/test_red_black_tree.py`**:
    * [ ]`test_rb_tree_insert_scenarios`: This test should test end state only. Don't assert internal tree states.

## Skipped Tests

These tests are currently skipped due to external dependencies or temporary reasons. they should be enabled and addressed once the underlying issues are resolved.

* [ ] **`tests/builtins/test_visual.py`**:
    * [ ]`test_a_to_svg_simple_tree`: Skipped because Graphviz 'dot' executable was not found. This test covers asynchronous SVG rendering.

* [ ] **`tests/core/test_async_schedule.py`**:
    * [ ]`test_recurring_async_job`: Temporarily skipped. Leave it skipped. This test covers the functionality of recurring asynchronous jobs.

## Progress on Test Coverage

* [ ] **`symbol/core/base_symbol.py`**: Achieved 96% coverage. All tests passing.
* [ ] **`symbol/core/symbol.py`**: Achieved 41% coverage. All tests passing.
* [ ] **`symbol/builtins/avl_tree.py`**: Achieved 64% coverage. All tests passing.
* [ ] **`symbol/builtins/index.py`**: Achieved 90% coverage. All tests passing.
* [ ] **`symbol/builtins/red_black_tree.py`**: Achieved 57% coverage. All tests passing.
* [ ] **`symbol/core/maturing.py`**: Achieved 95% coverage. All tests passing.


This structured approach will allow for systematic improvement of test coverage and overall code quality. Update this document regularly to reflect progress.

