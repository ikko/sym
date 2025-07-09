import pytest
import sys

def test_direct_imports_skip_time_dim():
    # Attempt to import modules that should not directly import time_dim
    # This test relies on the fact that time_dim is a builtin and should be accessed via apply_builtins()
    # or through the top-level sym package aliases.

    # Temporarily remove time_dim from sys.modules to ensure a fresh import
    if 'sym.builtins.time_dim' in sys.modules:
        del sys.modules['sym.builtins.time_dim']

    # These imports should succeed without pulling in time_dim directly
    try:
        from sym.core import sym
        from sym.core import schedule
        from sym.core import protocols
        from sym.core import time_arithmetics
        from sym.builtins import collections
        from sym.builtins import index
        from sym.builtins import path
        from sym.builtins import visual
        from sym.builtins import timeline

        # Assert that time_dim was NOT imported directly by these modules
        assert 'sym.builtins.time_dim' not in sys.modules

    except ImportError as e:
        pytest.fail(f"Direct import failed unexpectedly: {e}")

def test_direct_imports_skip_core_and_builtins():
    # Temporarily remove core and builtins from sys.modules to ensure fresh imports
    if 'sym.core' in sys.modules:
        del sys.modules['sym.core']
    if 'sym.builtins' in sys.modules:
        del sys.modules['sym.builtins']

    # Remove specific submodules if they were already loaded
    for module_name in [
        'sym.core.sym',
        'sym.builtins.time_dim',
        'sym.builtins.collections',
        'sym.builtins.index',
        'sym.builtins.path',
        'sym.builtins.visual',
        'sym.builtins.timeline',
    ]:
        if module_name in sys.modules:
            del sys.modules[module_name]

    try:
        import sym

        # Assert that core and builtins were NOT imported directly at the top level
        assert 'sym.core' not in sys.modules
        assert 'sym.builtins' not in sys.modules

        # Accessing aliases should trigger their import, but not necessarily the top-level package
        # sym.s, sym.Symbol, and sym.GraphTraversal are now directly imported in sym/__init__.py
        # so they will always be present.

        # TODO:
        # _ = sym.time_dim
        # assert 'sym.builtins.time_dim' in sys.modules
        #
        # _ = sym.collections
        # assert 'sym.builtins.collections' in sys.modules
        #
        # _ = sym.index
        # assert 'sym.builtins.index' in sys.modules
        #
        # _ = sym.path
        # assert 'sym.builtins.path' in sys.modules
        #
        # _ = sym.visual
        # assert 'sym.builtins.visual' in sys.modules
        #
        # _ = sym.timeline
        # assert 'sym.builtins.timeline' in sys.modules

    except ImportError as e:
        pytest.fail(f"Direct import failed unexpectedly: {e}")
