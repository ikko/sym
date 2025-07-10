"""This module provides the core functionality for mixin-based extensibility of the Symbol class.

It allows for the dynamic registration and application of mixins,
with support for freezing the class to prevent further modifications.
"""
from collections import defaultdict
import gc
import logging
from typing import Callable, Any, Dict, get_origin, get_args, Union, Awaitable, Type
import inspect
import ast

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
    """
    what: Freezes the Symbol class.
    why: To prevent further runtime modifications.
    how: Sets a global flag `_is_frozen` to True.
    when: When the Symbol class state needs to be immutable.
    by (caller(s)): Symbol.immute.
    how often: Once per application lifecycle.
    how much: Minimal.
    what is it like: Locking down a system.
    how, what, why and when to improve: N/A.
    """
    global _is_frozen
    if _is_frozen:
        log.warning("Mixinability is already frozen. No action taken.")
        return

    _is_frozen = True
    log.info("Symbol class has been frozen. No further modifications are allowed.")

def is_frozen() -> bool:
    """
    what: Checks if the Symbol class is frozen.
    why: To determine if modifications are allowed.
    how: Reads the global `_is_frozen` flag.
    when: Before attempting to modify Symbol class state.
    by (caller(s)): elevate, slim, immute, clear_context, register_mixin.
    how often: Frequently.
    how much: Minimal.
    what is it like: Checking a lock status.
    how, what, why and when to improve: N/A.
    """ 
    return _is_frozen

import re

