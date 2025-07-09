
from typing import Any

class LazySymbol:
    __slots__ = ('_obj', '_symb')

    def __init__(self, obj: Any):
        self._obj = obj
        self._symb = None

    def __getattr__(self, name: str) -> Any:
        if self._symb is None:
            from .symb import Symbol
            self._symb = Symbol.from_object(self._obj)
        return getattr(self._symb, name)

    def __repr__(self) -> str:
        if self._symb is None:
            return f"LazySymbol(unevaluated: {self._obj!r})"
        return repr(self._symb)

    def __str__(self) -> str:
        if self._symb is None:
            return f"LazySymbol(unevaluated: {self._obj!s})"
        return str(self._symb)

    def __eq__(self, other: Any) -> bool:
        if self._symb is None:
            from .symb import Symbol
            self._symb = Symbol.from_object(self._obj)
        return self._symb == other

    def __hash__(self) -> int:
        if self._symb is None:
            from .symb import Symbol
            self._symb = Symbol.from_object(self._obj)
        return hash(self._symb)
