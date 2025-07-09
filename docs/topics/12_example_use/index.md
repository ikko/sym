# Example Use: Practical Applications of the Symbol Framework

The `Symbol` framework is designed to be versatile, providing a powerful foundation for a wide range of applications that benefit from graph-based data structures and symbic manipulation. This section illustrates several practical use cases, demonstrating how `Symbol`'s core features can be leveraged to solve real-world problems.

## Basic Symbol Creation and Relationships

This example demonstrates the fundamental operations of creating `Symbol` instances and establishing basic parent-child relationships. It showcases the simplicity of defining a graph structure using `Symbol` and the `add()` method.

### Code Example
```python
from symb import s, Symbol

# --- Basic Symbol creation and relationships ---
hello = Symbol('hello')
world = s.world
hello.add(world)
print(hello.tree())
```
<details>
<summary>Outcome</summary>

```text
[<Symbol: hello>, <Symbol: world>]
```
</details>

### Explanation
- `Symbol('hello')`: Creates a `Symbol` instance named 'hello'. Due to the interning mechanism, if 'hello' already exists, the existing instance is returned.
- `s.world`: Utilizes the `SymbolNamespace` (`s`) for a more concise way to create a `Symbol` named 'world'. This is syntactic sugar for `Symbol('world')`.
- `hello.add(world)`: Establishes a directed relationship from `hello` to `world`, making `world` a child of `hello`. If the relationship already exists, it's idempotent.
- `print(hello.tree())`: Performs a depth-first traversal starting from `hello` and prints the names of all reachable symbs in a tree-like structure.

### Diagram
```mermaid
graph TD
    A[hello] --> B[world];

    style A fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style B fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
```
## ESG Example: Tracking Deforestation in a Supply Chain

This example illustrates how `Symbol` can model complex supply chain relationships and track specific events, such as deforestation. It demonstrates the ability to build a graph representing entities and their connections, and then query this graph to identify paths that lead to undesirable events.

### Code Example
```python
from symb import s, Symbol
from symb.core.mixinability import register_mixin
from symb.core.protocols import SymbolProtocol
from symb.builtins import apply_builtins

class SupplyChainMixin(SymbolProtocol):
    def buys_from(self, supplier: Symbol):
        self.add(supplier)

    def sources_from(self, source: Symbol):
        self.add(source)

register_mixin(SupplyChainMixin, expand=True)
apply_builtins()

s.Global_Goods_Inc.buys_from(s.Palm_Oil_Processor)
s.Palm_Oil_Processor.buys_from(s.Supplier_A)
s.Palm_Oil_Processor.buys_from(s.Supplier_B)
s.Supplier_A.sources_from(s.Plantation_X)
s.Supplier_B.sources_from(s.Plantation_Y)
s.Plantation_Y.add(s.deforestation_event_2024_Q4)

def has_deforestation(symb):
    return 'deforestation' in symb.name

for path in s.Global_Goods_Inc.match(has_deforestation):
    print(f"Deforestation Link Found: {path.path_to(s.deforestation_event_2024_Q4)}")
```
<details>
<summary>Outcome</summary>

```text
Deforestation Link Found: ['<Symbol: Global_Goods_Inc>', '<Symbol: Palm_Oil_Processor>', '<Symbol: Supplier_B>', '<Symbol: Plantation_Y>', '<Symbol: deforestation_event_2024_Q4>']
```
</details>

### Explanation
- **Supply Chain Modeling**: Each entity (e.g., `Global_Goods_Inc`, `Palm_Oil_Processor`, `Plantation_X`) is represented as a `Symbol`. Relationships like `buys_from` and `sources_from` are established using custom methods (which would internally use `add()` or `relate_to()`).
- **Event Representation**: `s.deforestation_event_2024_Q4` is a `Symbol` representing a specific event, linked to `Plantation_Y`.
- **Graph Querying**: The `has_deforestation` function acts as a predicate to identify symbs related to deforestation. `s.Global_Goods_Inc.match(has_deforestation)` performs a graph traversal (likely a depth-first search or breadth-first search) to find all paths from `Global_Goods_Inc` to any symb satisfying the predicate.
- `path.path_to(s.deforestation_event_2024_Q4)`: Once a path is found, this method reconstructs the sequence of symbs from the starting point to the deforestation event, providing traceability.

### Diagram
```mermaid
graph TD
    A[Global_Goods_Inc] --> B[Palm_Oil_Processor];
    B --> C[Supplier_A];
    B --> D[Supplier_B];
    C --> E[Plantation_X];
    D --> F[Plantation_Y];
    F --> G[deforestation_event_2024_Q4];

    style A fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style B fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style D fill:#FF4500,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style E fill:#8A2BE2,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style F fill:#FF1493,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style G fill:#00FFFF,stroke:#333,stroke-width:2px,color:#000000;
```
## Timeline Example

This example showcases the use of `symb.builtins.timeline` to manage and analyze temporal data. It demonstrates how to create timelines, add time periods, and perform operations like finding overlaps between different timelines.

