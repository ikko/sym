# 1.3 Layered Architecture: Modularity and Extensibility

The `Symbol` framework is designed with a **layered architecture**, a fundamental principle that separates concerns into distinct, hierarchical layers. This approach ensures a lean and stable core while allowing for flexible and modular extension of functionalities. The primary distinction is between the `symb.core` package, which houses the essential building blocks, and the `symb.builtins` package, which provides optional, high-level extensions.

## Core Layer (`symb.core`)

This layer represents the foundational elements of the `Symbol` framework. It contains the absolute minimum necessary for a `Symbol` object to exist and to participate in graph structures. Key characteristics include:

-   **Minimalism**: Focuses solely on the fundamental definition of a `Symbol`, its unique identification (interning), and the basic mechanisms for establishing and managing relationships (parents, children).
-   **Stability**: Designed to be highly stable and rarely change, providing a robust base for all other functionalities.
-   **Independence**: Ideally, this layer has minimal dependencies on higher-level components, ensuring its integrity and reusability.

```mermaid
graph TD
    A[symb.core] --> B[base_symb.py];
    A --> C[symb.py];
    A --> D[maturing.py];
    A --> E[mixinability.py];

    style A fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style B fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style D fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style E fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
```
## Builtin Extensions Layer (`symb.builtins`)

This layer comprises a collection of modular extensions that provide specialized functionalities to `Symbol` objects. These extensions are designed to be plug-and-play, allowing developers to include only the features relevant to their specific application without bloating the core.

-   **Modularity**: Each module within `symb.builtins` addresses a specific domain (e.g., date/time, collections, visualization).
-   **Extensibility**: New functionalities can be easily added by creating new modules in this layer, adhering to the framework's extension protocols.
-   **Controlled Dependencies**: While `symb.builtins` modules depend on `symb.core`, the `symb.core` generally remains independent of `symb.builtins`, maintaining the hierarchical integrity.

```mermaid
graph TD
    A[symb.builtins] --> B[collections.py];
    A --> C[time_dim.py];
    A --> D[index.py];
    A --> E[path.py];
    A --> F[visual.py];
    A --> G[timeline.py];

    style A fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style B fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style C fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style D fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style E fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style F fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style G fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
```
## Inter-Layer Communication

The `symb.core` package, particularly `symb.py`, integrates with selected `symb.builtins` modules to enhance its fundamental capabilities. For instance, `SymbolIndex` from `symb.builtins.index` is used within the `Symbol` class to manage per-instance indexing. This controlled dependency allows the core to leverage specialized, well-encapsulated functionalities without compromising its lean design.

### Code Example: Core Leveraging Builtins

```python
# From symb/core/symb.py
from ..builtins.collections import OrderedSymbolSet
from ..builtins.index import SymbolIndex

class Symbol(BaseSymbol):
    def __new__(cls, name: str, origin: Optional[Any] = None):
        obj = super().__new__(cls, name, origin)
        if not hasattr(obj, 'index'):
            obj.index = SymbolIndex(obj) # Core uses a builtin for indexing
            obj.metadata = DefDict()
            obj.context = DefDict()
        # ... rest of __new__
```

### Industry Applications

**High-Tech: Microservices Architecture**
```python
from symb import s

# Core services
s.AuthService.provides(s.UserAuthentication)
s.DataStorageService.provides(s.DataPersistence)

# Specialized services (builtins)
s.PaymentProcessingService.uses(s.AuthService)
s.RecommendationEngine.uses(s.DataStorageService)

print(f"Payment service uses: {[c.name for c in s.PaymentProcessingService.children]}")
```
<details>
<summary>Outcome</summary>

```text
Payment service uses: []
```
</details>

**Low-Tech: Modular Furniture Design**
```python
from symb import s

# Core components
s.BasicFrame.connects_with(s.StandardConnector)

# Add-on modules (builtins)
s.ShelfModule.attaches_to(s.BasicFrame)
s.DrawerModule.attaches_to(s.BasicFrame)

print(f"Basic frame connections: {[c.name for c in s.BasicFrame.children]}")
```
<details>
<summary>Outcome</summary>

```text
Basic frame connections: []
```
</details>

## Conclusion

The layered architecture of the `Symbol` framework is a testament to its robust and scalable design. By clearly separating core functionalities from modular extensions, it achieves a balance between minimalism and extensibility, making it adaptable to a wide array of complex symbic data manipulation tasks while maintaining a clean and maintainable codebase.
