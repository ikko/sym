import sys
import os
import pytest
from symbol import Symbol
from symbol.builtins import apply_builtins
from symbol.builtins.avl_tree import AVLTree

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

@pytest.fixture(scope='session', autouse=True)
def apply_builtins_for_session():
    apply_builtins()

@pytest.fixture(autouse=True)
def setup_and_teardown(request):

    # Store original _numbered and _pool, and clear them for predictable testing
    original_numbered = Symbol._numbered.traverse_inorder()
    original_pool = dict(Symbol._pool)

    # Clear for predictable testing
    Symbol._numbered = AVLTree() # Reinitialize AVLTree
    Symbol._pool.clear()
    Symbol._auto_counter = 0
    Symbol._read_cursor = 0.0
    Symbol._write_cursor = 0.0

    # If the test function has a specific set of symbols to use, add them
    if hasattr(request, 'param'):
        for sym in request.param:
            # Assuming sym has a ._position attribute for its weight
            Symbol(sym.name, sym.origin) # Re-create symbol to ensure it's added to the new AVLTree and pool

    yield

    # Restore original _numbered and _pool after each test
    Symbol._numbered = AVLTree() # Reinitialize AVLTree
    for sym in original_numbered:
        Symbol(sym.name, sym.origin) # Re-create symbol to ensure it's added to the new AVLTree and pool
    Symbol._pool.update(original_pool)
    # Reset auto_counter, read_cursor, write_cursor based on original_numbered if needed
    # For now, assuming they will be correctly managed by Symbol.__new__ upon re-creation
