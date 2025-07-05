# Symbol Architecture

## Introduction

The `symbol` library is a Python framework for creating, manipulating, and reasoning about symbolic data structures. It is designed to be lightweight, extensible, and memory-aware, providing a powerful foundation for a wide range of applications, from data modeling and graph analysis to scheduling and metaprogramming.

At its core, the `symbol` library is built upon a layered architecture that separates the fundamental `Symbol` class from its extended functionalities. This design promotes modularity, reduces complexity, and allows for a high degree of customization through mixins and builtin extensions.

This document provides a detailed overview of the `symbol` library's architecture, including its core components, builtin extensions, and the principles that guide its design.

## Core Architecture

The core architecture of the `symbol` library is divided into two main layers: the **Core Layer** and the **Builtin Extensions Layer**.

```mermaid
graph TD
    subgraph "Symbol Package"
        A[symbol] --> B&#40;symbol.core&#41;
        A --> C&#40;symbol.builtins&#41;
    end

    subgraph "Core Layer &#40;symbol.core&#41;"
        B --> B1[symbol.core.base_symbol]
        B --> B2[symbol.core.symbol]
        B --> B3[symbol.core.graph]
        B --> B4[symbol.core.maturing]
        B --> B5[symbol.core.mixinability]
        B --> B6[symbol.core.mixin_validator]
        B --> B7[symbol.core.protocols]
        B --> B8[symbol.core.symbolable]
        B --> B9[symbol.core.time_arithmetics]
        B --> B10[symbol.core.schedule]
        B --> B11[symbol.core.batch_processing]
    end

    subgraph "Builtin Extensions Layer &#40;symbol.builtins&#41;"
        C --> C1[symbol.builtins.collections]
        C --> C2[symbol.builtins.time_dim]
        C --> C3[symbol.builtins.index]
        C --> C4[symbol.builtins.path]
        C --> C5[symbol.builtins.visual]
        C --> C6[symbol.builtins.red_black_tree]
        C --> C7[symbol.builtins.avl_tree]
        C --> C8[symbol.builtins.timeline]
    end

    B2 -- uses --> B1
    B2 -- uses --> B3
    B2 -- uses --> B4
    B2 -- uses --> B5
    B2 -- uses --> C1
    B2 -- uses --> C3

    B5 -- uses --> B6
    B5 -- uses --> B7
    B5 -- uses --> B8
    
    B10 -- uses --> B2

    C2 -- uses --> B2
    C3 -- uses --> B2
    C4 -- uses --> B2
    C5 -- uses --> B2
    C6 -- uses --> B2
    C7 -- uses --> B2
    C8 -- uses --> B2

    C3 -- uses --> C6
    C3 -- uses --> C7

    C5 -- uses --> B9
    C8 -- uses --> B9

    style A fill:#97bff2,stroke:#333,stroke-width:2px,color:#000000;
```

### Legend

*   **Blue Boxes**: Core architectural components.
*   **Green Boxes**: Builtin extension modules.
*   **Light Blue Boxes**: Modules within the `symbol.core` layer.
*   **Light Green Boxes**: Modules within the `symbol.builtins` layer.
*   **Arrows**: Indicate dependencies between modules.

### Core Layer (`symbol.core`)

The Core Layer provides the fundamental building blocks of the `symbol` library. It includes the `Symbol` class itself, along with essential services for graph traversal, mixin-based extensibility, and memory management.

*   **`base_symbol`**: Defines the foundational `Symbol` class and its core instantiation logic, preventing circular import dependencies.
*   **`symbol`**: Extends the `base_symbol` with advanced features such as graph traversal, indexing, maturing, and serialization.
*   **`graph`**: Provides graph traversal capabilities for `Symbol` objects.
*   **`maturing`**: Implements the "maturing" process for `Symbol` objects, which involves elevating metadata to first-class attributes and methods.
*   **`mixinability`**: Provides the core functionality for mixin-based extensibility of the `Symbol` class.
*   **`mixin_validator`**: A validator for `Symbol` mixins, using static analysis to ensure adherence to the expected interface.
*   **`protocols`**: Defines the protocols that govern the behavior of `Symbol` objects.
*   **`symbolable`**: Defines the `Symbolable` protocol, used to identify objects that can be integrated into a `Symbol` instance.
*   **`time_arithmetics`**: Provides functions for performing arithmetic operations on time-related objects.
*   **`schedule`**: Provides the core scheduling logic for the `symbol` project.
*   **`batch_processing`**: Provides functions for processing batches of items asynchronously and synchronously.

### Builtin Extensions Layer (`symbol.builtins`)

The Builtin Extensions Layer provides a collection of optional modules that extend the functionality of the `Symbol` class. These modules are designed to be self-contained and can be used independently of one another.

*   **`collections`**: Provides custom collection classes for `Symbol` objects, such as `OrderedSymbolSet`.
*   **`time_dim`**: Provides time dimension-related functionality for `Symbol` objects.
*   **`index`**: Provides index capabilities for `Symbol` objects.
*   **`path`**: Provides pathfinding capabilities for `Symbol` objects.
*   **`visual`**: Provides visualization capabilities for `Symbol` objects.
*   **`red_black_tree`**: An implementation of a red-black tree.
*   **`avl_tree`**: An implementation of an AVL tree.
*   **`timeline`**: Provides a `Timeline` class for representing a series of time periods.
