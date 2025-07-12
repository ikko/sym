
from core.symbol import Symbol
from core.symb import s
from core.graph_traversal import GraphTraversal

from builtin import apply_builtins
from core.time_arithmetics import add_time_objects, subtract_time_objects
from core.batch_processing import a_process_batch, process_batch
from . import builtin, core

# Apply the mixins first to ensure the Symbol class is fully featured
# This call should ideally happen once at application startup, not on every import
# For testing purposes, it's handled by conftest.py
apply_builtins()

# --- User-facing aliases for convenience ---

# Expose builtin modules at the top level (lazy loaded)
def __getattr__(name):
    if name == "schedule":
        return core.schedule
    elif name == "time_dim":
        return builtin.time_dim
    elif name == "collections":
        return builtin.collections
    elif name == "index":
        return builtin.index
    elif name == "path":
        return builtin.path
    elif name == "timeline":
        return builtin.timeline
    elif name == "visual":
        return builtin.visual
    elif name == "add_time":
        return add_time_objects
    elif name == "subtract_time":
        return subtract_time_objects
    elif name == "a_process_batch":
        return a_process_batch
    elif name == "process_batch":
        return process_batch
    elif name == "td":
        return builtin.time_dim
    elif name == "coll":
        return builtin.collections
    elif name == "idx":
        return builtin.index
    elif name == "vis":
        return builtin.visual
    elif name == "tl":
        return builtin.timeline
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def __dir__():
    return sorted(list(globals().keys()) + [
        "schedule", "time_dim", "collections", "index", "path", "timeline", "visual",
        "add_time", "subtract_time", "a_process_batch", "process_batch",
        "td", "coll", "idx", "vis", "tl"
    ])
