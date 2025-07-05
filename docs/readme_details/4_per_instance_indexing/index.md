# 1.4 Per-Instance Indexing: Sophisticated Data Structuring

The `Symbol` framework introduces the concept of **per-instance indexing**, where each `Symbol` object possesses its own private, weighted index of other symbols. This advanced feature enables the creation and efficient management of sophisticated, nested data structures, moving beyond simple parent-child relationships to allow for more complex, context-specific associations.

## The `SymbolIndex` Mechanism

At the heart of per-instance indexing is the `SymbolIndex` class, located in `symbol/builtins/index.py`. Each `Symbol` instance is initialized with its own `SymbolIndex` object &#40;as seen in `symbol/core/symbol.py` within the `__new__` method&#41;. This `SymbolIndex` acts as a localized, internal data store for the `Symbol`, allowing it to maintain a structured collection of references to other `Symbol` instances, potentially with associated weights or metadata.

```mermaid
graph TD
    A[Symbol Instance] --> B{SymbolIndex &#40;Private&#41;};
    B --> C[IndexNode 1];
    B --> D[IndexNode 2];
    B --> E[...];
    C -- "references" --> F[Other Symbol];
    D -- "references" --> G[Another Symbol];

    style A fill:#10cc31,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:#10cc31,stroke:#333,stroke-width:2px,color:#000000;```

## Key Features and Benefits

-   **Private Context**: Each `Symbol` can maintain its own unique view or organization of related symbols, independent of global relationships. This is crucial for modeling complex domains where relationships are highly contextual.
-   **Weighted Associations**: The ability to assign weights to indexed symbols allows for the representation of strength, relevance, or priority in relationships. This facilitates advanced algorithms for ranking, recommendation, or decision-making.
-   **Sophisticated Traversal and Querying**: With a dedicated index, a `Symbol` can perform highly optimized local traversals and queries on its directly associated symbols, without needing to traverse the entire global graph.
-   **Nested Data Structures**: This feature enables the construction of hierarchical or nested data structures where a `Symbol` can encapsulate a complex internal organization of other symbols.

### Code Example: Product Configuration with Weighted Features

Imagine a product configurator where a `Product` symbol needs to index its `Features` with associated `weights` &#40;e.g., importance, cost impact&#41;.

```python
from symbol import Symbol
from symbol.builtins.index import SymbolIndex

# Create product and feature symbols
product_laptop = s.Laptop
feature_ssd = s.SSD
feature_ram = s.RAM
feature_gpu = s.GPU

# Initialize SymbolIndex for the product &#40;this happens automatically in Symbol.__new__&#41;
# product_laptop.index = SymbolIndex(product_laptop) # Conceptual, already done

# Insert features into the product's private index with weights
product_laptop.index.insert(feature_ssd, weight=0.8) # High importance
product_laptop.index.insert(feature_ram, weight=0.6) # Medium importance
product_laptop.index.insert(feature_gpu, weight=0.9) # Very high importance

# Traverse the product's index &#40;e.g., by weight&#41;
print("Laptop features by importance:")
for feature_sym in product_laptop.index.traverse(order="in"):
    print(f"- {feature_sym.name} &#40;Weight: {product_laptop.index._function_map[feature_sym.name].eval_weight()}&#41;")

# Rebalance the index based on weight &#40;conceptual, SymbolIndex supports this&#41;
# product_laptop.index.rebalance(strategy='weight')
```

### Industry Applications

**High-Tech: Recommendation Systems**
```python
from symbol import s
from symbol.builtins.index import SymbolIndex

# User and Product symbols
user_alice = s.Alice
product_book = s.Book_A
product_movie = s.Movie_B

# User's private index of liked products with preference scores
user_alice.index.insert(product_book, weight=0.9)
user_alice.index.insert(product_movie, weight=0.7)

print(f"Alice's liked items: {[item.name for item in user_alice.index.traverse()]}")
```

**Low-Tech: Library Cataloging and Cross-Referencing**
```python
from symbol import s
from symbol.builtins.index import SymbolIndex

# Book and Keyword symbols
book_history = s.History_of_Time
keyword_physics = s.Physics
keyword_cosmology = s.Cosmology

# Book's private index of keywords with relevance
book_history.index.insert(keyword_physics, weight=0.8)
book_history.index.insert(keyword_cosmology, weight=0.95)

print(f"Keywords for 'History of Time': {[kw.name for kw in book_history.index.traverse()]}")
```

## Conclusion

Per-instance indexing significantly enhances the expressive power of the `Symbol` framework. By providing each `Symbol` with its own localized, weighted index, it facilitates the modeling of intricate, contextual relationships and the construction of sophisticated, nested data structures. This capability is paramount for applications requiring fine-grained control over symbolic associations and efficient, localized data retrieval.
