## `symb.core.batch_processing` Module


> ⚠ _This module is under development and incomplete. Features may differ from what's written here. Should you use it, test comprehensively, especially before using `async batch` features_
 

This module provides functions for processing batches of items asynchronously and synchronously, with support for parallel execution using threads or processes. 



### Function: `a_process_batch`
```python
async def a_process_batch(batch: Iterable[T], func: Callable[[T], Union[U, Awaitable[U]]], new_process: bool = False, new_thread: bool = True) -> List[U]
```

*   **Description**: Asynchronously processes a batch of items using the given function. It supports running the function in new threads or (conceptually) new processes.
*   **Parameters**:
    *   `batch` (`Iterable[T]`): An iterable of items to process.
    *   `func` (`Callable[[T], Union[U, Awaitable[U]]]`): An async or sync function to apply to each item.
    *   `new_process` (`bool`): If `True`, attempts to run each item's processing in a new process. Currently, this falls back to thread/direct execution with a warning. Defaults to `False`.
    *   `new_thread` (`bool`): If `True`, runs each item's processing in a new thread. This is ignored if `new_process` is `True`. Defaults to `True`.
*   **Returns**: `List[U]` - A list of results from processing each item. (Note: Current implementation includes a placeholder for result collection).

### Function: `process_batch`
```python
def process_batch(batch: Iterable[T], func: Callable[[T], U], new_process: bool = False, new_thread: bool = True) -> List[U]
```

*   **Description**: Synchronously processes a batch of items using the given function. It supports running the function in new threads or (conceptually) new processes.
*   **Parameters**:
    *   `batch` (`Iterable[T]`): An iterable of items to process.
    *   `func` (`Callable[[T], U]`): A sync function to apply to each item.
    *   `new_process` (`bool`): If `True`, attempts to run each item's processing in a new process. Currently, this falls back to thread/direct execution with a warning. Defaults to `False`.
    *   `new_thread` (`bool`): If `True`, runs each item's processing in a new thread. This is ignored if `new_process` is `True`. Defaults to `True`.
*   **Returns**: `List[U]` - A list of results from processing each item.

---

## `symb.core.schedule` Module

This module provides the core scheduling logic for the Symbol project.

### Class: `ScheduledJob`
* **Description**: Represents a single scheduled job.
* **Constructor**: `ScheduledJob()`
```
def __init__(self, func: Callable[..., Any], args: tuple, kwargs: dict, schedule: Union[str, datetime.datetime, datetime.date, datetime.time, Symbol], new_process: bool = False, new_thread: bool = True, id: Optional[str] = None)
```

* **Description**: Initializes a new `ScheduledJob`.
* **Parameters**:
    *   `func`: The function to execute.
    *   `args`: Positional arguments for the function.
    *   `kwargs`: Keyword arguments for the function.
    *   `schedule`: The schedule for the job. Can be a cron string, a `datetime.datetime` object, a `datetime.date` object, a `datetime.time` object, or a `Symbol` with a name that can be parsed as an ISO 8601 datetime string.
    *   `new_process`: Whether to run the job in a new process.
    *   `new_thread`: Whether to run the job in a new thread.
    *   `id`: An optional ID for the job.

### Class: `Scheduler`
* **Description**: Manages the schedule of jobs.
* **Constructor**: `Scheduler()`  
```python
def __init__(self, schedule_file: Optional[str] = None)
```

*   **Description**: Initializes a new `Scheduler`.
*   **Parameters**:
    *   `schedule_file`: An optional file path to save and load the schedule.
* **`add_job(self, job: ScheduledJob)`**
    *   **Description**: Adds a job to the schedule.
* **`remove_job(self, job_id: str) -> Optional[ScheduledJob]`**
    *   **Description**: Removes a job from the schedule by its ID.
* **`start(self)`**
    *   **Description**: Starts the scheduler in a background thread.
* **`stop(self)`**
    *   **Description**: Stops the scheduler.
* **`save_schedule(self)`**
    *   **Description**: Saves the current schedule to the schedule file.
* **`load_schedule(self)`**
    *   **Description**: Loads the schedule from the schedule file.
