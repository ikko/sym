# Symbol: A Framework for Symbolic Data Manipulation

**Symbol** is a Python framework for creating, manipulating, and analyzing complex, graph-based data structures. It provides a versatile `Symbol` object that serves as a node in a dynamic, directed acyclic graph (DAG). The framework is designed to be lean, modular, and extensible, making it suitable for a wide range of applications, from data science and AI to domain-specific modeling.

# «symbol» namespace dsl

> `symbol.py` — A Lazy, Graph-Oriented, Immutable Symbol System for Domain-Specific Abstraction

_inspired by ruby's [symbol](https://ruby-doc.org/core-2.5.3/Symbol.html)_

## Core Concepts

-   **Symbol**: The fundamental building block. Each symbol has a unique name and can be connected to other symbols, forming complex relationships.
-   **Flyweight Design**: Symbols are unique. `Symbol('a')` will always return the same object, saving memory and ensuring consistency.
-   **Layered Architecture**: The core is minimal. Functionality is added through modular, "builtin" extensions for features like date/time handling, advanced collections, and visualization.
-   **Per-Instance Indexing**: Every symbol has its own private, weighted index of other symbols, allowing for the creation of sophisticated, nested data structures.
-   **Mixinability**: The framework supports dynamic extension of `Symbol` instances at runtime through mixins, which are validated for robustness.
-   **Memory-Aware Maturing**: Symbols can be "matured" to optimize memory usage and performance by elevating metadata and removing unused components.

API Highlights:
---------------
- `Symbol(name: str)` — globally interned, idempotent constructor
- `Symbol.next()` — creates and chains auto-numbered symbol (`sym_0`, `sym_1`, …)
- `symbol.append(child)` / `symbol.relate_to(other, how)` — link construction
- `symbol.tree()` / `.que()` / `.relate()` — lazy traversal
- `symbol.patch(other)` — recursive, structural deep merge (PATCH-like semantics)
- `symbol.to_mmd()` — outputs tree graph in Mermaid diagram syntax
- `symbol.to_ascii()` — outputs ASCII art representation of graphs
- `symbol.delete()` — removes node and its inverse references (parents/children)
- `symbol.elevate()` — promotes metadata to instance attributes/methods
- `symbol.slim()` — removes unused dynamically applied mixins
- `symbol.immute()` — orchestrates maturing process (elevate, slim, freeze)
- `symbol.ref` — alias for `symbol.origin` to track source provenance

Performance:
------------
- O(1) symbol instantiation (intern pool)
- O(1) relationship linking
- O(1) traversal with cache and float-based cursor insertion
- O(log n) insert/search when extended to use bisect-based insertion order

Memory Awareness:
-----------------
- GC-aware deletion (respecting `ENABLE_ORIGIN`, `MEMORY_AWARE_DELETE`)
- Proactive memory management for `context` attribute via `deep_del`

Extensibility:
---------------
- Easily extended with async traversal, typed relations, or backend persistence
- `Symbolable` type for robust callable integration
- `MixinFunction` protocol for formal mixin interface
- `SymbolAdapter` mixinable interface enables different logical structures
- Compatible with enum reflection and external DSL inputs

Example Use:
------------
```python
from symbol import s, Symbol

# --- Basic Symbol creation and relationships ---
hello = Symbol('hello')
world = s.world
hello.add(world)
print(hello.tree())

# --- ESG Example: Tracking Deforestation in a Supply Chain ---
# Define our supply chain entities
s.Global_Goods_Inc.buys_from(s.Palm_Oil_Processor)
s.Palm_Oil_Processor.buys_from(s.Supplier_A)
s.Palm_Oil_Processor.buys_from(s.Supplier_B)

s.Supplier_A.sources_from(s.Plantation_X)
s.Supplier_B.sources_from(s.Plantation_Y)

# Add deforestation data (hypothetical)
s.Plantation_Y.add(s.deforestation_event_2024_Q4)

# Now, let's find the tainted products
def has_deforestation(symbol):
    return 'deforestation' in symbol.name

# Find all paths from the company to a deforestation event
for path in s.Global_Goods_Inc.match(has_deforestation):
    print(f"Deforestation Link Found: {path.path_to(s.deforestation_event_2024_Q4)}")

# --- Timeline Example ---
from symbol import tl
import datetime

timeline1 = tl.Timeline()
timeline1.add_period(datetime.datetime(2023, 1, 1), datetime.datetime(2023, 1, 15))
timeline1.add_period(datetime.datetime(2023, 1, 10), datetime.datetime(2023, 1, 20))

timeline2 = tl.Timeline()
timeline2.add_period(datetime.datetime(2023, 1, 5), datetime.datetime(2023, 1, 12))

overlap_timeline = timeline1.overlap(timeline2)
print(f"Overlap periods: {list(overlap_timeline)}")
print(timeline1.to_ascii())

# --- Batch Processing Example ---
from symbol import process_batch

def square(x): return x * x
results = process_batch([1, 2, 3, 4], square)
print(f"Batch processing results: {results}")

```

Conclusion:
-----------
This module provides a high-performance, semantically rich, thread-safe symbol abstraction to power DSLs, runtime graphs, knowledge trees, and dynamic semantic layers. The design emphasizes structural clarity, cache efficiency, and symbolic extensibility.

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
    D --> G[symbol.builtins.datetime]
    D --> H[symbol.builtins.collections]
    D --> I[symbol.builtins.index]
    D --> J[symbol.builtins.path]
    D --> K[symbol.builtins.visual]
    D --> L[symbol.builtins.timeline]
```

## Software Architecture

```mermaid
graph TD
    subgraph Symbol Package
        A[symbol] --> B(symbol.core)
        A --> C(symbol.builtins)
    end

    subgraph Core Modules
        B --> B1[symbol.core.symbol]
        B --> B2[symbol.core.graph]
        B --> B3[symbol.core.maturing]
        B --> B4[symbol.core.mixinability]
        B --> B5[symbol.core.mixin_validator]
        B --> B6[symbol.core.protocols]
        B --> B7[symbol.core.symbolable]
        B --> B8[symbol.core.time_arithmetics]
    end

    subgraph Builtin Extensions
        C --> C1[symbol.builtins.collections]
        C --> C2[symbol.builtins.datetime]
        C --> C3[symbol.builtins.index]
        C --> C4[symbol.builtins.path]
        C --> C5[symbol.builtins.visual]
        C --> C6[symbol.builtins.red_black_tree]
        C --> C7[symbol.builtins.avl_tree]
        C --> C8[symbol.builtins.timeline]
    end

    B1 -- uses --> B2
    B1 -- uses --> B3
    B1 -- uses --> B4
    B1 -- uses --> C1
    B1 -- uses --> C3

    B4 -- uses --> B5
    B4 -- uses --> B6
    B4 -- uses --> B7

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

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bfb,stroke:#333,stroke-width:2px
```

## Getting Started

To begin, simply import the `Symbol` or `s` namespace factory:

```python
from symbol import Symbol, s

# Create symbols
hello = Symbol('hello')
world = s.world

# Build relationships
hello.add(world)

# Traverse the graph
print(hello.tree())

```
