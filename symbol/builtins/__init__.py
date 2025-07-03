from ..core.base_symbol import Symbol
from ..core.mixinability import register_mixin
from .path import SymbolPathMixin
from .datetime import SymbolDateTimeMixin
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

    # DateTime Mixin
    total_mixins += 1
    if register_mixin(Symbol, '_parse_timestamp', SymbolDateTimeMixin._parse_timestamp): successful_mixins += 1
    
    total_mixins += 1
    if register_mixin(Symbol, 'time_head', SymbolDateTimeMixin.time_head): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'time_tail', SymbolDateTimeMixin.time_tail): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_date', SymbolDateTimeMixin.as_date): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_time', SymbolDateTimeMixin.as_time): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_datetime', SymbolDateTimeMixin.as_datetime): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'day', SymbolDateTimeMixin.day): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'hour', SymbolDateTimeMixin.hour): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'minute', SymbolDateTimeMixin.minute): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'second', SymbolDateTimeMixin.second): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'period', SymbolDateTimeMixin.period): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_period', SymbolDateTimeMixin.as_period): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'duration', SymbolDateTimeMixin.duration): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_duration', SymbolDateTimeMixin.as_duration): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'delta', SymbolDateTimeMixin.delta): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_delta', SymbolDateTimeMixin.as_delta): successful_mixins += 1

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