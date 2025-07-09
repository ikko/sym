# Module Import Paths

This diagram illustrates the most direct import paths to each accessible module in the `sym` library. It provides a clear overview of the library's public API and how its various components can be accessed.

```mermaid
graph TD
    subgraph "Public API"
        A[sym] --> B(sym.s)
        A --> C(sym.Symbol)
        A --> D(sym.to_sym)
        A --> E(sym.SymbolNamespace)
    end

    subgraph "Core Modules"
        C --> F(sym.core.base_sym)
        C --> G(sym.core.sym)
        C --> I(sym.core.maturing)
        C --> J(sym.core.mixinability)
        C --> K(sym.core.mixin_validator)
        C --> L(sym.core.protocols)
        C --> M(sym.core.symable)
        C --> N(sym.core.time_arithmetics)
        C --> O(sym.core.schedule)
        C --> P(sym.core.batch_processing)
    end

    subgraph "Builtin Extensions"
        C --> Q(sym.builtins.collections)
        C --> R(sym.builtins.time_dim)
        C --> S(sym.builtins.index)
        C --> T(sym.builtins.path)
        C --> U(sym.builtins.visual)
        C --> V(sym.builtins.red_black_tree)
        C --> W(sym.builtins.avl_tree)
        C --> X(sym.builtins.timeline)
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
