# TODO

- [x] Make `AVLTree` iterable to fix the `TypeError` in `symbol.slim()`.
- [x] Implement `symbol.footprint()` to calculate the memory usage of a symbol.
- [x] Implement `symbol.ls` to list all loaded symbols with their name, footprint, and origin.
- [x] Ensure `symbol.slim()` removes all attributes that are not storing data (i.e., have a `_sentinel` value).
- [x] Move the current functionality of `.ls` to `.ps`.
- [x] Implement the new `.ls` to show all available modules.
- [x] Implement `.stat()` to show mixin statistics.
- [x] Verify and fix the `schedule` mixin for sync, async, batch, and single modes.
- [x] Write parameterized tests for the `schedule` mixin.
- [x] Un-skip and fix the scheduler tests.
- [ ] Provide a summary of the changes made.