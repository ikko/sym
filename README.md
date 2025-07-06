# `«symbol»`
**A Framework for Symbolic Data Manipulation**

_inspired by ruby's [symbol](https://ruby-doc.org/core-2.5.3/Symbol.html)_

> `symbol.py` — A Lazy, Graph-Oriented, Immutable Symbol System Concept for Domain-Specific Abstraction

## What is Symbol?

**Symbol** is a namespace dsl. It is a Python framework for creating, manipulating, and analyzing complex, graph-based data structures. It provides a versatile `Symbol` object that serves as a node in a dynamic, directed acyclic graph (DAG). The framework is designed to be lean, modular, and extensible, making it suitable for a wide range of applications, from data science and AI to domain-specific modeling.


## Core Concepts

-   **Symbol**: The fundamental building block. Each symbol has a unique name and can be connected to other symbols, forming complex relationships.
-   **Flyweight Design**: Symbols are unique. `Symbol('a')` will always return the same object, saving memory and ensuring consistency.
-   **Layered Architecture**: The core is minimal. Functionality is added through modular, "builtin" extensions for features like date/time handling, advanced collections, and visualization.
-   **Per-Instance Indexing**: Every symbol has its own private, weighted index of other symbols, allowing for the creation of sophisticated, nested data structures.
-   **[Mixinability](docs/readme_details/5_mixinability/index.md)**: The framework supports dynamic extension of `Symbol` instances at runtime through mixins, which are validated for robustness.
-   **[Memory-Aware Maturing](docs/readme_details/6_memory_aware_maturing/index.md)**: Symbols can be "matured" to optimize memory usage and performance by elevating metadata and removing unused components.
-   **[Scheduling](docs/readme_details/7_scheduling/index.md)**: A built-in scheduler allows for deferred execution of functions and methods, specified with cron-like strings, datetime objects, or even other Symbols.

