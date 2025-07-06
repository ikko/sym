# API Highlights: Core Functionality of the Symbol Framework

The `Symbol` framework provides a concise yet powerful API for manipulating symbolic data. This section details the key methods and properties that form the backbone of its functionality, offering insights into their design principles and practical applications.

## `Symbol(name: str)`: Globally Interned, Idempotent Constructor

The `Symbol` constructor serves as the fundamental entry point for creating symbolic entities within the framework. Its design adheres to the **Flyweight pattern**, ensuring that for any given `name` string, only a single `Symbol` object instance exists in memory. This global interning mechanism guarantees object identity and optimizes memory utilization, particularly in scenarios involving a large number of recurring symbolic representations. The constructor is idempotent, meaning repeated calls with the same `name` will consistently return the identical `Symbol` instance, thereby maintaining referential integrity across the system.

### Purpose and Usage
This method is used to create or retrieve a unique `Symbol` instance based on its string `name`. It's the primary way to introduce new symbolic entities into the graph.

### Code Example
```python
from symbol import Symbol, s

s1 = s.my_unique_symbol
s2 = s.my_unique_symbol
s3 = s.another_symbol

print(f"s1 is s2: {s1 is s2}")
print(f"s1 is s3: {s1 is s3}")
```

### Diagram
```mermaid
graph TD
    A[Call Symbol&#40'Name'&#41] --> B{Symbol Pool Check};
    B -- "Exists?" --> C{Yes};
    C --> D[Return Existing Instance];
    B -- "No" --> E[Create New Instance];
    E --> F[Add to Pool];
    F --> D;

    style A fill:lighten&#40&#41c855, 30%&#41,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:&#41c855,stroke:#333,stroke-width:2px,color:#000000;
```
## `Symbol.next()`: Creates and Chains Auto-Numbered Symbols

The `Symbol.next()` class method provides a convenient mechanism for generating a sequence of automatically numbered `Symbol` instances. This functionality is particularly useful for creating transient or placeholder symbols, or for scenarios where unique identifiers are required without the need for explicit naming. The method also implicitly establishes a linked-list-like chain between consecutively generated symbols, facilitating sequential traversal.

### Purpose and Usage
To generate a new `Symbol` with an auto-incrementing name (e.g., `sym_0`, `sym_1`, `sym_2`, ...). It's ideal for quick prototyping or when the specific name of a symbol is not semantically important.

### Code Example
```python
from symbol import Symbol

# Generate auto-numbered symbols
sym0 = Symbol.next()
sym1 = Symbol.next()
sym2 = Symbol.next()

print(f"Generated symbols: {sym0.name}, {sym1.name}, {sym2.name}")
print(f"sym0 next is sym1: {sym0._next is sym1}")
print(f"sym1 prev is sym0: {sym1._prev is sym0}")
```

### Diagram
```mermaid
graph TD
    A[Call Symbol.next&#40&#41] --> B{Increment Counter};
    B --> C[Generate Name &#40e.g., sym_N&#41];
    C --> D[Create New Symbol];
    D -- "Link to Previous &#40if any&#41" --> E[Previous Symbol];
    D --> F[Return New Symbol];

    style A fill:lighten&#40#26c4c6, 30%&#41,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:#26c4c6,stroke:#333,stroke-width:2px,color:#000000;
```
## `symbol.append(child)` / `symbol.relate_to(other, how)`: Link Construction

The `Symbol` framework provides intuitive methods for establishing relationships between symbolic entities, forming the edges of the underlying directed acyclic graph (DAG). `append(child)` creates a direct parent-child relationship, while `relate_to(other, how)` offers a more semantically rich way to define arbitrary connections, allowing for the specification of the nature of the relationship.

### Purpose and Usage
These methods are used to build the graph structure by defining directed relationships between `Symbol` instances. `append` is for simple hierarchical relationships, while `relate_to` allows for custom relationship types.

