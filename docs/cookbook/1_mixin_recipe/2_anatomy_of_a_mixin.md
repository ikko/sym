# [`«symb»`](https://github.com/ikko/symb) cookbook
**Recipes for Symbolic Mastery**

_Recipe 1: How to Create a Mixin?_

---

# 1.2 Anatomy of a Mixin: Structure and Protocols

Understanding the internal structure and expected protocols of a mixin is crucial for developing robust and well-integrated extensions within the `symb` framework. A mixin, at its core, is a Python class designed to be composed with `Symbol` objects, providing additional behaviors or attributes.

## Core Components of a Mixin

While mixins can vary in complexity, they generally adhere to a common structure:

1.  **Initialization (`__init__`)**: A mixin's `__init__` method typically takes the `Symbol` instance it is being mixed into as its primary argument. This allows the mixin to establish a reference to the `Symbol` object and perform any necessary setup or state initialization related to that specific `Symbol`.

    ```python
    class MyMixin:
        def __init__(self, symb_instance: Symbol):
            self.symb = symb_instance
            # Initialize mixin-specific state
    ```

2.  **Methods**: These are the functionalities that the mixin contributes to the `Symbol` object. Methods can be synchronous or asynchronous, following the `a_` prefix convention for asynchronous operations.

    ```python
    class MyMixin:
        # ...
        def sync_operation(self, data):
            # Synchronous logic
            return f"Processed {data} synchronously for {self.symb.name}"

        async def a_async_operation(self, data):
            # Asynchronous logic
            await anyio.sleep(0.01) # Simulate async work
            return f"Processed {data} asynchronously for {self.symb.name}"
    ```

3.  **Properties (Optional)**: Mixins can also expose properties that provide computed attributes or controlled access to internal state.

    ```python
    class MyMixin:
        # ...
        @property
        def mixin_status(self):
            # Return some status based on mixin's state
            return "Active"
    ```

## Protocols and Type Hinting

To ensure type safety and facilitate better code analysis, `symb` mixins often leverage Python's `typing.Protocol`. Protocols define the expected interface of a mixin, specifying the methods and attributes it *should* implement. This allows for static type checking and provides clear documentation of a mixin's capabilities without enforcing a rigid inheritance hierarchy.

For example, the `SymbolVisualProtocol` in `symb.core.protocols` defines the interface for mixins that provide visualization capabilities:

```python
from typing import Protocol, Literal, runtime_checkable

@runtime_checkable
class SymbolVisualProtocol(Protocol):
    def to_dot(self, mode: Literal["tree", "graph"]) -> str:
        ...

    async def a_to_svg(self, mode: Literal["tree", "graph"]) -> str:
        ...

    def to_svg(self, mode: Literal["tree", "graph"]) -> str:
        ...

    async def a_to_png(self, mode: Literal["tree", "graph"]) -> bytes:
        ...

    def to_png(self, mode: Literal["tree", "graph"]) -> bytes:
        ...

    def to_mmd(self, mode: Literal["tree", "graph"]) -> str:
        ...

    def to_ascii(self, mode: Literal["tree", "graph"]) -> str:
        ...
```

When implementing a mixin, it's highly recommended to declare that it adheres to a relevant protocol (if one exists) using `@runtime_checkable` and inheriting from `Protocol`. This provides a clear contract for how the mixin interacts with the `Symbol` framework and other components.

## Mixin Validation

The `symb` framework includes mechanisms to validate mixins, ensuring they conform to expected structures and behaviors. This validation process helps catch common errors early in development and ensures the stability of the system when new mixins are introduced. The `MixinValidationResult` and `validate_mixin_callable` (from `symb.core.mixin_validator`) are used internally to ensure mixins are correctly structured and their methods are callable.

By understanding these core components and adhering to established protocols, developers can create powerful, maintainable, and well-integrated mixins for the `symb` framework.
