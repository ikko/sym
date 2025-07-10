
from typing import Any

class LazySymbol:
    __slots__ = ('_obj', '_symbol')

    def __init__(self, obj: Any):
        """
        what: Initializes a LazySymbol instance.
        why: To defer the creation of a full Symbol object until needed.
        how: Stores the raw object and initializes `_symbol` to None.
        when: When a Symbol needs to be created lazily.
        by (caller(s)): Symbol.from_object, Symbol.append.
        how often: Frequently.
        how much: Minimal.
        what is it like: Creating a promise for a future object.
        how, what, why and when to improve: N/A.
        """
        self._obj = obj
        self._symbol = None

    def __getattr__(self, name: str) -> Any:
        """
        what: Lazily evaluates the underlying Symbol and accesses its attribute.
        why: To provide seamless access to Symbol attributes without eager creation.
        how: Creates the Symbol if not already created, then delegates attribute access.
        when: When any attribute of the LazySymbol is accessed.
        by (caller(s)): Python's attribute lookup mechanism.
        how often: Frequently.
        how much: Minimal if Symbol already created, otherwise depends on Symbol creation.
        what is it like: On-demand object creation.
        how, what, why and when to improve: Optimize Symbol creation for complex objects.
        """
        if self._symbol is None:
            from .symbol import Symbol
            self._symbol = Symbol.from_object(self._obj)
        return getattr(self._symbol, name)

    def __repr__(self) -> str:
        """
        what: Returns a developer-friendly string representation.
        why: For debugging and introspection of LazySymbol state.
        how: Shows unevaluated object or delegates to Symbol's `repr`.
        when: When LazySymbol is printed in a debugger or console.
        by (caller(s)): Python's `repr()` function.
        how often: Frequently.
        how much: Minimal.
        what is it like: A dynamic label.
        how, what, why and when to improve: Include more internal state for complex debugging.
        """
        if self._symbol is None:
            return f"LazySymbol(unevaluated: {self._obj!r})"
        return repr(self._symbol)

    def __str__(self) -> str:
        """
        what: Returns a user-friendly string representation.
        why: For display to end-users.
        how: Shows unevaluated object or delegates to Symbol's `str`.
        when: When LazySymbol is converted to a string.
        by (caller(s)): Python's `str()` function, print statements.
        how often: Frequently.
        how much: Minimal.
        what is it like: A dynamic label.
        how, what, why and when to improve: N/A.
        """
        if self._symbol is None:
            return f"LazySymbol(unevaluated: {self._obj!s})"
        return str(self._symbol)

    def __eq__(self, other: Any) -> bool:
        """
        what: Compares two LazySymbol instances for equality.
        why: To determine if two LazySymbols represent the same entity.
        how: Lazily creates Symbol if needed, then delegates to Symbol's `eq`.
        when: When comparing LazySymbols.
        by (caller(s)): Python's equality operator (`==`).
        how often: Frequently.
        how much: Minimal if Symbol already created, otherwise depends on Symbol creation.
        what is it like: Comparing objects on demand.
        how, what, why and when to improve: Optimize Symbol creation for complex objects.
        """
        if self._symbol is None:
            from .symbol import Symbol
            self._symbol = Symbol.from_object(self._obj)
        return self._symbol == other

    def __hash__(self) -> int:
        """
        what: Computes the hash value for a LazySymbol.
        why: To allow LazySymbols in hash-based collections.
        how: Lazily creates Symbol if needed, then delegates to Symbol's `hash`.
        when: When LazySymbol is added to a set or used as a dictionary key.
        by (caller(s)): Python's `hash()` function.
        how often: Frequently.
        how much: Minimal if Symbol already created, otherwise depends on Symbol creation.
        what is it like: Generating a dynamic fingerprint.
        how, what, why and when to improve: Optimize Symbol creation for complex objects.
        """
        if self._symbol is None:
            from .symbol import Symbol
            self._symbol = Symbol.from_object(self._obj)
        return hash(self._symbol)
