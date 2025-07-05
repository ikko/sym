# Module Import Paths

This diagram illustrates the most direct import paths to each accessible module in the `symbol` library. It provides a clear overview of the library's public API and how its various components can be accessed.

```mermaid
graph TD
    subgraph "Public API"
        A[symbol] --> B#40symbol.s#41
        A --> C#40symbol.Symbol#41
        A --> D#40symbol.to_sym#41
        A --> E#40symbol.SymbolNamespace#41
    end

    subgraph "Core Modules"
        C --> F#40symbol.core.base_symbol#41
        C --> G#40symbol.core.symbol#41
        C --> H#40symbol.core.graph#41
        C --> I#40symbol.core.maturing#41
        C --> J#40symbol.core.mixinability#41
        C --> K#40symbol.core.mixin_validator#41
        C --> L#40symbol.core.protocols#41
        C --> M#40symbol.core.symbolable#41
        C --> N#40symbol.core.time_arithmetics#41
        C --> O#40symbol.core.schedule#41
        C --> P#40symbol.core.batch_processing#41
    end

    subgraph "Builtin Extensions"
        C --> Q#40symbol.builtins.collections#41
        C --> R#40symbol.builtins.time_dim#41
        C --> S#40symbol.builtins.index#41
        C --> T#40symbol.builtins.path#41
        C --> U#40symbol.builtins.visual#41
        C --> V#40symbol.builtins.red_black_tree#41
        C --> W#40symbol.builtins.avl_tree#41
        C --> X#40symbol.builtins.timeline#41
    end

    style A fill:#97bff2,stroke:#333,stroke-width:2px,color:#000000;```
