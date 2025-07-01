from typing import Iterable, Callable, Any, List, TypeVar, Union, Awaitable
import asyncio
import anyio
import logging

from ..core.symbol import Symbol

log = logging.getLogger(__name__)

T = TypeVar('T')
U = TypeVar('U')

async def a_process_batch(batch: Iterable[T], func: Callable[[T], Union[U, Awaitable[U]]], 
                          new_process: bool = False, new_thread: bool = True) -> List[U]:
    """Asynchronously processes a batch of items using the given function.

    Args:
        batch: An iterable of items to process.
        func: An async or sync function to apply to each item.
        new_process: If True, run each item's processing in a new process.
        new_thread: If True, run each item's processing in a new thread (ignored if new_process is True).

    Returns:
        A list of results from processing each item.
    """
    results = []
    async def _process_item(item: T) -> U:
        if new_process:
            # Running in a new process requires serialization, more complex setup
            # For now, we'll log a warning and fall back to thread/direct execution
            log.warning("new_process is not fully implemented for batch processing. Falling back to new_thread/direct.")
            if new_thread:
                return await anyio.to_thread.run_sync(func, item)
            else:
                return func(item)
        elif new_thread:
            return await anyio.to_thread.run_sync(func, item)
        else:
            # Check if the function is a coroutine function
            if inspect.iscoroutinefunction(func):
                return await func(item)
            else:
                return func(item)

    async with anyio.create_task_group() as tg:
        for item in batch:
            tg.start_soon(_process_item, item)
    
    # Collect results (this part needs refinement to actually collect from task group)
    # For now, this is a placeholder. Actual results would be collected from tasks.
    log.warning("Batch processing result collection is a placeholder. Actual results not yet collected.")
    return results # Placeholder

def process_batch(batch: Iterable[T], func: Callable[[T], U], 
                  new_process: bool = False, new_thread: bool = True) -> List[U]:
    """Synchronously processes a batch of items using the given function.

    Args:
        batch: An iterable of items to process.
        func: A sync function to apply to each item.
        new_process: If True, run each item's processing in a new process.
        new_thread: If True, run each item's processing in a new thread (ignored if new_process is True).

    Returns:
        A list of results from processing each item.
    """
    # For synchronous version, we can directly iterate or use anyio.run for thread/process pools
    if new_process:
        log.warning("new_process is not fully implemented for batch processing. Falling back to new_thread/direct.")
        return [anyio.run(anyio.to_thread.run_sync, func, item) for item in batch] # Placeholder for process pool
    elif new_thread:
        return [anyio.run(anyio.to_thread.run_sync, func, item) for item in batch]
    else:
        return [func(item) for item in batch]
