from ..core.symbol import Symbol
from ..core.pluggability import register_patch
from .path import SymbolPathMixin
from .datetime import SymbolDateTimeMixin
from .visual import to_dot, a_to_svg, to_svg, a_to_png, to_png, to_mmd, to_ascii

def apply_builtins():
    # Path Mixin
    register_patch(Symbol, 'path_to', SymbolPathMixin.path_to)
    register_patch(Symbol, 'match', SymbolPathMixin.match)

    # DateTime Mixin
    register_patch(Symbol, 'head', property(SymbolDateTimeMixin.head.fget))
    register_patch(Symbol, 'tail', property(SymbolDateTimeMixin.tail.fget))
    register_patch(Symbol, 'as_date', property(SymbolDateTimeMixin.as_date.fget))
    register_patch(Symbol, 'as_time', property(SymbolDateTimeMixin.as_time.fget))
    register_patch(Symbol, 'as_datetime', property(SymbolDateTimeMixin.as_datetime.fget))
    register_patch(Symbol, 'day', property(SymbolDateTimeMixin.day.fget))
    register_patch(Symbol, 'hour', property(SymbolDateTimeMixin.hour.fget))
    register_patch(Symbol, 'minute', property(SymbolDateTimeMixin.minute.fget))
    register_patch(Symbol, 'second', property(SymbolDateTimeMixin.second.fget))
    register_patch(Symbol, 'period', property(SymbolDateTimeMixin.period.fget))
    register_patch(Symbol, 'as_period', property(SymbolDateTimeMixin.as_period.fget))
    register_patch(Symbol, 'duration', property(SymbolDateTimeMixin.duration.fget))
    register_patch(Symbol, 'as_duration', property(SymbolDateTimeMixin.as_duration.fget))
    register_patch(Symbol, 'delta', property(SymbolDateTimeMixin.delta.fget))
    register_patch(Symbol, 'as_delta', property(SymbolDateTimeMixin.as_delta.fget))

    # Visual functions (proxied from symbol.builtins.visual)
    register_patch(Symbol, 'to_dot', to_dot)
    register_patch(Symbol, 'a_to_svg', a_to_svg)
    register_patch(Symbol, 'to_svg', to_svg)
    register_patch(Symbol, 'a_to_png', a_to_png)
    register_patch(Symbol, 'to_png', to_png)
    register_patch(Symbol, 'to_mmd', to_mmd)
    register_patch(Symbol, 'to_ascii', to_ascii)