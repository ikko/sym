# TODO

- [x] Create `symb/core/relations.py` with the `Relations` class.
- [x] Implement `__init__`, `__getattr__`, `__setattr__`, and `__call__` in the `Relations` class.
- [x] Use `weakref.WeakSet` for storing related symbols.
- [x] Remove `related_to` and `related_how` from `__slots__` in `symb/core/base_symb.py`.
- [x] Add `relations` to `__slots__` in `symb/core/base_symb.py`.
- [x] Initialize `relations` in `BaseSymbol.__new__`.
- [x] Remove `relate` and `unrelate` methods from `symb/core/symb.py`.
- [x] Update `Symbol.__getattr__` to delegate to the `relations` object.
- [x] Update `to_mmd` to use the new `relations` object.
- [x] Update tests in `tests/core/test_symbol.py`.
- [x] Create new tests for the advanced relational system.
- [x] Update documentation.