import pytest
import anyio
from symb.core.batch_processing import process_batch, a_process_batch

# --- Synchronous Tests ---

def sync_square(x):
    return x * x

def sync_add_one(x):
    return x + 1

def test_process_batch_sync_direct():
    batch = [1, 2, 3]
    results = process_batch(batch, sync_square, new_thread=False, new_process=False)
    assert results == [1, 4, 9]

def test_process_batch_sync_new_thread():
    batch = [1, 2, 3]
    results = process_batch(batch, sync_square, new_thread=True, new_process=False)
    assert results == [1, 4, 9]

# --- Asynchronous Tests ---


