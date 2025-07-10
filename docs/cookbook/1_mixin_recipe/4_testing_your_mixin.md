# [`«symb»`](https://github.com/ikko/symb) cookbook

**Recipes for Symbolic Mastery**

_Recipe 1: How to Create a Mixin?_

---

# 1.4 Testing Your Mixin: Ensuring Robustness

Thoroughly testing your mixins is crucial to ensure their correctness, reliability, and proper integration within the `symb` framework. This section outlines best practices for testing mixins, covering both synchronous and asynchronous functionalities.

## Principles of Mixin Testing

1.  **Isolation:** Test the mixin's logic in isolation as much as possible. While a mixin is designed to extend a `Symbol`, its core functionality should be verifiable independently.
2.  **Integration:** Test how the mixin integrates with `Symbol` objects and how its methods behave when called through a `Symbol` instance.
3.  **Edge Cases:** Cover edge cases, such as empty graphs, symbs with no children, or complex graph structures.
4.  **Asynchronous Behavior:** For asynchronous methods, use `anyio`'s testing utilities (e.g., `@pytest.mark.anyio`) to properly manage the asynchronous execution context.

## Example: Testing the `DescendantCounterMixin`

Let's create a test file (e.g., `tests/test_descendant_counter_mixin.py`) for the `DescendantCounterMixin` we implemented earlier.

```python
# tests/test_descendant_counter_mixin.py

import pytest
import anyio
from symb import Symbol
from my_counter_mixin import DescendantCounterMixin # Assuming my_counter_mixin.py is in your PYTHONPATH

@pytest.fixture
def sample_symb_graph():
    # A
    # |\
    # B C
    # |
    # D
    # E (independent)
    a = Symbol("A")
    b = Symbol("B")
    c = Symbol("C")
    d = Symbol("D")
    e = Symbol("E")

    a.append(b)
    a.append(c)
    b.append(d)
    # c.append(d) # D is also a descendant of C, but only counted once

    return a, b, c, d, e

def test_count_descendants_sync(sample_symb_graph):
    a, b, c, d, e = sample_symb_graph

    # Test A: should have B, C, D as descendants (3 unique)
    mixin_a = DescendantCounterMixin(a)
    assert mixin_a.count_descendants() == 3

    # Test B: should have D as descendant (1 unique)
    mixin_b = DescendantCounterMixin(b)
    assert mixin_b.count_descendants() == 1

    # Test C: should have no descendants in this specific graph setup
    mixin_c = DescendantCounterMixin(c)
    assert mixin_c.count_descendants() == 0

    # Test D and E: no descendants
    mixin_d = DescendantCounterMixin(d)
    assert mixin_d.count_descendants() == 0
    mixin_e = DescendantCounterMixin(e)
    assert mixin_e.count_descendants() == 0

@pytest.mark.anyio
async def test_a_count_descendants_async(sample_symb_graph):
    a, b, c, d, e = sample_symb_graph

    # Test A
    mixin_a = DescendantCounterMixin(a)
    assert await mixin_a.a_count_descendants() == 3

    # Test B
    mixin_b = DescendantCounterMixin(b)
    assert await mixin_b.a_count_descendants() == 1

    # Test C
    mixin_c = DescendantCounterMixin(c)
    assert await mixin_c.a_count_descendants() == 0

    # Test D and E
    mixin_d = DescendantCounterMixin(d)
    assert await mixin_d.a_count_descendants() == 0
    mixin_e = DescendantCounterMixin(e)
    assert await mixin_e.a_count_descendants() == 0

# Example of testing integration if mixin methods were directly applied to Symbol
# This would depend on how mixins are applied in your specific Symbol setup
# @pytest.mark.anyio
# async def test_symb_with_mixin_integration(sample_symb_graph):
#     a, _, _, _, _ = sample_symb_graph
#     # Assuming a mechanism to apply mixin methods directly to Symbol instances
#     # For example, if Symbol had an 'apply_mixin' method:
#     # a.apply_mixin(DescendantCounterMixin)
#     # assert a.count_descendants() == 3
#     # assert await a.a_count_descendants() == 3
```

**Explanation:**

*   **`@pytest.fixture` `sample_symb_graph`:** This fixture sets up a consistent `Symbol` graph for all tests, ensuring reproducibility.
*   **`test_count_descendants_sync`:** This test function verifies the synchronous `count_descendants` method for various `Symbol` instances within the graph.
*   **`@pytest.mark.anyio` `test_a_count_descendants_async`:** This test function verifies the asynchronous `a_count_descendants` method. The `@pytest.mark.anyio` decorator is essential for running asynchronous test functions.
*   **Assertions:** We use `assert` statements to compare the actual results from the mixin methods with the expected values.

## Running the Tests

To run these tests, ensure you have `pytest` and `anyio` installed (`pip install pytest anyio`). Then, navigate to your project's root directory in the terminal and run:

```bash
pytest tests/test_descendant_counter_mixin.py
```

This will execute the tests and report any failures. Comprehensive testing ensures that your mixin behaves as expected and integrates seamlessly with the `symb` framework.
