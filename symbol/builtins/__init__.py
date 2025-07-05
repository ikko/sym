from ..core.base_symbol import Symbol
from ..core.mixinability import register_mixin
from .path import SymbolPathMixin
from .time_dim import SymbolTimeDimMixin
from .visual import to_dot, a_to_svg, to_svg, a_to_png, to_png, to_mmd, to_ascii
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

    # Visual functions (proxied from symbol.builtins.visual)
    total_mixins += 1
    if register_mixin(Symbol, 'to_dot', to_dot): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'a_to_svg', a_to_svg): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'to_svg', to_svg): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'a_to_png', a_to_png): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'to_png', to_png): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'to_mmd', to_mmd): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'to_ascii', to_ascii): successful_mixins += 1

    log.info(f"Mixin application complete. Successfully applied {successful_mixins} of {total_mixins} mixins.")
