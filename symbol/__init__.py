from .core.base_symbol import Symbol
from .core.symbol import s
from .core.symbol import GraphTraversal
from .core.mixinability import freeze, is_frozen
from .core.time_arithmetics import add_time_objects, subtract_time_objects
from .core.batch_processing import a_process_batch, process_batch
from .config import Config
from . import builtins
from .builtins import apply_builtins

# Apply the mixins first to ensure the Symbol class is fully featured
apply_builtins()

# --- User-facing aliases for convenience ---

# Expose builtin modules at the top level
datetime = builtins.datetime
collections = builtins.collections
indexing = builtins.indexing
path = builtins.path
timeline = builtins.timeline

# Proxy visual functions directly
visual = builtins.visual

# Expose time arithmetic functions
add_time = add_time_objects
subtract_time = subtract_time_objects

# Expose batch processing functions
a_process_batch = a_process_batch
process_batch = process_batch

# Create short aliases for the modules
dt = builtins.datetime
coll = builtins.collections
idx = builtins.indexing
vis = builtins.visual
tl = builtins.timeline