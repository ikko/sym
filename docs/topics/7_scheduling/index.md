# Scheduling: Event-Driven Automation with Symbol

The `Symbol` framework integrates a robust scheduling mechanism, enabling the deferred and automated execution of tasks. This feature is critical for building event-driven architectures, automating workflows, and managing background processes within applications. The scheduler is designed for flexibility, supporting various scheduling paradigms from precise time dimension triggers to recurring cron-like expressions.

## Core Components: ScheduledJob and Scheduler

The scheduling system is built around two primary components:

1.  **`ScheduledJob`**: This class encapsulates a single task to be executed. It holds references to the callable function (`func`), its arguments (`args`, `kwargs`), and crucially, the `schedule` on which it should run. The `schedule` can be a `datetime.datetime` object for one-off tasks, a `cron` string for recurring jobs, or even a `Symbol` instance whose name represents an ISO 8601 datetime string.

    ```mermaid
    graph TD
            A[Callable Function] --> B[ScheduledJob];
            C[Arguments #40;args, kwargs#41;] --> B;
            D[Schedule #40;datetime.datetime, cron string, Symbol#41;] --> B;
            B -- "Calculates" --> E[Next Run Time];
    
        style A fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
        style B fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
        style C fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
        style D fill:#FF4500,stroke:#333,stroke-width:2px,color:#FFFFFF;
        style E fill:#8A2BE2,stroke:#333,stroke-width:2px,color:#FFFFFF;
    ```
2.  **`Scheduler`**: This class manages a collection of `ScheduledJob` instances. It operates in a separate thread, continuously monitoring the jobs and executing them when their `next_run` time arrives. The `Scheduler` uses a min-heap (`_schedule`) to efficiently retrieve the next job to be executed, ensuring timely processing. It also supports persistence, allowing the schedule to be saved to and loaded from a file, thus surviving application restarts.

    ```mermaid
    graph TD
        A[Scheduler] --> B{add_job#40;#41;};
        B -- "Adds Job to" --> C[Min-Heap];;
        C -- "Monitors" --> D[Execution Thread];
        D -- "Executes Job" --> E[Callable Function];
        E -- "If Recurring" --> F[Reschedules Job];

      style A fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
      style B fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
      style C fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
      style D fill:#FF4500,stroke:#333,stroke-width:2px,color:#FFFFFF;
      style E fill:#8A2BE2,stroke:#333,stroke-width:2px,color:#FFFFFF;
      style F fill:#FF1493,stroke:#333,stroke-width:2px,color:#FFFFFF;
    ```

## Illustrative Examples

### Microservice Orchestration
```python
from symb.core.schedule import Scheduler, ScheduledJob
import datetime, time

def data_ingestion(): print(f"[{datetime.datetime.now()}] Data Ingestion.")
def data_transformation(): print(f"[{datetime.datetime.now()}] Data Transformation.")
def data_loading(): print(f"[{datetime.datetime.now()}] Data Loading.")

scheduler = Scheduler()
scheduler.add_job(ScheduledJob(data_ingestion, args=(), kwargs={}, schedule="* * * * *"))
scheduler.add_job(ScheduledJob(data_transformation, args=(), kwargs={}, schedule=datetime.datetime.now() + datetime.timedelta(seconds=10)))
scheduler.add_job(ScheduledJob(data_loading, args=(), kwargs={}, schedule=datetime.datetime.now() + datetime.timedelta(seconds=20)))

scheduler.start()
time.sleep(5) # Run for 5 seconds
scheduler.stop()
```
<details>
<summary>Outcome</summary>

```text
[2025-07-06 16:25:00.000000] Data Ingestion.
[2025-07-06 16:25:00.000000] Data Ingestion.
[2025-07-06 16:25:00.000000] Data Ingestion.
[2025-07-06 16:25:00.000000] Data Ingestion.
[2025-07-06 16:25:00.000000] Data Ingestion.
```
</details>

```mermaid
graph TD
    subgraph "Microservice Orchestration"
        A[Data Ingestion] --> B{Scheduler};
        B -- "Triggers" --> C[Data Transformation];
        C -- "Triggers" --> D[Data Loading];
        B -- "Recurring" --> A;
    end

    style A fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style B fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
    style D fill:#FF4500,stroke:#333,stroke-width:2px,color:#FFFFFF;
```

Automated Report Generation

For businesses, automated report generation is a common requirement. The `Symbol` scheduler can reliably handle tasks like generating daily sales reports, weekly inventory summaries, or monthly financial statements.

```python
from symb.core.schedule import Scheduler, ScheduledJob
import datetime
import time

def generate_daily_sales_report():
    print(f"[{datetime.datetime.now()}] Generating daily sales report...")
    # Simulate report generation logic
    time.sleep(0.5)
    print(f"[{datetime.datetime.now()}] Daily sales report generated.")

def generate_weekly_inventory_summary():
    print(f"[{datetime.datetime.now()}] Generating weekly inventory summary...")
    # Simulate report generation logic
    time.sleep(1)
    print(f"[{datetime.datetime.now()}] Weekly inventory summary generated.")

scheduler = Scheduler()

# Schedule daily sales report for 23:00 every day
# Note: In a real scenario, you'd set the time more precisely, e.g., '0 23 * * *'
# For demonstration, we'll schedule it for a few seconds from now.
daily_report_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
job_daily = ScheduledJob(generate_daily_sales_report, args=(), kwargs={}, schedule=daily_report_time)
scheduler.add_job(job_daily)

# Schedule weekly inventory summary for every Monday at 09:00
# For demonstration, we'll use a cron string for every minute
job_weekly = ScheduledJob(generate_weekly_inventory_summary, args=(), kwargs={}, schedule="* * * * MON")
scheduler.add_job(job_weekly)

print("Starting report generation scheduler...")
scheduler.start()

try:
    time.sleep(70) # Let it run for a bit
except KeyboardInterrupt:
    pass
finally:
    scheduler.stop()
    print("Scheduler stopped.")
```
<details>
<summary>Outcome</summary>

```text
Starting report generation scheduler...
[2025-07-06 16:25:00.000000] Generating daily sales report...
[2025-07-06 16:25:00.000000] Daily sales report generated.
[2025-07-06 16:25:00.000000] Generating weekly inventory summary...
[2025-07-06 16:25:00.000000] Weekly inventory summary generated.
Scheduler stopped.
```
</details>

```mermaid
graph TD
    subgraph "Automated Report Generation"
        A[Daily Sales Report] --> B{Scheduler};
        B -- "Triggers Daily" --> A;
        C[Weekly Inventory Summary] --> B;
        B -- "Triggers Weekly" --> C;
    end
    style A fill:#FFD700,stroke:#333,stroke-width:2px,color:#000000;
    style B fill:#1E90FF,stroke:#333,stroke-width:2px,color:#FFFFFF;
    style C fill:#32CD32,stroke:#333,stroke-width:2px,color:#000000;
```
## Conclusion

The `Symbol` framework's scheduling capabilities provide a powerful and flexible foundation for automating tasks and orchestrating complex processes. By offering diverse scheduling options and robust job management, it empowers developers to build highly responsive and efficient systems, from sophisticated microservice deployments to routine business operations. The persistence feature further enhances its utility by ensuring that scheduled tasks are not lost across application lifecycles.

For a visual representation of the scheduling process, refer to the [Scheduling Flow Diagram](scheduling_flow.mmd).

---