### Code Example
```python
from symbol import s

parent = s.Parent
child1 = s.Child1
child2 = s.Child2
related_entity = s.RelatedEntity

parent.append(child1)
parent.append(child2)
parent.relate_to(related_entity, how='depends_on')

print(f"Parent children: {[c.name for c in parent.children]}")
print(f"Child1 parents: {[p.name for p in child1.parents]}")
```

### Diagram
```mermaid
graph TD
    A[Source Symbol] --> B{append&#40Child&#41};
    B --> C[Child Symbol];
    A -- "parent-child" --> C;

    X[Source Symbol] --> Y{relate_to&#40Other, 'how'&#41};
    Y --> Z[Other Symbol];
    X -- "how" --> Z;

    style A fill:#c57f86,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:#c57f86,stroke:#333,stroke-width:2px,color:#000000;
    style X fill:#c57f86,stroke:#333,stroke-width:2px,color:#000000;
```
## `symbol.tree()` / `.que()` / `.relate()`: Lazy Traversal

The `Symbol` framework provides a suite of methods for traversing the underlying graph structure, designed with efficiency and flexibility in mind. `tree()` performs a depth-first traversal, `que()` (likely `queue` or `deque` based) performs a breadth-first traversal, and `relate()` (not explicitly shown in `symbol.py` but implied by `related_to` attribute) would allow traversal based on custom relationships. The "lazy" aspect implies that these traversals might not materialize the entire graph in memory at once, but rather yield elements as they are visited, which is crucial for large graphs.

### Purpose and Usage
These methods are used to navigate the graph of `Symbol` instances. `tree()` is suitable for hierarchical views, `que()` for level-by-level processing, and `relate()` for exploring specific types of connections.

### Code Example
```python
from symbol import Symbol

# Build a sample graph
root = Symbol('Root')
level1_a = Symbol('Level1_A')
level1_b = Symbol('Level1_B')
level2_a1 = Symbol('Level2_A1')
level2_a2 = Symbol('Level2_A2')

root.append(level1_a)
root.append(level1_b)
level1_a.append(level2_a1)
level1_a.append(level2_a2)

# Tree traversal (Depth-First)
print("Tree Traversal:")
for sym in root.tree():
    print(sym.name)

# Queue traversal (Breadth-First) - assuming 'que' is implemented as BFS
# Note: 'que' is not directly implemented in the provided symbol.py,
# but a BFS traversal can be built using the children attribute.
# For demonstration, we'll simulate a BFS.
print("\nQueue Traversal (Simulated BFS):")
from collections import deque
q = deque([root])
visited = set()
while q:
    current_sym = q.popleft()
    if current_sym not in visited:
        visited.add(current_sym)
        print(current_sym.name)
        for child in current_sym.children:
            q.append(child)
```

### Diagram
```mermaid
graph TD
    A[Root Symbol] --> B{Traversal Method};
    B -- "tree&#40&#41" --> C[Depth-First Traversal];
    B -- "que&#40&#41" --> D[Breadth-First Traversal];
    B -- "relate&#40&#41" --> E[Custom Relationship Traversal];
    C --> F[Yields Symbols];
    D --> F;
    E --> F;

    style A fill:#1c06ab,stroke:#333,stroke-width:2px,color:#FFFFFF;

    style A fill:#1c06ab,stroke:#333,stroke-width:2px,color:#FFFFFF;
```
## `symbol.patch(other)`: Recursive, Structural Deep Merge

The `patch()` method provides a powerful mechanism for merging the structural and relational aspects of two `Symbol` instances. Unlike a simple overwrite, `patch()` performs a recursive, structural deep merge, intelligently combining the children, parents, and related entities of the `other` symbol into the current symbol. This operation is crucial for scenarios involving data synchronization, version control, or the aggregation of information from disparate sources within a graph.

