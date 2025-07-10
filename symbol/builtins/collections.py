"""This module provides custom collection classes for Symbol objects.

It includes an OrderedSymbolSet, which is a set of Symbols that maintains insertion order.
"""
import threading

from ..core.base_symbol import Symbol


class OrderedSymbolSet:
    def __init__(self, items=None):
        """
        what: Initializes an OrderedSymbolSet instance.
        why: To create a set of Symbols that maintains insertion order.
        how: Uses an internal dictionary and a lock for thread safety.
        when: When a new ordered set of Symbols is needed.
        by (caller(s)): Symbol.children, Symbol.parents.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Creating an ordered collection.
        how, what, why and when to improve: Optimize for very large sets.
        """
        self._dict = dict()
        self._lock = threading.RLock()
        self._length = 0
        if items:
            for item in items:
                self.add(item)

    def add(self, sym: 'Symbol'):
        """
        what: Adds a Symbol to the set.
        why: To include a Symbol in the ordered collection.
        how: Adds to internal dictionary, increments length, patches if exists.
        when: When a Symbol needs to be added to the set.
        by (caller(s)): OrderedSymbolSet.__init__, Symbol.append.
        how often: Frequently.
        how much: Minimal.
        what is it like: Adding an item to a unique, ordered list.
        how, what, why and when to improve: Optimize for very large sets.
        """
        with self._lock:
            if sym.name not in self._dict:
                self._dict[sym.name] = sym
                self._length += 1
            else:
                self._dict[sym.name].patch(sym)

    def __iter__(self):
        """
        what: Provides an iterator for the Symbols in the set.
        why: To allow iteration over the ordered collection.
        how: Returns an iterator over the internal dictionary's values.
        when: When iterating over Symbols in the set.
        by (caller(s)): Python's iteration mechanism.
        how often: Frequently.
        how much: Minimal.
        what is it like: Looping through an ordered collection.
        how, what, why and when to improve: N/A.
        """
        return iter(self._dict.values())

    def __len__(self):
        """
        what: Returns the number of Symbols in the set.
        why: To get the size of the ordered collection.
        how: Returns the internal `_length` attribute.
        when: When the count of Symbols is needed.
        by (caller(s)): Python's `len()` function.
        how often: Frequently.
        how much: Minimal.
        what is it like: Counting elements in a collection.
        how, what, why and when to improve: N/A.
        """
        return self._length

    def __contains__(self, sym):
        """
        what: Checks if a Symbol is in the set.
        why: To determine if a Symbol is part of the collection.
        how: Checks if the Symbol's name is a key in the internal dictionary.
        when: When checking for Symbol membership.
        by (caller(s)): Python's `in` operator.
        how often: Frequently.
        how much: Minimal.
        what is it like: Checking for an item in a set.
        how, what, why and when to improve: N/A.
        """
        return sym.name in self._dict
