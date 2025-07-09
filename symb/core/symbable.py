"""This module defines the Symbolable protocol.

This protocol is used to identify objects that can be integrated into a Symbol instance,
providing a clear contract for their behavior.
"""
from typing import Protocol, Any, Callable, Awaitable, Union

class Symbolable(Protocol):
    """Protocol for objects that can be integrated into a Symbol instance."""
    def __call__(self, *args: Any, **kwargs: Any) -> Union[Any, Awaitable[Any]]:
        """Defines the callable interface for Symbolable objects."""
        ...

    # Additional methods/properties can be added here to define what it means to be Symbolable
    # For example, a method to get its signature, or a flag indicating if it's async.
