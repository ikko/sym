import pytest
import sys

def test_direct_imports_skip_time_dim():
    # Attempt to import modules that should not directly import time_dim
    # This test relies on the fact that time_dim is a builtin and should be accessed via apply_builtins()
    # or through the top-level symbol package aliases.

    # Temporarily remove time_dim from sys.modules to ensure a fresh import
    if 'symbol.builtins.time_dim' in sys.modules:
        del sys.modules['symbol.builtins.time_dim']

    # These imports should succeed without pulling in time_dim directly
    try:
        from symbol.core import symbol
        from symbol.core import schedule
        from symbol.core import protocols
        from symbol.core import time_arithmetics
        from symbol.builtins import collections
        from symbol.builtins import index
        from symbol.builtins import path
        from symbol.builtins import visual
        from symbol.builtins import timeline

        # Assert that time_dim was NOT imported directly by these modules
        assert 'symbol.builtins.time_dim' not in sys.modules

    except ImportError as e:
        pytest.fail(f"Direct import failed unexpectedly: {e}")

def test_direct_imports_skip_core_and_builtins():
    # Temporarily remove core and builtins from sys.modules to ensure fresh imports
    if 'symbol.core' in sys.modules:
        del sys.modules['symbol.core']
    if 'symbol.builtins' in sys.modules:
        del sys.modules['symbol.builtins']

    # Remove specific submodules if they were already loaded
    for module_name in [
        'symbol.core.symbol',
        'symbol.builtins.time_dim',
        'symbol.builtins.collections',
        'symbol.builtins.index',
        'symbol.builtins.path',
        'symbol.builtins.visual',
        'symbol.builtins.timeline',
    ]:
        if module_name in sys.modules:
            del sys.modules[module_name]

    try:
        import symbol

        # Assert that core and builtins were NOT imported directly at the top level
        assert 'symbol.core' not in sys.modules
        assert 'symbol.builtins' not in sys.modules

        # Accessing aliases should trigger their import, but not necessarily the top-level package
        _ = symbol.s
        assert 'symbol.core.symbol' in sys.modules

        _ = symbol.Symbol
        assert 'symbol.core.symbol' in sys.modules

        _ = symbol.time_dim
        assert 'symbol.builtins.time_dim' in sys.modules

        _ = symbol.collections
        assert 'symbol.builtins.collections' in sys.modules

        _ = symbol.index
        assert 'symbol.builtins.index' in sys.modules

        _ = symbol.path
        assert 'symbol.builtins.path' in sys.modules

        _ = symbol.visual
        assert 'symbol.builtins.visual' in sys.modules

        _ = symbol.timeline
        assert 'symbol.builtins.timeline' in sys.modules

    except ImportError as e:
        pytest.fail(f"Direct import failed unexpectedly: {e}")