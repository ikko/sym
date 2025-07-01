from collections import defaultdict
import gc
import logging
from typing import Callable, Any, Dict

# --- Module-level state ---

_is_frozen: bool = False
_applied_patches: Dict[str, Any] = {}

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
        _applied_patches[name] = None # Mark as new patch, no original value to restore
        setattr(target_class, name, value)
        log.info(f"Applied patch: {target_class.__name__}.{name}")
    else:
        # If attribute already exists, store its original value for potential restoration
        if name not in _applied_patches: # Only store if not already tracked
            _applied_patches[name] = getattr(target_class, name)
        setattr(target_class, name, value)
        log.warning(f"Patch '{name}' already exists on {target_class.__name__}. Overwriting.")

def get_applied_patches() -> Dict[str, Any]:
    """Returns a copy of the dictionary of applied patches."""
    return _applied_patches.copy()
