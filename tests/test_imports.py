import pytest
import sys

def test_direct_imports_skip_time_dim():
    # Attempt to import modules that should not directly import time_dim
    # This test relies on the fact that time_dim is a builtin and should be accessed via apply_builtins()
    # or through the top-level symb package aliases.

    # Temporarily remove time_dim from sys.modules to ensure a fresh import
    if 'symb.builtins.time_dim' in sys.modules:
        del sys.modules['symb.builtins.time_dim']

    # These imports should succeed without pulling in time_dim directly
    try:
        from symb.core import symb
        from symb.core import schedule
        from symb.core import protocols
        from symb.core import time_arithmetics
        from symb.builtins import collections
        from symb.builtins import index
        from symb.builtins import path
        from symb.builtins import visual
        from symb.builtins import timeline

        # Assert that time_dim was NOT imported directly by these modules
        assert 'symb.builtins.time_dim' not in sys.modules

    except ImportError as e:
        pytest.fail(f"Direct import failed unexpectedly: {e}")

def test_direct_imports_skip_core_and_builtins():
    # Temporarily remove core and builtins from sys.modules to ensure fresh imports
    if 'symb.core' in sys.modules:
        del sys.modules['symb.core']
    if 'symb.builtins' in sys.modules:
        del sys.modules['symb.builtins']

    # Remove specific submodules if they were already loaded
    for module_name in [
        'symb.core.symb',
        'symb.builtins.time_dim',
        'symb.builtins.collections',
        'symb.builtins.index',
        'symb.builtins.path',
        'symb.builtins.visual',
        'symb.builtins.timeline',
    ]:
        if module_name in sys.modules:
            del sys.modules[module_name]

    try:
        import symb

        # Assert that core and builtins were NOT imported directly at the top level
        assert 'symb.core' not in sys.modules
        assert 'symb.builtins' not in sys.modules

        # Accessing aliases should trigger their import, but not necessarily the top-level package
        # symb.s, symb.Symbol, and symb.GraphTraversal are now directly imported in symb/__init__.py
        # so they will always be present.

        # TODO:
        # _ = symb.time_dim
        # assert 'symb.builtins.time_dim' in sys.modules
        #
        # _ = symb.collections
        # assert 'symb.builtins.collections' in sys.modules
        #
        # _ = symb.index
        # assert 'symb.builtins.index' in sys.modules
        #
        # _ = symb.path
        # assert 'symb.builtins.path' in sys.modules
        #
        # _ = symb.visual
        # assert 'symb.builtins.visual' in sys.modules
        #
        # _ = symb.timeline
        # assert 'symb.builtins.timeline' in sys.modules

    except ImportError as e:
        pytest.fail(f"Direct import failed unexpectedly: {e}")
