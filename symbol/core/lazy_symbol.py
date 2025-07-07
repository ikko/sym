
from typing import Any

class LazySymbol:
    __slots__ = ('_obj', '_symbol')

    def __init__(self, obj: Any):
        self._obj = obj
        self._symbol = None

    def __getattr__(self, name: str) -> Any:
        if self._symbol is None:
            from .symbol import Symbol
            self._symbol = Symbol.from_object(self._obj)
        return getattr(self._symbol, name)

    def __repr__(self) -> str:
        if self._symbol is None:
            return f"LazySymbol(unevaluated: {self._obj!r})"
        return repr(self._symbol)

    def __str__(self) -> str:
        if self._symbol is None:
            return f"LazySymbol(unevaluated: {self._obj!s})"
        return str(self._symbol)

    def __eq__(self, other: Any) -> bool:
        if self._symbol is None:
            from .symbol import Symbol
            self._symbol = Symbol.from_object(self._obj)
        return self._symbol == other

    def __hash__(self) -> int:
        if self._symbol is None:
            from .symbol import Symbol
            self._symbol = Symbol.from_object(self._obj)
        return hash(self._symbol)
