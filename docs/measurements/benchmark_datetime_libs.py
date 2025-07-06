from pathlib import Path
import datetime
import timeit
import tracemalloc
import pandas as pd
from dateutil import parser as dateutil_parser
import rich
from rich.console import Console
from rich.table import Table
from rich.progress import track

# Try importing optional libraries
try:
    import arrow
except ImportError:
    arrow = None

try:
    import pendulum
except ImportError:
    pendulum = None

# Benchmark config
N_values = [1, 10, 100, 1000, 10000]
libraries = {
    "datetime": lambda: datetime.datetime.now(),
    "dateutil": lambda: dateutil_parser.parse("2025-07-06T14:00:00Z"),
}
if arrow:
    libraries["arrow"] = lambda: arrow.now()
if pendulum:
    libraries["pendulum"] = lambda: pendulum.now("UTC")

# Benchmark function
def benchmark_datetime_libraries():
    results = []

    def measure(lib_name, creation_func):
        for N in N_values:
            t = timeit.timeit(lambda: [creation_func() for _ in range(N)], number=1)
            tracemalloc.start()
            _ = [creation_func() for _ in range(N)]
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            results.append({
                "Library": lib_name,
                "N": N,
                "Time (s)": round(t, 6),
                "Peak Memory (KB)": peak // 1024,
            })

    for lib_name, func in track(libraries.items(), description="Benchmarking..."):
        measure(lib_name, func)

    return results

# Pretty output
def render_results_table(results):
    console = Console()
    table = Table(title="Datetime Library Benchmark")

    table.add_column("Library", style="cyan", no_wrap=True)
    table.add_column("N", justify="right", style="magenta")
    table.add_column("Time (s)", justify="right", style="green")
    table.add_column("Peak Memory (KB)", justify="right", style="yellow")

    for row in results:
        table.add_row(str(row["Library"]), str(row["N"]), str(row["Time (s)"]), str(row["Peak Memory (KB)"]))

    console.print(table)

# Main entry point
if __name__ == "__main__":
    results = benchmark_datetime_libraries()
    render_results_table(results)
