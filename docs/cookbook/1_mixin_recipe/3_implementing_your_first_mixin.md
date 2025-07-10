# [`«symb»`](https://github.com/ikko/symb) cookbook
**Recipes for Symbolic Mastery**

_Recipe 1: How to Create a Mixin?_

---

# 1.3 Implementing Your First Mixin: A Practical Example

Let's walk through a practical example of creating a simple mixin for the `symb` framework. This mixin will add a new capability to `Symbol` objects: the ability to count the total number of descendants (children, grandchildren, etc.) in their respective sub-graphs.

## Step 1: Define the Mixin Class

Create a new Python file (e.g., `my_counter_mixin.py`) and define your mixin class. Remember to import `Symbol` and any other necessary modules.

```python
# my_counter_mixin.py

from symb.core.base_symb import Symbol
from typing import Set

class DescendantCounterMixin:
    def __init__(self, symb_instance: Symbol):
        self.symb = symb_instance

    def count_descendants(self) -> int:
        """Counts the total number of unique descendants for this symb."""
        seen_symbs: Set[Symbol] = set()
        queue = list(self.symb.children)

        while queue:
            current_symb = queue.pop(0)
            if current_symb not in seen_symbs:
                seen_symbs.add(current_symb)
                for child in current_symb.children:
                    queue.append(child)
        return len(seen_symbs)

    async def a_count_descendants(self) -> int:
        """Asynchronously counts the total number of unique descendants for this symb."""
        # For simplicity, this async version just calls the sync version
        # In a real-world scenario, this might involve async I/O or CPU-bound tasks
        # that are offloaded to a thread pool using anyio.to_thread.run_sync
        return self.count_descendants()

```

**Explanation:**

*   The `DescendantCounterMixin` class takes a `symb_instance` in its `__init__`, storing a reference to the `Symbol` it's extending.
*   `count_descendants` is a synchronous method that performs a breadth-first search to find all unique descendants.
*   `a_count_descendants` is the asynchronous counterpart. For this simple example, it just calls the synchronous version. In a more complex scenario, you might use `anyio.to_thread.run_sync` to offload heavy computation to a thread pool, or perform actual asynchronous operations.

## Step 2: Apply the Mixin to a Symbol

To use your mixin, you need to apply it to a `Symbol` instance. The `symb` framework provides mechanisms for this, often through a dedicated `apply_mixin` function or by directly instantiating the mixin with the `Symbol`.

For demonstration purposes, let's assume a direct application:

```python
# main.py (or a test file)

from symb import Symbol
from my_counter_mixin import DescendantCounterMixin

# Create some symbs to form a graph
a = Symbol("A")
b = Symbol("B")
c = Symbol("C")
d = Symbol("D")
e = Symbol("E")

a.append(b)
a.append(c)
b.append(d)
c.append(e)
c.append(d) # D is also a descendant of C

# Apply the mixin to Symbol A
a_with_counter = DescendantCounterMixin(a)

# Now you can call the mixin methods through the mixin instance
print(f"Symbol A has {a_with_counter.count_descendants()} descendants.")

# For asynchronous methods, use await
async def main():
    print(f"Symbol A has {await a_with_counter.a_count_descendants()} descendants (async).")

if __name__ == "__main__":
    import anyio
    anyio.run(main)
```

**Expected Output:**

```
Symbol A has 4 descendants.
Symbol A has 4 descendants (async).
```

**Explanation:**

*   We create a sample `Symbol` graph.
*   An instance of `DescendantCounterMixin` is created, passing `Symbol A` to its constructor.
*   We then call `count_descendants()` and `a_count_descendants()` on the `a_with_counter` instance. Note that the `Symbol` framework typically integrates mixins such that their methods appear directly on the `Symbol` object itself (e.g., `a.count_descendants()`). The direct instantiation shown here is for illustrative purposes of the mixin's structure.

This example demonstrates the basic process of defining a mixin and applying it to a `Symbol` object. The next step will involve writing tests to ensure your mixin behaves as expected.