API Highlights:
---------------
- **[Symbol(name: str)](docs/readme_details/8_api_highlights/index.md#symbolname-str-globally-interned-idempotent-constructor)** — globally interned, idempotent constructor
- **[Symbol.next()](docs/readme_details/8_api_highlights/index.md#symbolnext-creates-and-chains-auto-numbered-symbols)** — creates and chains auto-numbered symbol (`sym_0`, `sym_1`, …)
- **[symbol.append(child) / symbol.relate_to(other, how)](docs/readme_details/8_api_highlights/index.md#symbolappendchild--symbolrelate_toother-how-link-construction)** — link construction
- **[symbol.tree() / .que() / .relate()](docs/readme_details/8_api_highlights/index.md#symboltree--que--relate-lazy-traversal)** — lazy traversal
- **[symbol.patch(other)](docs/readme_details/8_api_highlights/index.md#symbolpatchother-recursive-structural-deep-merge)** — recursive, structural deep merge (PATCH-like semantics)
- **[symbol.to_mmd()](docs/readme_details/8_api_highlights/index.md#symbolto_mmd-outputs-tree-graph-in-mermaid-diagram-syntax)** — outputs tree graph in Mermaid diagram syntax
- **[symbol.to_ascii()](docs/readme_details/8_api_highlights/index.md#symbolto_ascii-outputs-ascii-art-representation-of-graphs)** — outputs ASCII art representation of graphs
- **[symbol.delete()](docs/readme_details/8_api_highlights/index.md#symboldelete-removes-node-and-its-inverse-references)** — removes node and its inverse references (parents/children)
- **[symbol.elevate()](docs/readme_details/8_api_highlights/index.md#symbolelevate-promotes-metadata-to-instance-attributesmethods)** — promotes metadata to instance attributes/methods
- **[symbol.slim()](docs/readme_details/8_api_highlights/index.md#symbolslim-removes-unused-dynamically-applied-mixins)** — removes unused dynamically applied mixins
- **[symbol.immute()](docs/readme_details/8_api_highlights/index.md#symbolimmute-orchestrates-maturing-process-elevate-slim-freeze)** — orchestrates maturing process (elevate, slim, freeze)
- **[symbol.ref](docs/readme_details/8_api_highlights/index.md#symbolref-alias-for-symbolorigin-to-track-source-provenance)** — alias for `symbol.origin` to track source provenance
- **[Scheduler.add_job(job)](docs/readme_details/8_api_highlights/index.md#scheduleradd_jobjob-schedules-a-new-job-for-execution)** — schedules a new job for execution

Performance:
------------
For detailed performance analysis and empirical validation of Big O notations, refer to the [Performance Notations and Empirical Validation](docs/notations.md) document.

- O(1) symbol instantiation (intern pool)
- O(1) relationship linking
- O(1) traversal with cache and float-based cursor insertion
- O(log n) insert/search when extended to use bisect-based insertion order

Memory Awareness:
-----------------
-   **[Memory Awareness](docs/readme_details/10_memory_awareness/index.md)**: GC-aware deletion (respecting `ENABLE_ORIGIN`, `MEMORY_AWARE_DELETE`)
-   Proactive memory management for `context` attribute via `deep_del`

Extensibility:
--------------
- Easily extended with async traversal, typed relations, or backend persistence
- `Symbolable` type for robust callable integration
- `MixinFunction` protocol for formal mixin interface
- `SymbolAdapter` mixinable interface enables different logical structures
- Compatible with enum reflection and external DSL inputs

Example Use:
------------
- **[Practical Applications](docs/readme_details/12_example_use/index.md)**: Demonstrates how Symbol's core features can be leveraged to solve real-world problems.

Conclusion:
-----------
- **[Overview](docs/readme_details/13_conclusion/index.md)**: This module provides a high-performance, semantically rich, thread-safe symbol abstraction to power DSLs, runtime graphs, knowledge trees, and dynamic semantic layers. The design emphasizes structural clarity, cache efficiency, and symbolic extensibility.

## Project Structure

The project is organized into two main packages:

-   `symbol.core`: Contains the essential `Symbol` class and graph traversal logic.
-   `symbol.builtins`: Provides optional, high-level extensions for collections, date/time operations, index, pathfinding, and visualization.

```mermaid
graph TD
    A[User Application] --> B(symbol)
    B --> C{symbol.core}
    B --> D{symbol.builtins}
    C --> E[symbol.core.symbol]
    C --> F[symbol.core.graph]
    C --> G[symbol.core.schedule]
    D --> H[symbol.builtins.time_dim]
    D --> I[symbol.builtins.collections]
    D --> J[symbol.builtins.index]
    D --> K[symbol.builtins.path]
    D --> L[symbol.builtins.visual]
    D --> M[symbol.builtins.timeline]
    
    style A fill:#007BFF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style B fill:#228B22,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C fill:#FF8C00,stroke:#333,stroke-width:2px,color:#000000;
    style D fill:#800080,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style E fill:#FFA07A,stroke:#333,stroke-width:2px,color:#000000;
    style F fill:#FFA07A,stroke:#333,stroke-width:2px,color:#000000;
    style G fill:#FFA07A,stroke:#333,stroke-width:2px,color:#000000;
    style H fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style I fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style J fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style K fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style L fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style M fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
```

## Software Architecture

```mermaid
graph TD
    subgraph "Symbol Package"
        A[symbol] --> B(symbol.core)
        A --> C(symbol.builtins)
    end
    style A fill:#228B22,stroke:#333,stroke-width:2px,color:#FFFFFF;

    subgraph "Core Modules"
        B --> B1[symbol.core.symbol]
        B --> B3[symbol.core.maturing]
        B --> B4[symbol.core.mixinability]
        B --> B5[symbol.core.mixin_validator]
        B --> B6[symbol.core.protocols]
        B --> B7[symbol.core.symbolable]
        B --> B8[symbol.core.time_arithmetics]
        B --> B9[symbol.core.schedule]
    end
    style B fill:#FF8C00,stroke:#333,stroke-width:2px,color:#000000;

    subgraph "Builtin Extensions"
        C --> C1[symbol.builtins.collections]
        C --> C2[symbol.builtins.time_dim]
        C --> C3[symbol.builtins.index]
        C --> C4[symbol.builtins.path]
        C --> C5[symbol.builtins.visual]
        C --> C6[symbol.builtins.red_black_tree]
        C --> C7[symbol.builtins.avl_tree]
        C --> C8[symbol.builtins.timeline]
    end
    style C fill:#800080,stroke:#333,stroke-width:2px,color:#FFFFFF;

    B1 -- uses --> B3
    B1 -- uses --> B4
    B1 -- uses --> C1
    B1 -- uses --> C3

    B4 -- uses --> B5
    B4 -- uses --> B6
    B4 -- uses --> B7
    
    B9 -- uses --> B1

    C2 -- uses --> B1
    C3 -- uses --> B1
    C4 -- uses --> B1
    C5 -- uses --> B1
    C6 -- uses --> B1
    C7 -- uses --> B1
    C8 -- uses --> B1

    C3 -- uses --> C6
    C3 -- uses --> C7

    C5 -- uses --> B8
    C8 -- uses --> B8

    style B1 fill:#FFA07A,stroke:#333,stroke-width:2px,color:#000000;
    style B3 fill:#FFA07A,stroke:#333,stroke-width:2px,color:#000000;
    style B4 fill:#FFA07A,stroke:#333,stroke-width:2px,color:#000000;
    style B5 fill:#FFA07A,stroke:#333,stroke-width:2px,color:#000000;
    style B6 fill:#FFA07A,stroke:#333,stroke-width:2px,color:#000000;
    style B7 fill:#FFA07A,stroke:#333,stroke-width:2px,color:#000000;
    style B8 fill:#FFA07A,stroke:#333,stroke-width:2px,color:#000000;
    style B9 fill:#FFA07A,stroke:#333,stroke-width:2px,color:#000000;

    style C1 fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C2 fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C3 fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C4 fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C5 fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C6 fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C7 fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C8 fill:#9370DB,stroke:#333,stroke-width:2px,color:#FFFFFF;
```

## Getting Started

To begin, simply import the `Symbol` or `s` namespace factory:

```python
>>> from symbol import Symbol, s

>>> # Create symbols
>>> hello = Symbol('hello')
>>> world = s.world

>>> # Build relationships
>>> hello.add(world)

>>> # Traverse the graph
>>> print(hello.tree())
```
<details>

```text
[<Symbol: hello>, <Symbol: world>]
```
</details>

## Running Tests

To run all tests, execute the following command from the project root directory:

```bash
>>> python -m pytest tests
```
<details>

```text
============================= test session starts ==============================
platform linux -- Python 3.13.3, pytest-8.4.1, pluggy-1.6.0 -- /home/miki/.virtualenvs/gemini/bin/python3
cachedir: .pytest_cache
rootdir: /home/miki/code/ikko/symbol
configfile: pytest.ini
plugins: anyio-4.9.0, cov-6.2.1
collected 62 items

tests/builtins/test_collections.py::test_ordered_symbol_set_creation_and_add PASSED
tests/builtins/test_collections.py::test_ordered_symbol_set_iteration_length_and_containment PASSED
tests/builtins/test_index.py::test_symbol_index_instantiation PASSED
tests/builtins/test_index.py::test_symbol_index_insertion PASSED
tests/builtins/test_index.py::test_symbol_index_traverse_inorder PASSED
tests/builtins/test_index.py::test_symbol_index_traverse_preorder PASSED
tests/builtins/test_index.py::test_symbol_index_traverse_postorder PASSED
tests/builtins/test_index.py::test_symbol_index_map_and_filter PASSED
tests/builtins/test_index.py::test_symbol_index_ascii_representation PASSED
tests/builtins/test_path.py::test_path_to_direct_path PASSED
tests/builtins/test_path.py::test_path_to_no_path PASSED
tests/builtins/test_path.py::test_path_to_self PASSED
tests/builtins/test_path.py::test_path_to_with_cycle PASSED
tests/builtins/test_path.py::test_match_dfs PASSED
tests/builtins/test_path.py::test_match_bfs PASSED
tests/builtins/test_path.py::test_match_no_match PASSED
tests/builtins/test_path.py::test_match_all_match PASSED
tests/builtins/test_time_dim.py::test_parse_timestamp PASSED
tests/builtins/test_time_dim.py::test_symbol_time_dim_properties PASSED
tests/builtins/test_time_dim.py::test_symbol_head_and_tail[setup_and_teardown0] PASSED
tests/builtins/test_time_dim.py::test_symbol_period_properties[setup_and_teardown0] PASSED
tests/builtins/test_time_dim.py::test_symbol_period_properties[setup_and_teardown1] PASSED
tests/builtins/test_visual.py::test_to_mmd_simple_tree PASSED
tests/builtins/test_visual.py::test_to_mmd_simple_graph PASSED
tests/core/test_mixinability.py::test_freeze_and_is_frozen_states PASSED
tests/core/test_mixinability.py::test_register_mixin_basic_application PASSED
tests/core/test_schedule.py::test_scheduler_instantiation PASSED
tests/core/test_symbol_creation.py::test_symbol_creation_and_interning PASSED
tests/core/test_symbol_creation.py::test_symbol_equality_and_hashing PASSED
tests/core/test_symbol_creation.py::test_symbol_string_representation PASSED
tests/core/test_symbol_creation.py::test_symbol_basic_graph_operations PASSED
tests/core/test_symbol_creation.py::test_symbol_namespace PASSED
tests/core/test_symbol_happy_path.py::test_symbol_creation_and_interning PASSED
tests/core/test_symbol_happy_path.py::test_symbol_equality_and_hashing PASSED
tests/core/test_symbol_happy_path.py::test_symbol_string_representation PASSED
tests/core/test_symbol_happy_path.py::test_symbol_basic_graph_operations PASSED
tests/core/test_symbol_happy_path.py::test_symbol_namespace PASSED
tests/test_config.py::test_config_default_path PASSED
tests/test_config.py::test_config_load_save PASSED
tests/test_config.py::test_config_get_set_methods PASSED
tests/test_conversion/test_conversions.py::test_from_int PASSED
tests/test_conversion/test_conversions.py::test_int_to_sym PASSED
tests/test_conversion/test_conversions.py::test_from_float PASSED
tests/test_conversion/test_conversions.py::test_float_to_sym PASSED
tests/test_conversion/test_conversions.py::test_from_str PASSED
tests/test_conversion/test_conversions.py::test_str_to_sym PASSED
tests/test_conversion/test_conversions.py::test_from_bool PASSED
tests/test_conversion/test_conversions.py::test_bool_to_sym PASSED
tests/test_conversion/test_conversions.py::test_from_none PASSED
tests/test_conversion/test_conversions.py::test_none_to_sym PASSED
tests/test_conversion/test_conversions.py::test_from_list PASSED
tests/test_conversion/test_conversions.py::test_list_to_sym PASSED
tests/test_conversion/test_conversions.py::test_from_dict PASSED
tests/test_conversion/test_conversions.py::test_dict_to_sym PASSED
tests/test_conversion/test_conversions.py::test_from_tuple PASSED
tests/test_conversion/test_conversions.py::test_tuple_to_sym PASSED
tests/test_conversion/test_conversions.py::test_from_set PASSED
tests/test_conversion/test_conversions.py::test_set_to_sym PASSED
tests/test_conversion/test_conversions.py::test_nested_conversion PASSED
tests/test_conversion/test_conversions.py::test_global_to_sym_fallback PASSED
tests/test_imports.py::test_direct_imports_skip_time_dim PASSED
tests/test_imports.py::test_direct_imports_skip_core_and_builtins PASSED

========================= 62 passed in 0.10s =========================
```
</details>