import pytest
import anyio
from symbol.core.batch_processing import process_batch, a_process_batch

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

async def async_square(x):
    await anyio.sleep(0.01) # Simulate async work
    return x * x

async def async_add_one(x):
    await anyio.sleep(0.01) # Simulate async work
    return x + 1

@pytest.mark.anyio
async def test_a_process_batch_async_direct():
    batch = [1, 2, 3]
    results = await a_process_batch(batch, async_square, new_thread=False, new_process=False)
    assert results == [1, 4, 9]

@pytest.mark.anyio
async def test_a_process_batch_async_new_thread():
    batch = [1, 2, 3]
    results = await a_process_batch(batch, async_square, new_thread=True, new_process=False)
    assert results == [1, 4, 9]

@pytest.mark.anyio
async def test_a_process_batch_sync_func_async_context():
    batch = [1, 2, 3]
    results = await a_process_batch(batch, sync_square, new_thread=False, new_process=False)
    assert results == [1, 4, 9]