def register_mixin(value: Any, name: str = None, target_class: type = None, safe: bool = False, expand: bool = True) -> bool:
    """
    what: Registers a mixin for dynamic application.
    why: To extend Symbol class functionality at runtime.
    how: Validates, infers name, handles expansion, applies mixin.
    when: During application setup or dynamic feature loading.
    by (caller(s)): apply_builtins.
    how often: Infrequently.
    how much: Moderate, depends on mixin complexity.
    what is it like: Plugging in a new module.
    how, what, why and when to improve: Improve error handling, add more validation.
    """
    if target_class is None:
        from ..core.base_symbol import Symbol
        target_class = Symbol

    def _to_snake_case(s: str) -> str:
        """
        what: Converts a string to snake_case.
        why: To standardize mixin names.
        how: Uses regular expressions for conversion.
        when: During mixin registration.
        by (caller(s)): register_mixin.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Formatting text.
        how, what, why and when to improve: N/A.
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    # Evaluate value if it's a string
    if isinstance(value, str):
        try:
            # WARNING: Using eval() can be dangerous if the input string is not trusted.
            # Ensure that 'value' strings come from trusted sources.
            value = ast.literal_eval(value)
        except Exception as e:
            log.error(f"Failed to evaluate mixin value string '{value}': {repr(e)}.")
            return False

    # Infer name if not provided
    if name is None:
        if inspect.ismethod(value) or inspect.isfunction(value):
            name = value.__name__
        elif hasattr(value, '__class__'):
            class_name = value.__class__.__name__
            if class_name.endswith('Mixin'):
                class_name = class_name[:-5]
            name = _to_snake_case(class_name)
        else:
            log.error(f"Failed to infer mixin name from value: {value}. Please provide a name explicitly.")
            return False

    # Handle expansion for classes and modules
    if expand:
        if inspect.isclass(value):
            for attr_name in dir(value):
                if not attr_name.startswith('_'):
                    attr_value = getattr(value, attr_name)
                    if isinstance(attr_value, staticmethod):
                        actual_value = attr_value.__func__
                        setattr(target_class, attr_name, staticmethod(actual_value))
                        log.info(f"Successfully applied static mixin: {target_class.__name__}.{attr_name}")
                    elif isinstance(attr_value, property):
                        actual_value = attr_value.fget # Get the getter for the property
                        setattr(target_class, attr_name, property(actual_value))
                        log.info(f"Successfully applied property mixin: {target_class.__name__}.{attr_name}")
                    elif inspect.isfunction(attr_value) or inspect.ismethod(attr_value):
                        # Recursively register methods, but don't expand them further
                        register_mixin(attr_value, name=attr_name, target_class=target_class, safe=safe, expand=False)
            return True # Class expansion handled, return
        elif inspect.ismodule(value):
            for attr_name in dir(value):
                if not attr_name.startswith('_'):
                    attr_value = getattr(value, attr_name)
                    # Recursively register public members, but don't expand them further
                    register_mixin(attr_value, name=attr_name, target_class=target_class, safe=safe, expand=False)
            return True # Module expansion handled, return

    # Validate the mixin callable if it's a function or method
    if callable(value) and not isinstance(value, (type, property)): # Exclude classes and properties
        try:
            # Perform static analysis validation
            validation_result = validate_mixin_callable(value)
            if not validation_result.is_valid:
                error_msg = f"Failed to register mixin '{name}': Static analysis validation failed: {'. '.join(validation_result.errors)}."
                log.error(error_msg)
                return False
            for warning in validation_result.warnings:
                log.warning(f"Mixin '{name}' static analysis warning: {warning}")

            # Further runtime validation against MixinFunction Protocol
            # Further runtime validation against MixinFunction Protocol
            if not isinstance(value, MixinFunction):
                log.warning(f"Mixin '{name}' does not fully conform to MixinFunction protocol at runtime.")

            # Check for new_process/new_thread parameters if it's an async function
            if inspect.iscoroutinefunction(value):
                sig = inspect.signature(value)
                if 'new_process' not in sig.parameters:
                    log.debug(f"Async mixin '{name}' should include 'new_process: bool = False' in its signature.")
                if 'new_thread' not in sig.parameters:
                    log.debug(f"Async mixin '{name}' should include 'new_thread: bool = True' in its signature.")

        except Exception as e:
            error_msg = f"An unexpected error occurred during validation of mixin '{name}': {repr(e)}."
            log.error(error_msg)
            return False

    if hasattr(target_class, name):
        if safe:
            log.error(f"Failed to register mixin '{name}': Attribute already exists on {target_class.__name__} and safe mode is enabled (no overwrite).")
            return False
        else:
            # If attribute already exists, store its original value for potential restoration
            if name not in _applied_mixins: # Only store if not already tracked
                _applied_mixins[name] = getattr(target_class, name)
            setattr(target_class, name, value)
            log.warning(f"Mixin '{name}' already exists on {target_class.__name__}. Overwriting.")
            return True
    else:
        _applied_mixins[name] = None # Mark as new mixin, no original value to restore
        setattr(target_class, name, value)
        log.debug(f"Successfully applied mixin: {target_class.__name__}.{name}")
        return True

def get_applied_mixins() -> Dict[str, Any]:
    """
    what: Retrieves currently applied mixins.
    why: To inspect the Symbol class's extended capabilities.
    how: Returns a copy of the internal `_applied_mixins` dictionary.
    when: When auditing or debugging mixin application.
    by (caller(s)): Symbol.stat, Symbol.ls.
    how often: Infrequently.
    how much: Minimal.
    what is it like: Listing installed plugins.
    how, what, why and when to improve: N/A.
    """
    return _applied_mixins.copy()

def apply_mixin_to_instance(instance: 'Symbol', mixin: Any):
    """
    what: Applies a mixin to a specific Symbol instance.
    why: For isolated operations without global class modification.
    how: Elevates mixin attributes to the instance's `_elevated_attributes`.
    when: When temporary or instance-specific mixin behavior is needed.
    by (caller(s)): Symbol.stat, _get_mixin_metrics.
    how often: Infrequently.
    how much: Minimal.
    what is it like: Adding a temporary ability.
    how, what, why and when to improve: N/A.
    """
    if inspect.isclass(mixin):
        # Instantiate the mixin if it's a class
        mixin_instance = mixin()
        for attr_name in dir(mixin_instance):
            if not attr_name.startswith('__'):
                attr_value = getattr(mixin_instance, attr_name)
                instance._elevated_attributes[attr_name] = attr_value
    else:
        # For functions or other callables, we can't easily apply them to an instance without registering them.
        # For stat, we are interested in the footprint, so we can just add the mixin itself.
        if hasattr(mixin, '__name__'):
            instance._elevated_attributes[mixin.__name__] = mixin


from .protocols import MixinHealthState

def _get_mixin_metrics(mixin_cls: Any, Symbol_cls: Type['Symbol']) -> dict:
    """
    what: Calculates metrics for a given mixin.
    why: To provide detailed information about mixin performance and state.
    how: Creates a dummy Symbol, applies mixin, measures footprint, checks init time.
    when: When `Symbol.stat()` or `Symbol.ls()` is called.
    by (caller(s)): Symbol.stat, Symbol.ls.
    how often: Infrequently.
    how much: Moderate, involves dummy Symbol creation.
    what is it like: Running a diagnostic on a component.
    how, what, why and when to improve: Refine footprint calculation, implement health checks.
    """
    metrics = {}
    metrics['name'] = mixin_cls.__name__ if inspect.isclass(mixin_cls) else mixin_cls.__class__.__name__

    # Create a temporary dummy symbol to measure mixin size
    dummy_symbol = Symbol_cls(f"dummy_for_{metrics['name']}")
    apply_mixin_to_instance(dummy_symbol, mixin_cls)

    # Calculate footprint
    # This is a simplified approach. A more accurate footprint would involve
    # recursively calculating the size of all attributes added by the mixin.
    # For now, we'll consider the size of the elevated attributes dictionary.
    metrics['footprint'] = dummy_symbol.footprint() - Symbol_cls("dummy").footprint() # Approximate footprint

    # Determine slim_tag
    is_slim_tag = False
    for attr_name in dir(dummy_symbol):
        if not attr_name.startswith('__') and not callable(getattr(dummy_symbol, attr_name)):
            try:
                value = getattr(dummy_symbol, attr_name)
                if value is not SENTINEL:
                    is_slim_tag = True
                    break
            except AttributeError:
                pass
    metrics['slim_tag'] = is_slim_tag

    # Uptime
    mixin_instance = mixin_cls() if inspect.isclass(mixin_cls) else mixin_cls
    if hasattr(mixin_instance, '_init_time') and mixin_instance._init_time:
        metrics['uptime'] = datetime.datetime.now() - mixin_instance._init_time
    else:
        metrics['uptime'] = datetime.timedelta(0)

    # Health State (placeholder for now, will refine later)
    metrics['state'] = MixinHealthState.UNKNOWN.value # Placeholder

    # Healthy
    metrics['healthy'] = (metrics['state'] == MixinHealthState.HEALTHY.value)

    return metrics

def _reset_frozen_state_for_testing() -> None:
    """
    what: Resets the Symbol class frozen state.
    why: For testing scenarios requiring mutable state.
    how: Sets the global `_is_frozen` flag to False.
    when: Exclusively in test environments.
    by (caller(s)): Test fixtures.
    how often: Only during testing.
    how much: Minimal.
    what is it like: Unlocking a test environment.
    how, what, why and when to improve: N/A.
    """
    global _is_frozen
    _is_frozen = False
    log.warning("Symbol class frozen state has been reset for testing. DO NOT USE IN PRODUCTION.")
