# Module Import Paths

This diagram illustrates the most direct import paths to each accessible module in the `symb` library. It provides a clear overview of the library's public API and how its various components can be accessed.

```mermaid
graph TD
    subgraph "Public API"
        A[symb] --> B(symb.s)
        A --> C(symb.Symbol)
        A --> D(symb.to_sym)
        A --> E(symb.SymbolNamespace)
    end

    subgraph "Core Modules"
        C --> F(symb.core.base_symb)
        C --> G(symb.core.symb)
        C --> I(symb.core.maturing)
        C --> J(symb.core.mixinability)
        C --> K(symb.core.mixin_validator)
        C --> L(symb.core.protocols)
        C --> M(symb.core.symbable)
        C --> N(symb.core.time_arithmetics)
        C --> O(symb.core.schedule)
        C --> P(symb.core.batch_processing)
    end

    subgraph "Builtin Extensions"
        C --> Q(symb.builtins.collections)
        C --> R(symb.builtins.time_dim)
        C --> S(symb.builtins.index)
        C --> T(symb.builtins.path)
        C --> U(symb.builtins.visual)
        C --> V(symb.builtins.red_black_tree)
        C --> W(symb.builtins.avl_tree)
        C --> X(symb.builtins.timeline)
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