### Purpose and Usage
To combine the graph structure of another `Symbol` into the current `Symbol` without losing existing relationships. It's particularly useful for updating a `Symbol` with new information or merging branches in a graph.

### Code Example
```python
from symbol import Symbol

# Create base symbol
base = Symbol('Base')
base.append(Symbol('CommonChild'))
base.append(Symbol('BaseSpecificChild'))

# Create another symbol with overlapping and new children
update = Symbol('Update')
update.append(Symbol('CommonChild')) # Overlapping child
update.append(Symbol('UpdateSpecificChild'))

print("Before patch:")
print(f"Base children: {[c.name for c in base.children]}")

# Patch the base symbol with the update symbol
base.patch(update)

print("\nAfter patch:")
print(f"Base children: {[c.name for c in base.children]}")
```

### Diagram
```mermaid
graph TD
    A[Current Symbol] --> B{patch&#40Other Symbol&#41};
    B -- "Merges" --> C[Other Symbol's Children];
    B -- "Merges" --> D[Other Symbol's Parents];
    B -- "Merges" --> E[Other Symbol's Related Entities];
    C --> F[Updated Current Symbol];
    D --> F;
    E --> F;

    style A fill:#681388,stroke:#333,stroke-width:2px,color:#FFFFFF;

    style A fill:#681388,stroke:#333,stroke-width:2px,color:#FFFFFF;
```
## `symbol.to_mmd()`: Outputs Tree Graph in Mermaid Diagram Syntax

The `to_mmd()` method provides a direct utility for visualizing the hierarchical structure of a `Symbol` and its descendants in the widely adopted Mermaid diagram syntax. This capability is invaluable for documentation, debugging, and communicating complex graph structures in a human-readable and easily renderable format. It transforms the internal graph representation into a textual description that can be rendered by Mermaid-compatible tools.

### Purpose and Usage
To generate a Mermaid graph definition string representing the `Symbol`'s tree structure. This string can then be embedded in Markdown documents or used with Mermaid rendering tools.

### Code Example
```python
from symbol import Symbol

# Build a sample graph
root = Symbol('Project')
task1 = Symbol('Task1')
task2 = Symbol('Task2')
subtask1_1 = Symbol('Subtask1_1')

root.append(task1)
root.append(task2)
task1.append(subtask1_1)

# Generate Mermaid syntax
mermaid_syntax = root.to_mmd()
print(mermaid_syntax)

# Expected output (or similar):
# graph TD
#     Project --> Task1
#     Project --> Task2
#     Task1 --> Subtask1_1
```


### Diagram
```mermaid
graph TD
    A[Symbol Instance] --> B{to_mmd&#40&#41};
    B --> C[Traverse Children];;
    C --> D[Generate Mermaid Syntax];
    D --> E[Return String];

    style A fill:#10cc31,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:#10cc31,stroke:#333,stroke-width:2px,color:#000000;
```
## `symbol.to_ascii()`: Outputs ASCII Art Representation of Graphs

Complementing `to_mmd()`, the `to_ascii()` method offers an alternative, text-based visualization of the `Symbol`'s graph structure. This is particularly useful for environments where graphical rendering is not available or desired, such as command-line interfaces, log files, or simple text-based reports. It provides a quick and accessible way to inspect the relationships between symbols.

### Purpose and Usage
To get a simple, text-based visual representation of the `Symbol`'s tree structure. Useful for quick debugging or console output.

### Code Example
```python
from symbol import Symbol

# Build a sample graph
root = Symbol('Root')
level1_a = Symbol('Level1_A')
level1_b = Symbol('Level1_B')
level2_a1 = Symbol('Level2_A1')

root.append(level1_a)
root.append(level1_b)
level1_a.append(level2_a1)

# Generate ASCII art
ascii_art = root.to_ascii()
print(ascii_art)

# Expected output (or similar):
# - Root
#   - Level1_A
#     - Level2_A1
#   - Level1_B
```

