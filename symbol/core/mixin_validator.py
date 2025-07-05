"""This module provides a validator for Symbol mixins.

It uses static analysis with LibCST to ensure that mixins adhere to the expected interface
and do not contain any potentially unsafe code.
"""
import libcst as cst
from libcst.metadata import MetadataWrapper
from libcst.metadata import QualifiedNameProvider, QualifiedName
from typing import Callable, Any, List, Tuple, Union, Optional, Dict
import inspect
import logging
import textwrap
import warnings

log = logging.getLogger(__name__)

class MixinValidationResult:
    def __init__(self, is_valid: bool, errors: Optional[List[str]] = None, warnings: Optional[List[str]] = None):
        self.is_valid = is_valid
        self.errors = errors if errors is not None else []
        self.warnings = warnings if warnings is not None else []

    def __bool__(self) -> bool:
        return self.is_valid

    def __repr__(self) -> str:
        status = "Valid" if self.is_valid else "Invalid"
        return f"<MixinValidationResult: {status}, Errors: {len(self.errors)}, Warnings: {len(self.warnings)}>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def validate_mixin_callable(func: Callable[..., Any]) -> MixinValidationResult:
    """Validates a mixin callable for adherence to the Symbol's mixin interface."""
    errors = []
    validation_warnings = []

    source_code = None
    try:
        source_code = textwrap.dedent(inspect.getsource(func))
    except TypeError:
        errors.append(f"Cannot get source code for callable {func.__name__}. It might be a built-in or dynamically generated.")
        return MixinValidationResult(False, errors=errors)
    except OSError as e:
        errors.append(f"OS error getting source for {func.__name__}: {repr(e)}")
        return MixinValidationResult(False, errors=errors)

    tree = None
    try:
        tree = cst.parse_module(source_code)
        wrapper = MetadataWrapper(tree)
    except Exception as e:
        errors.append(f"Unexpected error during LibCST parsing: {repr(e)}")
        return MixinValidationResult(False, errors=errors)

    func_node = None
    for node in tree.body:
        if isinstance(node, cst.FunctionDef) and node.name.value == func.__name__:
            func_node = node
            break

    if not func_node:
        errors.append(f"Could not find function definition for {func.__name__} in parsed source.")
        return MixinValidationResult(False, errors=errors)

    try:
        # Validate signature (simplified for now, focusing on key aspects)
        params = func_node.params
        if not params.params or params.params[0].name.value != 'self':
            errors.append("Mixin function must have 'self' as its first parameter.")

        # Check for async/await usage if it's an async function
        if inspect.iscoroutinefunction(func):
            if not func_node.asynchronous:
                errors.append(f"Async mixin function {func.__name__} is not marked as 'async' in its definition.")
        elif func_node.asynchronous:
            validation_warnings.append(f"Sync mixin function {func.__name__} is marked as 'async' but is not a coroutine function.")

        # Check for forbidden imports/operations (example: direct file system access)
        # This would require a more sophisticated visitor pattern with LibCST
        # For now, a simple check for common problematic modules
        # This is a placeholder for more advanced static analysis.
        if "import os" in source_code or "import subprocess" in source_code:
            validation_warnings.append("Mixin contains potentially unsafe imports (os, subprocess). Review carefully.")

        # Check for return type annotation (optional but good practice)
        if not func_node.returns:
            validation_warnings.append(f"Mixin function {func.__name__} has no return type annotation.")

    except Exception as e:
        errors.append(f"Unexpected error during mixin validation logic: {repr(e)}")

    return MixinValidationResult(not errors, errors=errors, warnings=validation_warnings)