### Code Example
```python
from symb.builtins.timeline import Timeline
import datetime

timeline1 = Timeline()
timeline1.add_period(datetime.datetime(2023, 1, 1), datetime.datetime(2023, 1, 15))
timeline1.add_period(datetime.datetime(2023, 1, 10), datetime.datetime(2023, 1, 20))

timeline2 = Timeline()
timeline2.add_period(datetime.datetime(2023, 1, 5), datetime.datetime(2023, 1, 12))

overlap_timeline = timeline1.overlap(timeline2)
print(f"Overlap periods: {list(overlap_timeline)}")
print(timeline1.to_ascii())
```
<details>
<summary>Outcome</summary>

```text
Overlap periods: []
#----------#----
```
</details>

### Explanation
- `Timeline()`: Instantiates a `Timeline` object, which is a specialized `Symbol` for managing time intervals.
- `add_period()`: Adds a time period (defined by start and end `datetime.datetime` objects) to the timeline. These periods are internally represented as `Symbol` instances.
- `overlap()`: A method provided by the `Timeline` class that calculates the overlapping periods between two timelines. This demonstrates `Symbol`'s ability to extend its core functionality for domain-specific operations.
- `to_ascii()`: Visualizes the timeline using ASCII art, providing a quick textual representation of the time periods.

### Diagram
```mermaid
graph TD
    A[Timeline 1] -- "Period 1" --> B[2023-01-01_to_2023-01-15]
    A -- "Period 2" --> C[2023-01-10_to_2023-01-20]
    X[Timeline 2] -- "Period 3" --> Y[2023-01-05_to_2023-01-12]
    A -- "overlap()" --> Z[Overlap Periods];

    style A fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style B fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style X fill:#FF4500,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style Y fill:#8A2BE2,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style Z fill:#FF1493,stroke:#333,stroke-width:2px,color:#FFFFFF;
```
## Batch Processing Example

This example demonstrates a simple batch processing utility, showcasing how `Symbol` can be used in conjunction with functional programming paradigms to apply a given function to a collection of inputs. While `Symbol` itself is not a batch processing engine, its extensibility allows for the integration of such utilities.

### Code Example
```python
from symb.core.batch_processing import process_batch

def square(x): return x * x
results = process_batch([1, 2, 3, 4], square)
print(f"Batch processing results: {results}")
```
<details>
<summary>Outcome</summary>

```text
Batch processing results: [1, 4, 9, 16]
```
</details>

### Explanation
- `process_batch()`: A utility function (likely part of `symb.core.batch_processing`) that takes a list of inputs and a function, applying the function to each input in a batch. This highlights how `Symbol` can be part of a larger system, where its symbic representations can be processed by external functions.
- `square()`: A simple function demonstrating the type of operation that can be applied in a batch.

### Diagram
```mermaid
graph LR
    A[Input List] --> B{process_batch&#40&#41};
    C[Function &#40e.g., square&#41] --> B;
    B --> D[Processed Results];

    style A fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style B fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style D fill:#FF4500,stroke:#333,stroke-width:2px,color:#FFFFFF;
```
## Scheduler Example

This example demonstrates the use of `symb.core.schedule` to schedule and execute tasks at specified times. It showcases the `Scheduler` and `ScheduledJob` classes, allowing for the automation of functions based on time dimension objects.

### Code Example
```python
from symb.core.schedule import Scheduler, ScheduledJob
import time
import datetime

def my_task(message):
    print(f"Executing task: {message}")

scheduler = Scheduler()
job = ScheduledJob(my_task, args=("Hello` from the scheduler!",), schedule=datetime.datetime.now() + datetime.timedelta(seconds=5))
scheduler.add_job(job)

scheduler.start()
time.sleep(6) # Wait for the job to run
scheduler.stop()
```
<details>
<summary>Outcome</summary>

```text
Executing task: Hello from the scheduler!
```
</details>

### Explanation
- `Scheduler()`: Initializes the scheduler, which runs in a separate thread to monitor and execute jobs.
- `ScheduledJob()`: Creates a job object, specifying the function to run (`my_task`), its arguments, and the `schedule` (in this case, 5 seconds from now).
- `scheduler.add_job(job)`: Adds the created job to the scheduler's queue.
- `scheduler.start()`: Initiates the scheduler's execution loop.
- `time.sleep()`: Pauses the main thread to allow the scheduler thread to execute the scheduled task.
- `scheduler.stop()`: Halts the scheduler's execution.

### Diagram
```mermaid
graph TD
    A[Function &#40my_task&#41] --> B[ScheduledJob];
    C[Schedule &#40datetime.datetime&#41] --> B;
    B --> D[Scheduler.add_job&#40&#41];
    D --> E[Scheduler.start&#40&#41];
    E -- "Executes at time" --> A;

    style A fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style B fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style D fill:#FF4500,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style E fill:#8A2BE2,stroke:#333,stroke-width:2px,color:#FFFFFF;
```
## Conclusion

These examples collectively demonstrate the versatility and power of the `Symbol` framework. From basic graph construction to complex supply chain analysis, temporal data management, batch processing, and task scheduling, `Symbol` provides a flexible and efficient foundation for building sophisticated applications. Its modular design and extensibility allow developers to tailor its capabilities to specific domain requirements, making it a valuable tool for a wide array of symbic data manipulation tasks.

---