### Diagram
```mermaid
graph TD
    A[Symbol Instance] --> B{to_ascii&#40&#41};
    B --> C[Traverse Children];
    C --> D[Format as ASCII Art];
    D --> E[Return String];

    style A fill:#10cc31,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:#10cc31,stroke:#333,stroke-width:2px,color:#000000;
```
## `symbol.delete()`: Removes Node and Its Inverse References

The `delete()` method provides a mechanism for safely removing a `Symbol` instance from the graph. This operation is not merely a simple object deletion; it intelligently severs all incoming and outgoing relationships associated with the symbol. This includes removing the symbol from its parents' children lists and from its children's parents lists, ensuring graph consistency and preventing dangling references.

### Purpose and Usage
To completely remove a `Symbol` and all its connections from the graph. This is a critical operation for managing the lifecycle of symbolic entities and maintaining graph integrity.

### Code Example
```python
from symbol import Symbol

# Build a sample graph
parent = Symbol('Parent')
child = Symbol('Child')
grandchild = Symbol('Grandchild')

parent.append(child)
child.append(grandchild)

print(f"Before delete: Parent children: {[c.name for c in parent.children]}")
print(f"Before delete: Child parents: {[p.name for p in child.parents]}")

# Delete the child symbol
child.delete()

print(f"After delete: Parent children: {[c.name for c in parent.children]}")
print(f"After delete: Child parents: {[p.name for p in child.parents]}")
# Note: grandchild's parents will still contain 'Child' until grandchild is also processed or garbage collected
# In a real application, you might re-parent grandchildren or handle them explicitly.
```

### Diagram
```mermaid
graph TD
    A[Symbol to Delete] --> B{delete&#40&#41};
    B -- "Removes from" --> C[Parents' Children Lists];
    B -- "Removes from" --> D[Children's Parents Lists];
    B -- "Clears" --> E[Its Own Parent/Child Lists];
    C --> F[Graph Consistency];
    D --> F;
    E --> F;

    style A fill:#3ed964,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:#3ed964,stroke:#333,stroke-width:2px,color:#000000;
```
## `symbol.elevate()`: Promotes Metadata to Instance Attributes/Methods

The `elevate()` method is a key component of the `Symbol` framework's memory-aware maturing process. It facilitates the transformation of dynamic metadata, initially stored in the `Symbol`'s `metadata` `DefDict`, into static, first-class instance attributes or methods. This promotion enhances performance by enabling direct attribute access, which is generally faster than dictionary lookups, and contributes to a more predictable object structure.

### Purpose and Usage
To convert dynamic metadata associated with a `Symbol` into direct attributes or methods of the `Symbol` instance. This is part of optimizing the `Symbol`'s memory footprint and access speed.

### Code Example
```python
from symbol import Symbol

# Create a symbol with metadata
s = Symbol('MySymbol')
s.metadata['version'] = '1.0'
s.metadata['status'] = 'active'

def custom_method(self):
    return f"This is {self.name} version {self.version} with status {self.status}."

s.metadata['get_info'] = custom_method

print(f"Before elevate: Metadata: {s.metadata}")
print(f"Before elevate: Has 'version' attribute? {'version' in s.__dict__}")

# Elevate metadata
s.elevate()

print(f"After elevate: Metadata: {s.metadata}") # Should be empty or contain only non-elevated items
print(f"After elevate: Has 'version' attribute? {'version' in s.__dict__}")
print(f"Elevated method call: {s.get_info()}")
```

### Diagram
```mermaid
graph TD
    A[Symbol.metadata] --> B{elevate&#40&#41};
    B -- "Transforms" --> C[Key-Value Pairs];
    C --> D[Direct Instance Attributes];
    C --> E[Direct Instance Methods];
    D --> F[Faster Access];
    E --> F;

    style A fill:#badb62,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:#badb62,stroke:#333,stroke-width:2px,color:#000000;
```
## `symbol.slim()`: Removes Unused Dynamically Applied Mixins

