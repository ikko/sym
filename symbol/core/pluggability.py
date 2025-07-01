import gc
import logging
from typing import Callable, Any

# --- Module-level state ---

_is_frozen: bool = False
_applied_patches: dict[str, Any] = {}

# --- Logger Setup ---

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


# --- Core Pluggability Functions ---

def freeze() -> None:
    """Freezes the Symbol class, preventing any further runtime modifications."""
    global _is_frozen
    if _is_frozen:
        log.warning("Pluggability is already frozen. No action taken.")
        return

    _is_frozen = True
    log.info("Symbol class has been frozen. No further modifications are allowed.")

def immute() -> None:
    """
    Makes the Symbol class immutable by removing all dynamically applied built-in methods.
    This is a destructive, one-way operation that frees up memory.
    """
    global _is_frozen
    if not _is_frozen:
        raise RuntimeError("Cannot immute a non-frozen class. Call freeze() first.")

    log.info(f"Immuting Symbol class. Removing {_len(_applied_patches)} applied patches.")

    from ..core.symbol import Symbol
    for name, original_value in _applied_patches.items():
        try:
            delattr(Symbol, name)
            log.info(f"  - Removed patch: {name}")
        except AttributeError:
            log.warning(f"  - Could not remove patch '{name}'. It may have been removed manually.")

    _applied_patches.clear()
    gc.collect()
    log.info("Symbol class is now immutable and memory has been reclaimed.")

def is_frozen() -> bool:
    """Returns True if the Symbol class is currently frozen."""
    return _is_frozen

def register_patch(target_class: type, name: str, value: Any) -> None:
    """
A decorator or function to register a patch before applying it.
    This allows `immute` to know what to remove.
    """
    if _is_frozen:
        raise RuntimeError(f"Cannot patch '{name}' because the Symbol class is frozen.")

    if not hasattr(target_class, name):
        _applied_patches[name] = getattr(target_class, name, None)
        setattr(target_class, name, value)
        log.info(f"Applied patch: {target_class.__name__}.{name}")
    else:
        log.warning(f"Patch '{name}' already exists on {target_class.__name__}. Overwriting.")
        setattr(target_class, name, value)
