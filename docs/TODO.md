# TODO List for Enhanced Relationship Management

- [ ] Create `symb/core/relations.py` and implement the `Relationships` class.
- [ ] Modify `symb/core/base_symb.py`:
    - [ ] Remove `related_to` and `related_how` from `__slots__`.
    - [ ] Add `relations` to `__slots__`.
    - [ ] Initialize `self.relations` in `Symbol.__new__`.
- [ ] Modify `symb/core/symb.py`:
    - [ ] Import the `Relationships` class.
    - [ ] Update the `relate` method.
    - [ ] Update the `unrelate` method.
    - [ ] Update the `to_mmd` method.
    - [ ] Implement the dynamic relationship creation in `__getattr__`.
- [ ] Create `tests/core/test_relations.py` and add comprehensive tests for the new functionality.
