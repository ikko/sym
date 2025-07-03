import sys
import os
import pytest
from symbol.core.symbol import Symbol
from symbol.builtins import apply_builtins

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

@pytest.fixture(autouse=True)
def setup_and_teardown(request):
    # Ensure builtins are applied before each test
    apply_builtins()

    # Store original _numbered and _pool, and clear them for predictable testing
    original_numbered = list(Symbol._numbered)
    original_pool = dict(Symbol._pool)
    Symbol._numbered.clear()
    Symbol._pool.clear()

    # If the test function has a specific set of symbols to use, add them
    if hasattr(request, 'param'):
        for sym in request.param:
            Symbol._numbered.append(sym)

    yield

    # Restore original _numbered and _pool after each test
    Symbol._numbered.clear()
    Symbol._numbered.extend(original_numbered)
    Symbol._pool.clear()
    Symbol._pool.update(original_pool)