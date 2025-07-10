"""This module provides functions for processing batches of items asynchronously and synchronously.

It offers a flexible and efficient way to apply a function to a collection of items,
with support for parallel execution using threads or processes.
"""
from typing import Iterable, Callable, Any, List, TypeVar, Union, Awaitable
import anyio
import logging
import inspect

from ..core.symbol import Symbol

log = logging.getLogger(__name__)

T = TypeVar('T')
U = TypeVar('U')

async def a_process_batch(batch: Iterable[T], func: Callable[[T], Union[U, Awaitable[U]]], 
                          new_process: bool = False, new_thread: bool = True) -> List[U]:
    """
    what: Asynchronously processes a batch of items.
    why: To apply a function to multiple items concurrently.
    how: Uses AnyIO task groups and thread/process pools.
    when: When processing a batch of items in an async context.
    by (caller(s)): External async code.
    how often: Frequently.
    how much: Depends on batch size and function complexity.
    what is it like: Parallel map operation.
    how, what, why and when to improve: Implement full new_process support.
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
    """
    what: Synchronously processes a batch of items.
    why: To apply a function to multiple items in a synchronous context.
    how: Uses AnyIO to run functions in threads/processes or directly.
    when: When processing a batch of items in a sync context.
    by (caller(s)): External sync code.
    how often: Frequently.
    how much: Depends on batch size and function complexity.
    what is it like: Synchronous map operation.
    how, what, why and when to improve: Implement full new_process support.
    """
    # For synchronous version, we can directly iterate or use anyio.run for thread/process pools
    if new_process:
        log.warning("new_process is not fully implemented for batch processing. Falling back to new_thread/direct.")
        return [anyio.run(anyio.to_thread.run_sync, func, item) for item in batch] # Placeholder for process pool
    elif new_thread:
        return [anyio.run(anyio.to_thread.run_sync, func, item) for item in batch]
    else:
        return [func(item) for item in batch]
