
from typing import Any

class LazySymbol:
    __slots__ = ('_obj', '_sym')

    def __init__(self, obj: Any):
        self._obj = obj
        self._sym = None

    def __getattr__(self, name: str) -> Any:
        if self._sym is None:
            from .sym import Symbol
            self._sym = Symbol.from_object(self._obj)
        return getattr(self._sym, name)

    def __repr__(self) -> str:
        if self._sym is None:
            return f"LazySymbol(unevaluated: {self._obj!r})"
        return repr(self._sym)

    def __str__(self) -> str:
        if self._sym is None:
            return f"LazySymbol(unevaluated: {self._obj!s})"
        return str(self._sym)

    def __eq__(self, other: Any) -> bool:
        if self._sym is None:
            from .sym import Symbol
            self._sym = Symbol.from_object(self._obj)
        return self._sym == other

    def __hash__(self) -> int:
        if self._sym is None:
            from .sym import Symbol
            self._sym = Symbol.from_object(self._obj)
        return hash(self._sym)
