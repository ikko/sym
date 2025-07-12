
# Implementation Plan for Enhanced Relationship Management

This document outlines the plan to refactor the relationship management system in the `Symbol` class. The current list-based approach will be replaced with a more powerful and intuitive dictionary-like object that supports attribute-style access and dynamic relationship creation.

## 1. New `Relationships` Class

A new class, `Relationships`, will be created to manage the relationships of a `Symbol`. This class will be a custom dictionary-like object with the following features:

-   It will inherit from `collections.abc.MutableMapping` to provide standard dictionary methods (`__getitem__`, `__setitem__`, `__delitem__`, `__iter__`, `__len__`).
-   It will implement `__getattr__` and `__setattr__` to allow for attribute-style access to relationships.
-   It will store relationships in an internal dictionary, where keys are the `how` strings and values are lists of related `Symbol` objects.

## 2. `Symbol` Class Modification

The `Symbol` class in `symb/core/base_symb.py` and `symb/core/symb.py` will be modified as follows:

-   The `related_to` and `related_how` attributes will be removed from the `__slots__` in `base_symb.py`.
-   A new attribute, `relations`, will be added to the `__slots__` in `base_symb.py`.
-   In the `Symbol` class's `__new__` method, `self.relations` will be initialized as an instance of the new `Relationships` class.
-   The `relate` and `unrelate` methods in `symb.py` will be updated to use the new `relations` object.
-   The `to_mmd` method in `symb.py` will be updated to iterate over the `relations` object.

## 3. Dynamic Relationship Creation via `__getattr__`

The `Symbol` class's `__getattr__` method will be enhanced to intercept calls to undefined methods. The logic will be as follows:

1.  If an `AttributeError` is caught, the method name will be interpreted as the `how` of a relationship.
2.  The arguments of the call will be interpreted as the `Symbol`s to be related.
3.  The keyword arguments of the call will be interpreted as additional relationships to be created.
4.  The `Symbol.from_object` method will be used to convert arguments to `Symbol` instances.
5.  If no arguments can be converted to `Symbol`s, a `TypeError` will be raised.

## 4. Implementation Steps

1.  **Create `Relationships` class:** Implement the `Relationships` class in a new file, `symb/core/relations.py`.
2.  **Update `base_symb.py`:** Modify the `Symbol` class in `base_symb.py` to remove `related_to` and `related_how` and add the `relations` attribute.
3.  **Update `symb.py`:**
    -   Import the `Relationships` class.
    -   Update the `Symbol` class's `__new__` method to initialize `self.relations`.
    -   Update the `relate`, `unrelate`, and `to_mmd` methods.
    -   Implement the new `__getattr__` logic.
4.  **Testing:** Create a new test file, `tests/core/test_relations.py`, to thoroughly test the new functionality.

This plan ensures a modular and clean implementation, separating the relationship management logic into its own class while integrating it seamlessly with the existing `Symbol` class.
