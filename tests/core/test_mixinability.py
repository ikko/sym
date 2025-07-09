import pytest
from sym import Symbol
from sym.core.mixinability import freeze, is_frozen, register_mixin, _reset_frozen_state_for_testing

@pytest.fixture(autouse=True)
def reset_frozen_state():
    _reset_frozen_state_for_testing()
    yield
    _reset_frozen_state_for_testing() # Reset again after test to ensure clean state for other tests

def test_freeze_and_is_frozen_states():
    # Ensure initial state is not frozen
    assert not is_frozen()

    # Test freezing the Symbol class
    freeze()
    assert is_frozen()

    # Test that subsequent calls to freeze do not change state (it's idempotent)
    freeze()
    assert is_frozen()

def test_register_mixin_basic_application():
    # Define a simple mixin function
    def my_mixin_function(self):
        return f"Hello from {self.name}"

    # Register the mixin
    success = register_mixin(my_mixin_function, "my_new_method")
    assert success is True

    # Test that the mixin is applied to Symbol instances
    s = Symbol("test_sym_for_mixin")
    assert hasattr(s, "my_new_method")
    assert callable(s.my_new_method)
    assert s.my_new_method() == "Hello from test_sym_for_mixin"

    # Test registering another mixin that overwrites an existing one
    def my_overwriting_mixin(self):
        return "Overwritten!"

    success_overwrite = register_mixin(my_overwriting_mixin, "my_new_method")
    assert success_overwrite is True
    assert s.my_new_method() == "Overwritten!"
