# Changelog

## [Unreleased]
- Nothing yet!

## [v0.0.9] - 2025-07-13
### Added
- **Dynamic Relation Syntax**: Introduced a more intuitive and expressive API for defining relationships between `Symbol` instances (e.g., `sym.relates_to(other)` instead of `sym.relate(other, how='relates_to')`). This enhances the readability and semantic clarity of graph construction, aligning with principles of Domain-Specific Languages (DSLs).
- **Comprehensive Serialization/Deserialization**: Added robust capabilities for persisting and reconstructing `Symbol` graphs to/from various structured data formats: JSON (`to_json`, `from_json`), YAML (`to_yaml`, `from_yaml`), and TOML (`to_toml`, `from_toml`). This significantly improves data interchange, reproducibility, and integration with external systems.
- **ASCII Graph Round-trip**: Implemented `Symbol.from_ascii()` to complement the enhanced `Symbol.to_ascii()`, enabling full round-trip serialization of `Symbol` graphs into human-readable ASCII representations. This is invaluable for debugging, visualization, and simplified data sharing.
- **Configurable Graph Traversal**: Introduced a dedicated `GraphTraversal` class with parameters (`traverse_mode`, `family_mode`, `graph_mode`) for fine-grained control over graph exploration strategies (DFS, BFS, and specific family/general relation traversal orders). This provides greater flexibility for algorithmic development and analysis.
- **PyPI-Optimized Documentation**: Integrated a new `docs/pypi_org/` directory with scripts (`start.sh`, `update.py`) to generate a PyPI-specific `README.md` that includes rendered SVG diagrams and transformed links. This enhances the project's presentation and accessibility on the Python Package Index.
- **Formalized Development Planning**: Added `docs/plan.md` and `docs/todo.md` to formalize development planning and task tracking, promoting a more structured and transparent project management approach.
- **Software Architecture Overview**: Included `docs/software_architecture.md` to provide a high-level overview of the system's design, aiding in comprehension for new contributors and facilitating architectural discussions.

### Changed
- **Architectural Decomposition**: Performed a significant refactoring of the core `Symbol` implementation, decomposing `symb/core/symb.py` into `symb/core/symbol.py` (for core `Symbol` logic) and `symb/core/symbol_namespace.py` (for the `s` namespace and related utilities). This enhances modularity, reduces coupling, and improves maintainability.
- **Module Renaming**: Renamed the `symb/builtins` package to `symb/builtin` for improved naming consistency and adherence to Python's standard library conventions. All internal and external references have been updated accordingly.
- **Python Version Requirement**: Increased the minimum required Python version from `3.6` to `3.8` in `pyproject.toml` to leverage modern language features and ensure compatibility with contemporary development environments.
- **Project Metadata**: Updated `pyproject.toml` with comprehensive project metadata, including PyPI classifiers, author information, and explicit URLs for homepage, repository, and documentation. This improves project discoverability and formalizes its distribution.
- **Test Fixture Refinement**: Modified `tests/conftest.py` to introduce a more robust `symb_fixture` that ensures a clean `Symbol._pool` state for each test and pre-populates a complex bioinformatics graph for comprehensive testing of graph operations and serialization.

### Fixed
- Minor documentation inconsistencies and code formatting issues across various files.

## [v0.0.6] - 2025-07-10
- Initial release of the package with basic functionality, including:
  - Core `Symbol` object with interning mechanism for unique identity.
  - Basic parent-child graph relationships.
  - Mixin-based extensibility for dynamic behavior injection.
  - Preliminary graph traversal capabilities.
  - Memory-aware object management.
