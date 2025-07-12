import pytest
import sys

def test_direct_imports_skip_time_dim():
    # Attempt to import modules that should not directly import time_dim
    # This test relies on the fact that time_dim is a builtin and should be accessed via apply_builtins()
    # or through the top-level symb package aliases.

    # Temporarily remove time_dim from sys.modules to ensure a fresh import
    if 'symb.builtin.time_dim' in sys.modules:
        del sys.modules['symb.builtin.time_dim']

    # These imports should succeed without pulling in time_dim directly
    try:
        from core import symb
        from core import schedule
        from core import protocols
        from core import time_arithmetics
        from builtin import collections
        from builtin import index
        from builtin import path
        from builtin import visual
        from builtin import timeline

        # Assert that time_dim was NOT imported directly by these modules
        assert 'symb.builtin.time_dim' not in sys.modules

    except ImportError as e:
        import logging
        logging.error(f"Direct import failed unexpectedly: {repr(e)}, line 28", exc_info=True)
        pytest.fail(f"Direct import failed unexpectedly: {repr(e)}")

def test_direct_imports_skip_core_and_builtins():
    # Temporarily remove core and builtin from sys.modules to ensure fresh imports
    if 'symb.core' in sys.modules:
        del sys.modules['symb.core']
    if 'symb.builtin' in sys.modules:
        del sys.modules['symb.builtin']

    # Remove specific submodules if they were already loaded
    for module_name in [
        'symb.core.symb',
        'symb.builtin.time_dim',
        'symb.builtin.collections',
        'symb.builtin.index',
        'symb.builtin.path',
        'symb.builtin.visual',
        'symb.builtin.timeline',
    ]:
        if module_name in sys.modules:
            del sys.modules[module_name]

    try:
        import symb

        # Assert that core and builtin were NOT imported directly at the top level
        assert 'symb.core' not in sys.modules
        assert 'symb.builtin' not in sys.modules

        # Accessing aliases should trigger their import, but not necessarily the top-level package
        # symb.s, symb.Symbol, and symb.GraphTraversal are now directly imported in symb/__init__.py
        # so they will always be present.

        # TODO:
        # _ = symb.time_dim
        # assert 'symb.builtin.time_dim' in sys.modules
        #
        # _ = symb.collections
        # assert 'symb.builtin.collections' in sys.modules
        #
        # _ = symb.index
        # assert 'symb.builtin.index' in sys.modules
        #
        # _ = symb.path
        # assert 'symb.builtin.path' in sys.modules
        #
        # _ = symb.visual
        # assert 'symb.builtin.visual' in sys.modules
        #
        # _ = symb.timeline
        # assert 'symb.builtin.timeline' in sys.modules

    except ImportError as e:
        import logging
        logging.error(f"Direct import failed unexpectedly: {repr(e)}, line 81", exc_info=True)
        pytest.fail(f"Direct import failed unexpectedly: {repr(e)}")
