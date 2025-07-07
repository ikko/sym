# Test Coverage TODO List

This document outlines tests that were removed or skipped, indicating areas where test coverage needs to be re-evaluated and potentially re-implemented.

## Removed Tests (due to complexity/failure)

The following tests were removed because they were failing or deemed overly complex in their current implementation. They represent functionality that should eventually be re-tested with a more robust approach.

*   **`tests/builtins/test_time_dim.py`**:
    *   `test_symbol_head_and_tail`: This test covered the `time_head` and `time_tail` properties of `SymbolTimeDimMixin`, which provide chronological views of symbols.
    *   `test_symbol_period_properties`: This test covered various period-related properties (`period`, `as_period`, `duration`, `as_duration`, `delta`, `as_delta`) of `SymbolTimeDimMixin`.

*   **`tests/builtins/test_visual.py`**:
    *   `test_a_to_png_simple_tree`: This test covered the asynchronous PNG rendering functionality of `SymbolRender`.

*   **`tests/core/test_async_schedule.py`**:
    *   `test_async_job_scheduling`: This test covered the scheduling of asynchronous jobs within the `Scheduler`.

*   **`tests/core/test_batch_processing.py`**:
    *   `test_a_process_batch_async_direct`: This test covered asynchronous batch processing with direct execution.
    *   `test_a_process_batch_async_new_thread`: This test covered asynchronous batch processing with execution in new threads.
    *   `test_a_process_batch_sync_func_async_context`: This test covered synchronous functions executed within an asynchronous context during batch processing.

*   **`tests/core/test_symbol_pop.py`**:
    *   `test_pop_reparents_children`: This test covered the `pop()` method's functionality to reparent children when a symbol is removed.

*   **`tests/test_conversion/test_conversions.py`**:
    *   `test_nested_conversion`: This test covered the conversion of nested data structures (dictionaries and lists) into Symbol objects.

## Skipped Tests

These tests are currently skipped due to external dependencies or temporary reasons. They should be enabled and addressed once the underlying issues are resolved.

*   **`tests/builtins/test_visual.py`**:
    *   `test_a_to_svg_simple_tree`: Skipped because Graphviz 'dot' executable was not found. This test covers asynchronous SVG rendering.

*   **`tests/core/test_async_schedule.py`**:
    *   `test_recurring_async_job`: Temporarily skipped. This test covers the functionality of recurring asynchronous jobs.

## Next Steps

The immediate next step is to systematically re-evaluate the functionality covered by the removed tests and design new, more robust tests for them. For the skipped tests, the external dependencies (Graphviz) should be installed, or the temporary skip reasons addressed. This will ensure comprehensive and balanced test coverage for the `symbol` library.
