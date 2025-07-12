import collections.abc
from weakref import WeakSet

class Relations:
    def __init__(self, owner):
        self._owner = owner
        self._relations = {}

    def __getattr__(self, how):
        if how.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{how}'")

        def relation_proxy(*args, **kwargs):
            if not args and not kwargs:
                raise TypeError(f"'{how}' relation requires at least one argument or keyword argument.")

            # Handle positional arguments
            for arg in args:
                try:
                    sym_arg = self._owner.from_object(arg) # Convert to Symbol
                except TypeError:
                    raise TypeError(f"Cannot convert positional argument '{arg}' to Symbol for '{how}' relation.")
                self._owner.relate(sym_arg, how=how)

            # Handle keyword arguments
            for key, value in kwargs.items():
                if isinstance(value, list):
                    for item in value:
                        try:
                            sym_item = self._owner.from_object(item) # Convert to Symbol
                        except TypeError:
                            raise TypeError(f"Cannot convert list item '{item}' to Symbol for '{key}' relation.")
                        self._owner.relate(sym_item, how=key)
                else:
                    try:
                        sym_value = self._owner.from_object(value) # Convert to Symbol
                    except TypeError:
                        raise TypeError(f"Cannot convert keyword argument value '{value}' to Symbol for '{key}' relation.")
                    self._owner.relate(sym_value, how=key)
            return self._owner

        return relation_proxy

    def add(self, how, related_symbol):
        if how not in self._relations:
            self._relations[how] = WeakSet()
        self._relations[how].add(related_symbol)

    def get(self, how):
        return self._relations.get(how, WeakSet())

    def remove(self, how, related_symbol):
        if how in self._relations and related_symbol in self._relations[how]:
            self._relations[how].remove(related_symbol)
            if not self._relations[how]:
                del self._relations[how]

    def items(self):
        return self._relations.items()

    def __iter__(self):
        return iter(self._relations)

    def __len__(self):
        return len(self._relations)

    def __repr__(self):
        return f"<Relations of {self._owner.name}>"