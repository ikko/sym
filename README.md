# symbol namespace dsl

> symbol.py — A Lazy, Graph-Oriented, Immutable Symbol System for Domain-Specific Abstraction

_inspired by ruby's [symbol](https://ruby-doc.org/core-2.5.3/Symbol.html)_


Overview:
---------
This module implements a symbol abstraction designed to serve as a foundational primitive for symbolic computation, DSL construction, type-safe identifiers, graph traversal, and dynamic metadata annotation. The `Symbol` construct abstracts named identity with deterministic interning, structural relationships, and memory-aware lifecycle management.

Target Audience:
----------------
Researchers and engineers working with DSLs, compilers, runtime graphs, knowledge representation, and structured symbolic computation. Especially relevant for those familiar with LISP, Elixir, Scala-like symbolic or type-level metaprogramming.

Motivations:
------------
- Express symbolic identities without string duplication (via global interning)
- Encode graph or tree structures among identifiers (que/tree/relate adapters)
- Maintain structural order and traversal semantics (prev/next, parent/child)
- Enable lazy evaluation and efficient cache-aware operations (O(1) reads)
- Allow origin tracking and selective memory cleanup (GC-awareness)
- Serve as the core building block in a future semantic engine or DSL system

Core Components:
----------------
- `Symbol`: Immutable, globally interned identifiers supporting relationship metadata.
- `OrderedSymbolSet`: Cache-aware, ordered deduplicating set.
- `SymbolAdapter`: Extensible traversal interface (que, tree, relate).
- `GraphTraversal`: Lazy, cycle-aware traversal engine.
- `SymbolNamespace`: Dot-accessor for ergonomic DSL usage (e.g. `S.user`, `S.login`).

Symbol Relationships:
----------------------
1. `que` — Ordered sequential graph via `next` / `prev` pointers.
2. `tree` — Hierarchical DAG via `parent` / `child` links.
3. `relate` — Polymorphic cross-linking via `related_to` / `related_how` pairs.

API Highlights:
---------------
- `Symbol(name: str)` — globally interned, idempotent constructor
- `Symbol.next()` — creates and chains auto-numbered symbol (`sym_0`, `sym_1`, …)
- `symbol.append(child)` / `symbol.relate_to(other, how)` — link construction
- `symbol.tree()` / `.que()` / `.relate()` — lazy traversal
- `symbol.patch(other)` — recursive, structural deep merge (PATCH-like semantics)
- `symbol.to_mmd()` — outputs tree graph in Mermaid diagram syntax
- `symbol.delete()` — removes node and its inverse references (parents/children)

Performance:
------------
- O(1) symbol instantiation (intern pool)
- O(1) relationship linking
- O(1) traversal with cache and float-based cursor insertion
- O(log n) insert/search when extended to use bisect-based insertion order

Memory Awareness:
-----------------
- GC-compatible deletion with optional `origin` retention
- `ENABLE_ORIGIN` and `MEMORY_AWARE_DELETE` flags allow granular control
- Optional `Symbol.origin` to track source provenance

Extensibility:
--------------
- Easily extended with async traversal, typed relations, or backend persistence
- `SymbolAdapter` pluggable interface enables different logical structures
- Compatible with enum reflection and external DSL inputs

Example Use:
------------
```python
S = SymbolNamespace()

S.backend.relate_to(S.database, how=S.uses)
S.page.append(S.header).append(S.footer)

print(S.page.tree())  # Traverse children
print(S.page.to_mmd())  # Render as Mermaid diagram
```

Conclusion:
-----------
This module provides a high-performance, semantically rich, thread-safe symbol abstraction to power DSLs, runtime graphs, knowledge trees, and dynamic semantic layers. The design emphasizes structural clarity, cache efficiency, and symbolic extensibility.
"""
