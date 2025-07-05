# TODO List for Symbol Project

This document tracks the remaining tasks and future enhancements for the Symbol project.

## Pending Tasks

- [ ] Replace `datetime` with `pendulum` throughout the codebase where functionality exists.
  - [x] Rename `symbol/builtins/datetime.py` to `symbol/builtins/time_dim.py`.
  - [ ] Update all references to `symbol.builtins.datetime` to `symbol.builtins.time_dim`.
  - [ ] Refactor `symbol/builtins/time_dim.py` to use `pendulum`.
  - [x] Update `symbol/core/protocols.py` to use `pendulum` and `SymbolTimeDimProtocol`.
  - [x] Update `symbol/core/schedule.py` to use `pendulum`.
  - [x] Update `symbol/core/symbol.py` to use `pendulum`.
  - [x] Update `symbol/builtins/index.py` to use `pendulum`.
  - [x] Update `symbol/builtins/timeline.py` to use `pendulum`.
  - [x] Update `tests/builtins/test_time_dim.py` to use `pendulum` and `SymbolTimeDimMixin`.
  - [x] Update `tests/builtins/time_dim.feature` to reflect `time_dim`.
  - [x] Update `docs/architecture.md` to reflect `time_dim`.
  - [x] Update `docs/module_paths_diagram.md` to reflect `time_dim`.
  - [x] Update `docs/1_quick_guide.md` to reflect `time_dim` and `pendulum`.
  - [x] Update `docs/2_introduction.md` to reflect `time_dim` and `pendulum`.
  - [x] Update `docs/3_advanced_tutorial.md` to reflect `time_dim` and `pendulum`.
  - [x] Update `docs/readme_details/7_scheduling/index.md` to reflect `time_dim` and `pendulum`.
  - [x] Update `docs/readme_details/8_api_highlights/index.md` to reflect `time_dim` and `pendulum`.
  - [x] Update `docs/readme_details/12_example_use/index.md` to reflect `time_dim` and `pendulum`.
  - [x] Update `docs/methods.md` to reflect `time_dim` and `pendulum`.
  - [x] Update `docs/namespace_dsl_spec.md` to reflect `time_dim`.
  - [x] Update `docs/user_info_journey.md` to reflect `time_dim`.
  - [x] Update `docs/notations.md` to reflect `time_dim`.
  - [x] Update `docs/GLOSSARY.md` to reflect `time_dim`.
  - [x] Update `docs/GOOD_TO_KNOW.md` to reflect `time_dim`.
  - [x] Update `docs/idohatarozok.md` to reflect `time_dim`.
  - [x] Update `docs/directory_validation.md` to reflect `time_dim`.
  - [ ] Add new tests to cover direct imports by skipping `time_dim`, `core`, and `builtins`.

- [ ] Implement `pendulum` functionalities that `datetime` has but `pendulum` does not (if any).
- [ ] Identify functionalities that both `pendulum` and `datetime` have.
- [ ] Identify functionalities that `datetime` has but `pendulum` does not.

## Future Enhancements

- [ ] Implement `SymbolAdapter` for new traversal topologies.
- [ ] Develop async-ready traversal engine.
- [ ] Explore more frontend-ready output formats.
