"""This module provides functions for processing batches of items asynchronously and synchronously.

It offers a flexible and efficient way to apply a function to a collection of items,
with support for parallel execution using threads or processes.
"""
from typing import Iterable, Callable, Any, List, TypeVar, Union, Awaitable
import anyio
import logging
import inspect

from ..core.symb import Symbol

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
    tasks = []
    async with anyio.create_task_group() as tg:
        for item in batch:
            if new_process:
                log.warning("new_process is not fully implemented for batch processing. Falling back to new_thread/direct.")
                task = tg.start_soon(anyio.to_thread.run_sync, func, item)
            elif new_thread:
                task = tg.start_soon(anyio.to_thread.run_sync, func, item)
            else:
                if inspect.iscoroutinefunction(func):
                    task = tg.start_soon(func, item)
                else:
                    task = tg.start_soon(anyio.to_thread.run_sync, func, item)
            tasks.append(task)

    results = []
    for task in tasks:
        results.append(await task)
    return results

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