The `slim()` method is another integral part of the `Symbol` framework's memory optimization strategy. Its primary function is to remove dynamically applied mixins or attributes that are no longer actively used or have been superseded by elevated metadata. This process helps in reducing the memory footprint of `Symbol` instances by cleaning up transient or redundant components, ensuring that the object retains only necessary attributes.

### Purpose and Usage
To clean up a `Symbol` instance by removing dynamically added attributes or mixins that are not explicitly protected. This is part of the memory optimization process, especially after `elevate()`.

### Code Example
```python
from symbol import Symbol
from symbol.core.mixinability import register_mixin

# Create a symbol
s = Symbol('MySlimSymbol')

# Register and apply a mixin
def temporary_mixin_method(self):
    return "This is a temporary mixin."

register_mixin(Symbol, 'temp_method', temporary_mixin_method)
print(f"Before slim: Has 'temp_method'? {hasattr(s, 'temp_method')}")
print(f"Temporary method call: {s.temp_method()}")

# Slim the symbol
s.slim()

print(f"After slim: Has 'temp_method'? {hasattr(s, 'temp_method')}")
```

### Diagram
```mermaid
graph TD
    A[Symbol Instance] --> B{slim&#40&#41};
    B -- "Identifies" --> C[Dynamically Applied Mixins];
    C -- "Removes" --> D[Unused Attributes/Methods];
    D --> E[Reduced Memory Footprint];

    style A fill:#10cc31,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:#10cc31,stroke:#333,stroke-width:2px,color:#000000;
```
## `symbol.immute()`: Orchestrates Maturing Process (Elevate, Slim, Freeze)

The `immute()` method serves as the orchestrator for the entire memory-aware maturing process. It encapsulates the sequential execution of `elevate()`, `slim()`, and `freeze()`, providing a single, atomic operation to transition a `Symbol` instance into its optimized, immutable state. This method is designed to be called when a `Symbol` has reached a stable point in its lifecycle, ensuring that its structure and behavior are finalized for performance and predictability.

### Purpose and Usage
To perform a complete memory optimization and finalization of a `Symbol` instance. This method should be called when a `Symbol`'s dynamic phase is complete and it needs to be optimized for long-term use.

### Code Example
```python
from symbol import Symbol
from symbol.core.mixinability import register_mixin, is_frozen

# Create a symbol with initial dynamic state
s = Symbol('FinalSymbol')
s.metadata['config_param'] = 'value_A'

def dynamic_behavior(self):
    return f"Dynamic behavior for {self.name}."

register_mixin(Symbol, 'dyn_behavior', dynamic_behavior)

print(f"Before immute: Metadata: {s.metadata}")
print(f"Before immute: Has 'dyn_behavior'? {hasattr(s, 'dyn_behavior')}")
print(f"Before immute: Is Symbol class frozen? {is_frozen()}")

# Immuting the symbol
s.immute()

print(f"After immute: Metadata: {s.metadata}")
print(f"After immute: Has 'dyn_behavior'? {hasattr(s, 'dyn_behavior')}") # Should be False if not protected
print(f"After immute: Is Symbol class frozen? {is_frozen()}")
print(f"Elevated attribute: {s.config_param}")
```

### Diagram
```mermaid
graph TD
    A[Initial Symbol State] --> B{immute&#40&#41};
    B -- "1. Elevate&#40&#41" --> C[Metadata to Attributes];
    C -- "2. Slim&#40&#41" --> D[Remove Unused Mixins];
    D -- "3. Freeze&#40&#41" --> E[Lock Symbol Class];
    E --> F[Optimized, Immutable Symbol];

    style A fill:#f750dc,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:#f750dc,stroke:#333,stroke-width:2px,color:#000000;
```
## `symbol.ref`: Alias for `symbol.origin` to Track Source Provenance

