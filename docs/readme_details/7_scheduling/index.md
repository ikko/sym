# Scheduling: Event-Driven Automation with Symbol

The `Symbol` framework integrates a robust scheduling mechanism, enabling the deferred and automated execution of tasks. This feature is critical for building event-driven architectures, automating workflows, and managing background processes within applications. The scheduler is designed for flexibility, supporting various scheduling paradigms from precise time dimension triggers to recurring cron-like expressions.

## Core Components: ScheduledJob and Scheduler

The scheduling system is built around two primary components:

1.  **`ScheduledJob`**: This class encapsulates a single task to be executed. It holds references to the callable function (`func`), its arguments (`args`, `kwargs`), and crucially, the `schedule` on which it should run. The `schedule` can be a `pendulum.DateTime` object for one-off tasks, a `cron` string for recurring jobs, or even a `Symbol` instance whose name represents an ISO 8601 datetime string.

    ```mermaid
graph TD
        A[Callable Function] --> B[ScheduledJob];
        C[Arguments &#40;args, kwargs&#41;] --> B;
        D[Schedule &#40;pendulum.DateTime, cron string, Symbol&#41;] --> B;
        B -- "Calculates" --> E[Next Run Time];
    style D fill:lighten&#40;#896807, 30%&#41;,stroke:#333,stroke-width:2px,color:#FFFFFF;

    style A fill:#92925a,stroke:#333,stroke-width:2px,color:#000000;
    style C fill:lighten(#910f48, 30%),stroke:#333,stroke-width:2px,color:#FFFFFF;
    style D fill:lighten(#a5efdd, 30%),stroke:#333,stroke-width:2px,color:#000000;
```
2.  **`Scheduler`**: This class manages a collection of `ScheduledJob` instances. It operates in a separate thread, continuously monitoring the jobs and executing them when their `next_run` time arrives. The `Scheduler` uses a min-heap (`_schedule`) to efficiently retrieve the next job to be executed, ensuring timely processing. It also supports persistence, allowing the schedule to be saved to and loaded from a file, thus surviving application restarts.

    ```mermaid
graph TD
        A[Scheduler] --> B{add_job&#40;&#41;};
        B -- "Adds Job to" --> C[Min-Heap];;
        C -- "Monitors" --> D[Execution Thread];
        D -- "Executes Job" --> E[Callable Function];
        E -- "If Recurring" --> F[Reschedules Job];

    style A fill:#ffaac1,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:#ffaac1,stroke:#333,stroke-width:2px,color:#000000;
```
## Illustrative Examples

### High-Tech Industry: Microservice Orchestration
```python
from symbol.core.schedule import Scheduler, ScheduledJob
import pendulum, time

def data_ingestion(): print(f"[{pendulum.now()}] Data Ingestion.")
def data_transformation(): print(f"[{pendulum.now()}] Data Transformation.")
def data_loading(): print(f"[{pendulum.now()}] Data Loading.")

scheduler = Scheduler()
scheduler.add_job(ScheduledJob(data_ingestion, args=(), kwargs={}, schedule="* * * * *"))
scheduler.add_job(ScheduledJob(data_transformation, args=(), kwargs={}, schedule=pendulum.now().add(seconds=10)))
scheduler.add_job(ScheduledJob(data_loading, args=(), kwargs={}, schedule=pendulum.now().add(seconds=20)))

scheduler.start()
time.sleep(5) # Run for 5 seconds
scheduler.stop()
```

```mermaid
graph TD
    subgraph "Microservice Orchestration"
        A[Data Ingestion] --> B{Scheduler};
        B -- "Triggers" --> C[Data Transformation];
        C -- "Triggers" --> D[Data Loading];
        B -- "Recurring" --> A;
    end

    style A fill:#7779f4,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:#7779f4,stroke:#333,stroke-width:2px,color:#000000;
```
### Low-Tech Industry: Automated Report Generation

For businesses, automated report generation is a common requirement. The `Symbol` scheduler can reliably handle tasks like generating daily sales reports, weekly inventory summaries, or monthly financial statements.

```python
from symbol.core.schedule import Scheduler, ScheduledJob
import pendulum
import time

def generate_daily_sales_report():
    print(f"[{pendulum.now()}] Generating daily sales report...")
    # Simulate report generation logic
    time.sleep(0.5)
    print(f"[{pendulum.now()}] Daily sales report generated.")

def generate_weekly_inventory_summary():
    print(f"[{pendulum.now()}] Generating weekly inventory summary...")
    # Simulate report generation logic
    time.sleep(1)
    print(f"[{pendulum.now()}] Weekly inventory summary generated.")

scheduler = Scheduler()

# Schedule daily sales report for 23:00 every day
# Note: In a real scenario, you'd set the time more precisely, e.g., '0 23 * * *'
# For demonstration, we'll schedule it for a few seconds from now.
now = pendulum.now()
daily_report_time = now.add(seconds=5)
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

```mermaid
graph TD
    subgraph "Automated Report Generation"
        A[Daily Sales Report] --> B{Scheduler};
        B -- "Triggers Daily" --> A;
        C[Weekly Inventory Summary] --> B;
        B -- "Triggers Weekly" --> C;
    end
    style C fill:lighten&#40;#12dde0, 30%&#41;,stroke:#333,stroke-width:2px,color:#000000;

    style A fill:#93dd47,stroke:#333,stroke-width:2px,color:#000000;
    style C fill:lighten(#12dde0, 30%),stroke:#333,stroke-width:2px,color:#000000;
```
## Conclusion

The `Symbol` framework's scheduling capabilities provide a powerful and flexible foundation for automating tasks and orchestrating complex processes. By offering diverse scheduling options and robust job management, it empowers developers to build highly responsive and efficient systems, from sophisticated microservice deployments to routine business operations. The persistence feature further enhances its utility by ensuring that scheduled tasks are not lost across application lifecycles.

For a visual representation of the scheduling process, refer to the [Scheduling Flow Diagram](scheduling_flow.mmd).
