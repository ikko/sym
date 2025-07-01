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
    if register_mixin(Symbol, 'head', property(SymbolDateTimeMixin.head.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'tail', property(SymbolDateTimeMixin.tail.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_date', property(SymbolDateTimeMixin.as_date.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_time', property(SymbolDateTimeMixin.as_time.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_datetime', property(SymbolDateTimeMixin.as_datetime.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'day', property(SymbolDateTimeMixin.day.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'hour', property(SymbolDateTimeMixin.hour.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'minute', property(SymbolDateTimeMixin.minute.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'second', property(SymbolDateTimeMixin.second.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'period', property(SymbolDateTimeMixin.period.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_period', property(SymbolDateTimeMixin.as_period.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'duration', property(SymbolDateTimeMixin.duration.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_duration', property(SymbolDateTimeMixin.as_duration.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'delta', property(SymbolDateTimeMixin.delta.fget)): successful_mixins += 1
    total_mixins += 1
    if register_mixin(Symbol, 'as_delta', property(SymbolDateTimeMixin.as_delta.fget)): successful_mixins += 1

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