# Project `symbol` TODO List

This document outlines the development tasks and areas for improvement for the `symbol` project.

## Core Functionality

### Implement a Safe `.pop()` Method

-   [x] **Develop a `.pop()` method for `Symbol` objects.**
    -   The method should safely remove a `Symbol` from its hierarchy.
    -   **Re-parenting Logic:** Before removal, it must connect the children of the removed `Symbol` to its parent (i.e., connect grandchildren to grandparents). This should handle arbitrary chain lengths, effectively shortcutting the removed link.
    -   **Cascading Deletes:** Ensure that when a `Symbol` is popped, all associated resources are freed up. This includes cleaning up any memory that was cascaded by the delete operation.
    -   **Re-binding Linear Sequence:** Ensure that `_prev` and `_next` pointers of adjacent symbols are correctly re-bound.
    -   **Re-binding Tree Structures:** Ensure that `.left` and `.right` pointers in `SymbolIndex` are correctly re-bound.
    -   **Manage `related_to` and `related_how` lists:** Implement `relate` and `unrelate` methods to manage bidirectional relationships, ensuring consistency upon symbol deletion.
    

## Memory Management

-   [x] **Proactive Memory Cleanup:**
    -   Implement mechanisms to release memory for `Symbol` objects that are no longer needed, without waiting for the Garbage Collector (GC).
    -   The goal is to maintain a tight memory footprint for the `symbol` library.
-   [x] **Implement `.footprint()` Method:**
    -   Create a `.footprint()` method to calculate the byte size of a `Symbol` object and its children.
    -   Provide arguments to control the calculation for ambiguous or complex object graphs (e.g., how to handle shared objects, depth of calculation).

## Performance and Optimization

-   [x] **Lazy Evaluation:**
    -   Review the codebase to ensure that computations are deferred until their results are needed (lazy evaluation).
    -   Identify and refactor any parts of the code that are unnecessarily eager.
-   [x] **Merge Algorithm Improvement:**
    -   Analyze the existing merge algorithm(s) used in the `symbol` project.
    -   Identify areas for optimization and recommend improvements. This could involve algorithmic changes or implementation tweaks.
-   [x] **General Optimization:**
    -   Conduct a performance analysis of the codebase to identify bottlenecks.
    -   Recommend specific areas for optimization.
        -   **Optimize List Operations for Relationships:** Consider `set` or other data structures for `parents` and `children` if order is not critical, or `collections.deque` for efficient appends/pops. Profile for bottlenecks.
        -   **Consider `__slots__` for Memory Efficiency:** Evaluate for `Symbol` and `BaseSymbol` to reduce memory footprint and speed up attribute access.
        -   **Iterative vs. Recursive Graph Traversal:** Refactor deep recursive graph traversal methods to use iterative approaches with explicit stacks/queues.
        -   **Profiling for Specific Bottlenecks:** Use `cProfile` or `line_profiler` to identify exact performance hot spots.

## Concurrency

-   [x] **Thread Safety:**
    -   Audit the codebase for thread safety.
    -   Implement necessary locking or other concurrency control mechanisms to ensure that `Symbol` objects can be safely used in multi-threaded environments.
