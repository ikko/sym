"""This module provides custom collection classes for Symbol objects.

It includes an OrderedSymbolSet, which is a set of Symbols that maintains insertion order.
"""
import threading

from ..core.base_symb import Symbol


class OrderedSymbolSet:
    def __init__(self, items=None):
        self._dict = dict()
        self._lock = threading.RLock()
        self._length = 0
        if items:
            for item in items:
                self.add(item)

    def add(self, sym: 'Symbol'):
        with self._lock:
            if sym.name not in self._dict:
                self._dict[sym.name] = sym
                self._length += 1
            else:
                self._dict[sym.name].patch(sym)

    def __iter__(self):
        return iter(self._dict.values())

    def __len__(self):
        return self._length

    def __contains__(self, sym):
        return sym.name in self._dict
