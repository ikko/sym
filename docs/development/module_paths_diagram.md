# Module Import Paths

This diagram illustrates the most direct import paths to each accessible module in the `symbol` library. It provides a clear overview of the library's public API and how its various components can be accessed.

```mermaid
graph TD
    subgraph "Public API"
        A[symbol] --> B(symbol.s)
        A --> C(symbol.Symbol)
        A --> D(symbol.to_sym)
        A --> E(symbol.SymbolNamespace)
    end

    subgraph "Core Modules"
        C --> F(symbol.core.base_symbol)
        C --> G(symbol.core.symbol)
        C --> I(symbol.core.maturing)
        C --> J(symbol.core.mixinability)
        C --> K(symbol.core.mixin_validator)
        C --> L(symbol.core.protocols)
        C --> M(symbol.core.symbolable)
        C --> N(symbol.core.time_arithmetics)
        C --> O(symbol.core.schedule)
        C --> P(symbol.core.batch_processing)
    end

    subgraph "Builtin Extensions"
        C --> Q(symbol.builtins.collections)
        C --> R(symbol.builtins.time_dim)
        C --> S(symbol.builtins.index)
        C --> T(symbol.builtins.path)
        C --> U(symbol.builtins.visual)
        C --> V(symbol.builtins.red_black_tree)
        C --> W(symbol.builtins.avl_tree)
        C --> X(symbol.builtins.timeline)
    end

    style A fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style B fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style C fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style D fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style E fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;

    style F fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style G fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style I fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style J fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style K fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style L fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style M fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style N fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style O fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style P fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;

    style Q fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style R fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style S fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style T fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style U fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style V fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style W fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style X fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;