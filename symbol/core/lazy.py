from typing import Any

class _Sentinel:
    """A unique sentinel object used to distinguish between user-provided None and system-default None."""
    def __repr__(self) -> str:
        """
        what: Returns a string representation of the sentinel.
        why: For debugging and clear identification of the sentinel object.
        how: Returns the string "<SENTINEL>".
        when: When the sentinel object is printed or represented.
        by (caller(s)): Python's `repr()` function.
        how often: Infrequently.
        how much: Minimal.
        what is it like: A unique marker.
        how, what, why and when to improve: N/A.
        """
        return "<SENTINEL>"

SENTINEL = _Sentinel()