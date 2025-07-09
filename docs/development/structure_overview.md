## Project Structure

The project is organized into two main packages:

-   `symb.core`: Contains the essential `Symbol` class and graph traversal logic.
-   `symb.builtins`: Provides optional, high-level extensions for collections, date/time operations, index, pathfinding, and visualization.

```mermaid
graph LR
    A[User Application] --> B(symb)
    B --> C{symb.core}
    B --> D{symb.builtins}
    C --> E[symb.core.symb]
    C --> F[symb.core.graph]
    C --> G[symb.core.schedule]
    D --> H[symb.builtins.time_dim]
    D --> I[symb.builtins.collections]
    D --> J[symb.builtins.index]
    D --> K[symb.builtins.path]
    D --> L[symb.builtins.visual]
    D --> M[symb.builtins.timeline]
    
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
graph LR
    subgraph "Symbol Package"
        A[symb] --> B(symb.core)
        A --> C(symb.builtins)
    end
    style A fill:#228B22,stroke:#333,stroke-width:2px,color:#FFFFFF;

    subgraph "Core Modules"
        B --> B1[symb.core.symb]
        B --> B3[symb.core.maturing]
        B --> B4[symb.core.mixinability]
        B --> B5[symb.core.mixin_validator]
        B --> B6[symb.core.protocols]
        B --> B7[symb.core.symbable]
        B --> B8[symb.core.time_arithmetics]
        B --> B9[symb.core.schedule]
    end
    style B fill:#FF8C00,stroke:#333,stroke-width:2px,color:#000000;

    subgraph "Builtin Extensions"
        C --> C1[symb.builtins.collections]
        C --> C2[symb.builtins.time_dim]
        C --> C3[symb.builtins.index]
        C --> C4[symb.builtins.path]
        C --> C5[symb.builtins.visual]
        C --> C6[symb.builtins.red_black_tree]
        C --> C7[symb.builtins.avl_tree]
        C --> C8[symb.builtins.timeline]
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
