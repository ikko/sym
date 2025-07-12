
# Implementation Plan: Advanced Relational System

This document outlines the plan to refactor the relational system in the `Symbol` class.

## 1. Introduce the `Relations` Class

- **Location:** `symb/core/relations.py` (new file)
- **Functionality:**
    - [x] Inherit from `collections.abc.MutableMapping` to provide a dictionary-like interface.
    - [x] Implement `__getattr__` and `__setattr__` to allow dot notation access to relations.
    - [x] Store relations in an internal dictionary, where keys are the `how` and values are `weakref.WeakSet` of related symbols.
    - [x] Implement `__call__` to handle the dynamic relation creation.

## 2. Refactor `Symbol` and `BaseSymbol`

- **`symb/core/base_symb.py`:**
    - [x] Remove `related_to` and `related_how` from `__slots__`.
    - [x] Add a new `relations` attribute to `__slots__`.
    - [x] In `__new__`, initialize `relations` as an instance of the `Relations` class.

- **`symb/core/symb.py`:**
    - [x] Remove the existing `relate` and `unrelate` methods.
    - [x] Modify `__getattr__` to delegate to the `relations` object if an attribute is not found on the `Symbol` itself. This will be the entry point for the dynamic relation creation.
    - [x] The `__getattr__` will catch the `AttributeError`, and interpret the call as a relation.

## 3. Implement the Dynamic Relation Logic

- [x] In the `Relations` class, the `__getattr__` method will be the core of the dynamic relation creation.
- [x] It will return a callable object (e.g., a `functools.partial` or a small custom class) that captures the `how` of the relation.
- [x] This callable object will then handle the `*args` and `**kwargs` as described in the proposal.

## 4. Update Dependent Code

- [x] **`to_mmd`:** Modify the `to_mmd` method in `symb/core/symb.py` to use the new `relations` object for generating the graph.
- [x] **Tests:** Update all tests in `tests/core/test_symbol.py` that currently rely on `related_to` and `related_how`. Create new tests for the new relational system, covering all the specified use cases.

## 5. Documentation

- [x] Update all relevant documentation to reflect the new relational system.
