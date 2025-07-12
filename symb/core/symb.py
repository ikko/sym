"""
This module defines the Symbol NameSpace and links extended functionalities.
"""

from typing import Any

from .symbol_namespace import SymbolNamespace

ENABLE_ORIGIN = True

from .symbol import Symbol

def to_sym(obj: Any) -> 'Symbol':
    """Converts an object to a Symbol."""
    return Symbol.from_object(obj)


s = SymbolNamespace()