The `ref` property serves as a convenient alias for `symbol.origin`, providing a standardized way to track the provenance or original source of a `Symbol` instance. This is particularly valuable in data lineage, auditing, or debugging scenarios where understanding the origin of a symbolic entity is crucial. By explicitly linking a `Symbol` to its source, the framework enhances traceability and data governance.

### Purpose and Usage
To store and retrieve a reference to the original source or data from which the `Symbol` was created. This helps in tracking data lineage.

### Code Example
```python
from symbol import Symbol

# Create symbols with origin
data_row = {'id': 123, 'value': 'abc'}
s1 = Symbol('data_entry_123', origin=data_row)

file_path = '/path/to/source_file.txt'
s2 = Symbol('config_setting_A', origin=file_path)

print(f"Symbol s1 name: {s1.name}, origin (ref): {s1.ref}")
print(f"Symbol s2 name: {s2.name}, origin (ref): {s2.ref}")

# You can also set the ref property
s3 = Symbol('new_symbol')
s3.ref = {'source': 'user_input', 'timestamp': '2025-07-04'}
print(f"Symbol s3 name: {s3.name}, origin (ref): {s3.ref}")
```

### Diagram
```mermaid
graph TD
    A[Data Source] --> B[Symbol Creation];
    B -- "Sets origin" --> C[Symbol Instance];
    C -- "Accessed via" --> D[symbol.ref];
    D --> E[Provenance Tracking];

    style A fill:#338880,stroke:#333,stroke-width:2px,color:#FFFFFF;

    style A fill:#338880,stroke:#333,stroke-width:2px,color:#FFFFFF;
```
## `Scheduler.add_job(job)`: Schedules a New Job for Execution

The `Scheduler.add_job()` method is the primary interface for integrating tasks into the `Symbol` framework's scheduling system. It allows for the registration of `ScheduledJob` instances, which encapsulate a callable function, its arguments, and the specified execution schedule. This method is crucial for enabling automated, time-based execution of arbitrary functions, supporting both one-off and recurring tasks.

### Purpose and Usage
To add a `ScheduledJob` to the scheduler's queue for future execution. This is how you automate tasks within the `Symbol` framework.

### Code Example
```python
from symbol.core.schedule import Scheduler, ScheduledJob
import pendulum
import time

def my_scheduled_task(message):
    print(f"[{pendulum.now()}] Scheduled task executed: {message}")

# Initialize the scheduler
scheduler = Scheduler()

# Schedule a job to run in 5 seconds
future_time = pendulum.now().add(seconds=5)
job1 = ScheduledJob(my_scheduled_task, args=("Hello from future!",), kwargs={}, schedule=future_time)
scheduler.add_job(job1)

# Schedule a recurring job using cron syntax (every minute)
job2 = ScheduledJob(my_scheduled_task, args=("Hello from recurring job!",), kwargs={}, schedule="* * * * *")
scheduler.add_job(job2)

print("Scheduler started. Waiting for jobs...")
scheduler.start()

try:
    time.sleep(15) # Let the scheduler run for a while
except KeyboardInterrupt:
    pass
finally:
    scheduler.stop()
    print("Scheduler stopped.")
```

### Diagram
```mermaid
graph TD
    A[Callable Function] --> B[Create ScheduledJob];
    C[Schedule Details] --> B;
    B --> D{Scheduler.add_job&#40job&#41};
    D --> E[Add to Internal Queue];
    E --> F[Job Awaits Execution];
    style C fill:#6b894b,stroke:#333,stroke-width:2px,color:#FFFFFF;

    style A fill:#92925a,stroke:#333,stroke-width:2px,color:#000000;
    style C fill:#6b894b,stroke:#333,stroke-width:2px,color:#FFFFFF;
```
For a comprehensive overview of the Symbol API, refer to the [API Overview Diagram](api_overview.mmd).
