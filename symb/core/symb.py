"""
This module defines the Symbol NameSpace and links extended functionalities.
"""

from typing import Any

ENABLE_ORIGIN = True


def to_sym(obj: Any) -> 'Symbol':
    """Converts an object to a Symbol."""
    from core.symbol import Symbol
    return Symbol.from_object(obj)



