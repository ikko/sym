from ..core.base_symbol import Symbol
from ..core.mixinability import register_mixin
from .path import SymbolPathMixin
from .time_dim import SymbolTimeDimMixin
from .visual import SymbolRender
from .timeline import Timeline
import logging

log = logging.getLogger(__name__)

def apply_builtins():
    successful_mixins = 0
    total_mixins = 0

    # Path Mixin
    total_mixins += 1
    if register_mixin(Symbol, 'path_to', SymbolPathMixin.path_to): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'match', SymbolPathMixin.match): successful_mixins += 1

    # Time Dimension Mixin
    total_mixins += 1
    if register_mixin(Symbol, '_parse_timestamp', SymbolTimeDimMixin._parse_timestamp): successful_mixins += 1
    
    total_mixins += 1
    if register_mixin(Symbol, 'time_head', SymbolTimeDimMixin.time_head): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'time_tail', SymbolTimeDimMixin.time_tail): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_date', SymbolTimeDimMixin.as_date): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_time', SymbolTimeDimMixin.as_time): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_datetime', SymbolTimeDimMixin.as_datetime): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'day', SymbolTimeDimMixin.day): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'hour', SymbolTimeDimMixin.hour): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'minute', SymbolTimeDimMixin.minute): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'second', SymbolTimeDimMixin.second): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'period', SymbolTimeDimMixin.period): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_period', SymbolTimeDimMixin.as_period): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'duration', SymbolTimeDimMixin.duration): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_duration', SymbolTimeDimMixin.as_duration): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'delta', SymbolTimeDimMixin.delta): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_delta', SymbolTimeDimMixin.as_delta): successful_mixins += 1

    # Visual Mixin
    visual_methods = [
        'to_dot', 'a_to_svg', 'to_svg', 'a_to_png', 'to_png', 'to_mmd', 'to_ascii'
    ]
    for method_name in visual_methods:
        total_mixins += 1
        if register_mixin(Symbol, method_name, getattr(SymbolRender, method_name)): successful_mixins += 1

    log.info(f"Mixin application complete. Successfully applied {successful_mixins} of {total_mixins} mixins.")
