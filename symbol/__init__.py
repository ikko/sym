from .core.symbol import Symbol, s
from .core.graph import GraphTraversal
from .core.pluggability import freeze, immute, is_frozen
from . import builtins
from .builtins import apply_builtins

# Apply the patches first to ensure the Symbol class is fully featured
apply_builtins()

# --- User-facing aliases for convenience ---

# Expose builtin modules at the top level
datetime = builtins.datetime
collections = builtins.collections
indexing = builtins.indexing
path = builtins.path

# Proxy visual functions directly
visual = builtins.visual

# Create short aliases for the modules
dt = builtins.datetime
coll = builtins.collections
idx = builtins.indexing
vis = builtins.visual