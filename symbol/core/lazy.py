from typing import Any

class _Sentinel:
    """A unique sentinel object used to distinguish between user-provided None and system-default None."""
    def __repr__(self) -> str:
        return "<SENTINEL>"

SENTINEL = _Sentinel()