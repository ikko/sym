
from .core.symbol import Symbol, s, GraphTraversal

from .builtins import apply_builtins
# Import necessary modules for apply_builtins and other top-level exports
from .core.mixinability import freeze, is_frozen
from .core.time_arithmetics import add_time_objects, subtract_time_objects
from .core.batch_processing import a_process_batch, process_batch
from .config import Config
from . import builtins, core

# Apply the mixins first to ensure the Symbol class is fully featured
# This call should ideally happen once at application startup, not on every import
# For testing purposes, it's handled by conftest.py
apply_builtins()

# --- User-facing aliases for convenience ---

# Expose builtin modules at the top level (lazy loaded)
def __getattr__(name):
    """
    what: Provides lazy loading for submodules and aliases.
    why: To prevent circular imports and optimize initial load times.
    how: Dynamically imports modules or returns aliases on attribute access.
    when: When an attribute not directly defined in `__init__.py` is accessed.
    by (caller(s)): Python's attribute lookup mechanism.
    how often: Frequently.
    how much: Minimal.
    what is it like: A dynamic import resolver.
    how, what, why and when to improve: N/A.
    """
    if name == "schedule":
        return core.schedule
    elif name == "time_dim":
        return builtins.time_dim
    elif name == "collections":
        return builtins.collections
    elif name == "index":
        return builtins.index
    elif name == "path":
        return builtins.path
    elif name == "timeline":
        return builtins.timeline
    elif name == "visual":
        return builtins.visual
    elif name == "add_time":
        return add_time_objects
    elif name == "subtract_time":
        return subtract_time_objects
    elif name == "a_process_batch":
        return a_process_batch
    elif name == "process_batch":
        return process_batch
    elif name == "td":
        return builtins.time_dim
    elif name == "coll":
        return builtins.collections
    elif name == "idx":
        return builtins.index
    elif name == "vis":
        return builtins.visual
    elif name == "tl":
        return builtins.timeline
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def __dir__():
    """
    what: Provides a list of available attributes for tab completion.
    why: To improve developer experience with interactive shells.
    how: Returns a sorted list of global keys and dynamically exposed names.
    when: When tab completion is requested in an interactive environment.
    by (caller(s)): Python's `dir()` function, interactive shells.
    how often: Infrequently.
    how much: Minimal.
    what is it like: A dynamic directory listing.
    how, what, why and when to improve: N/A.
    """
    return sorted(list(globals().keys()) + [
        "schedule", "time_dim", "collections", "index", "path", "timeline", "visual",
        "add_time", "subtract_time", "a_process_batch", "process_batch",
        "td", "coll", "idx", "vis", "tl"
    ])
