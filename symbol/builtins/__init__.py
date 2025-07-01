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
    if register_mixin(Symbol, '_sorted_by_time', SymbolDateTimeMixin._sorted_by_time): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'head', property(lambda self: SymbolDateTimeMixin.head.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'tail', property(lambda self: SymbolDateTimeMixin.tail.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_date', property(lambda self: SymbolDateTimeMixin.as_date.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_time', property(lambda self: SymbolDateTimeMixin.as_time.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_datetime', property(lambda self: SymbolDateTimeMixin.as_datetime.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'day', property(lambda self: SymbolDateTimeMixin.day.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'hour', property(lambda self: SymbolDateTimeMixin.hour.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'minute', property(lambda self: SymbolDateTimeMixin.minute.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'second', property(lambda self: SymbolDateTimeMixin.second.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'period', property(lambda self: SymbolDateTimeMixin.period.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_period', property(lambda self: SymbolDateTimeMixin.as_period.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'duration', property(lambda self: SymbolDateTimeMixin.duration.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_duration', property(lambda self: SymbolDateTimeMixin.as_duration.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'delta', property(lambda self: SymbolDateTimeMixin.delta.fget(self))): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_delta', property(lambda self: SymbolDateTimeMixin.as_delta.fget(self))): successful_mixins += 1

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