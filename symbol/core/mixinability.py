"""This module provides the core functionality for mixin-based extensibility of the Symbol class.

It allows for the dynamic registration and application of mixins,
with support for freezing the class to prevent further modifications.
"""
from collections import defaultdict
import gc
import logging
from typing import Callable, Any, Dict, get_origin, get_args, Union, Awaitable
import inspect

from .mixin_validator import validate_mixin_callable, MixinValidationResult
from .protocols import MixinFunction

# --- Module-level state ---

_is_frozen: bool = False
_applied_mixins: Dict[str, Any] = {}

# --- Logger Setup ---

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


# --- Core Mixinability Functions ---

def freeze() -> None:
    """Freezes the Symbol class, preventing any further runtime modifications."""
    global _is_frozen
    if _is_frozen:
        log.warning("Mixinability is already frozen. No action taken.")
        return

    _is_frozen = True
    log.info("Symbol class has been frozen. No further modifications are allowed.")

def is_frozen() -> bool:
    """Returns True if the Symbol class is currently frozen.""" 
    return _is_frozen

def register_mixin(target_class: type, name: str, value: Any) -> bool:
    """Registers a mixin to be applied to the target class, with validation and error handling.
    Returns True if the mixin was successfully registered, False otherwise.
    """
    if _is_frozen:
        log.error(f"Failed to register mixin '{name}': Symbol class is frozen.")
        return False

    # Validate the mixin callable if it's a function or method
    if callable(value) and not isinstance(value, (type, property)): # Exclude classes and properties
        try:
            # Perform static analysis validation
            validation_result = validate_mixin_callable(value)
            if not validation_result.is_valid:
                error_msg = f"Failed to register mixin '{name}': Static analysis validation failed: {\
                    '. '.join(validation_result.errors)}."
                log.error(error_msg)
                return False
            for warning in validation_result.warnings:
                log.warning(f"Mixin '{name}' static analysis warning: {warning}")

            # Further runtime validation against MixinFunction Protocol
            if not isinstance(value, MixinFunction):
                warnings.append(f"Mixin '{name}' does not fully conform to MixinFunction protocol at runtime.")

            # Check for new_process/new_thread parameters if it's an async function
            if inspect.iscoroutinefunction(value):
                sig = inspect.signature(value)
                if 'new_process' not in sig.parameters:
                    warnings.append(f"Async mixin '{name}' should include 'new_process: bool = False' in its signature.")
                if 'new_thread' not in sig.parameters:
                    warnings.append(f"Async mixin '{name}' should include 'new_thread: bool = True' in its signature.")

        except Exception as e:
            error_msg = f"An unexpected error occurred during validation of mixin '{name}': {e}."
            log.error(error_msg)
            return False

    if not hasattr(target_class, name):
        _applied_mixins[name] = None # Mark as new mixin, no original value to restore
        setattr(target_class, name, value)
        log.info(f"Successfully applied mixin: {target_class.__name__}.{name}")
        return True
    else:
        # If attribute already exists, store its original value for potential restoration
        if name not in _applied_mixins: # Only store if not already tracked
            _applied_mixins[name] = getattr(target_class, name)
        setattr(target_class, name, value)
        log.warning(f"Mixin '{name}' already exists on {target_class.__name__}. Overwriting.")
        return True

def get_applied_mixins() -> Dict[str, Any]:
    """Returns a copy of the dictionary of applied mixins."""
    return _applied_mixins.copy()

def _reset_frozen_state_for_testing() -> None:
    """Resets the frozen state for testing purposes. DO NOT USE IN PRODUCTION."""
    global _is_frozen
    _is_frozen = False
    log.warning("Symbol class frozen state has been reset for testing. DO NOT USE IN PRODUCTION.")