## `symbol.core.batch_processing` Module

This module provides functions for processing batches of items asynchronously and synchronously, with support for parallel execution using threads or processes.

### Function: `a_process_batch(batch: Iterable[T], func: Callable[[T], Union[U, Awaitable[U]]], new_process: bool = False, new_thread: bool = True) -> List[U]`
*   **Description**: Asynchronously processes a batch of items using the given function. It supports running the function in new threads or (conceptually) new processes.
*   **Parameters**:
    *   `batch` (`Iterable[T]`): An iterable of items to process.
    *   `func` (`Callable[[T], Union[U, Awaitable[U]]]`): An async or sync function to apply to each item.
    *   `new_process` (`bool`): If `True`, attempts to run each item's processing in a new process. Currently, this falls back to thread/direct execution with a warning. Defaults to `False`.
    *   `new_thread` (`bool`): If `True`, runs each item's processing in a new thread. This is ignored if `new_process` is `True`. Defaults to `True`.
*   **Returns**: `List[U]` - A list of results from processing each item. (Note: Current implementation includes a placeholder for result collection).

### Function: `process_batch(batch: Iterable[T], func: Callable[[T], U], new_process: bool = False, new_thread: bool = True) -> List[U]`
*   **Description**: Synchronously processes a batch of items using the given function. It supports running the function in new threads or (conceptually) new processes.
*   **Parameters**:
    *   `batch` (`Iterable[T]`): An iterable of items to process.
    *   `func` (`Callable[[T], U]`): A sync function to apply to each item.
    *   `new_process` (`bool`): If `True`, attempts to run each item's processing in a new process. Currently, this falls back to thread/direct execution with a warning. Defaults to `False`.
    *   `new_thread` (`bool`): If `True`, runs each item's processing in a new thread. This is ignored if `new_process` is `True`. Defaults to `True`.
*   **Returns**: `List[U]` - A list of results from processing each item.

---
