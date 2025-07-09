from ..core.mixinability import register_mixin
from .path import SymbolPathMixin
from .time_dim import SymbolTimeDimMixin
from .visual import SymbolRender
from .timeline import Timeline
import logging

log = logging.getLogger(__name__)

def apply_builtins():
    from ..core.base_symb import Symbol
    successful_mixins = 0
    total_mixins = 0

    # Path Mixin
    total_mixins += 1
    if register_mixin(SymbolPathMixin.path_to, 'path_to'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolPathMixin.match, 'match'): successful_mixins += 1

    # Time Dimension Mixin
    
    
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.time_head, 'time_head'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.time_tail, 'time_tail'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.as_date, 'as_date'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.as_time, 'as_time'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.as_datetime, 'as_datetime'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.day, 'day'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.hour, 'hour'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.minute, 'minute'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.second, 'second'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.period, 'period'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.as_period, 'as_period'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.duration, 'duration'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.as_duration, 'as_duration'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.delta, 'delta'): successful_mixins += 1
    total_mixins += 1
    if register_mixin(SymbolTimeDimMixin.as_delta, 'as_delta'): successful_mixins += 1

    # Visual Mixin
    visual_methods = [
        'to_dot', 'a_to_svg', 'to_svg', 'a_to_png', 'to_png', 'to_mmd', 'to_ascii'
    ]
    for method_name in visual_methods:
        total_mixins += 1
        if register_mixin(getattr(SymbolRender, method_name), method_name): successful_mixins += 1

    log.debug(f"Mixin application complete. Successfully applied {successful_mixins} of {total_mixins} mixins.")
