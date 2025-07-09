"""This module provides a Typer-based CLI for interacting with the scheduler.

It provides commands for adding, removing, and listing scheduled jobs,
as well as for running the scheduler.
"""
import typer
import importlib
from typing import Optional

from ..core.schedule import Scheduler, ScheduledJob

app = typer.Typer()

scheduler: Optional[Scheduler] = None


def _get_func_from_str(func_str: str):
    """Dynamically imports a function from a string."""
    module_name, func_name = func_str.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, func_name)


@app.callback()
def main(
    schedule_file: Optional[str] = typer.Option(
        None,
        "--schedule-file",
        "-f",
        help="The file where the schedule is stored.",
    )
):
    """
    A Typer-based CLI for interacting with the scheduler.
    """
    global scheduler
    scheduler = Scheduler(schedule_file=schedule_file)


@app.command()
def add(
    func_str: str = typer.Argument(..., help="The function to be executed (e.g., 'my_module.my_function')."),
    schedule: str = typer.Argument(..., help="The schedule on which the job should be run (cron or ISO 8601)."),
):
    """Adds a new job to the schedule."""
    try:
        func = _get_func_from_str(func_str)
        job = ScheduledJob(func=func, args=(), kwargs={}, schedule=schedule)
        scheduler.add_job(job)
        print(f"Successfully added job {job.id} for function '{func_str}' with schedule '{schedule}'")
    except (ImportError, AttributeError) as e:
        print(f"Error: Could not import function '{func_str}'. {repr(e)}")
    except (ValueError, TypeError) as e:
        print(f"Error: Invalid schedule format. {repr(e)}")


@app.command()
def remove(job_id: str = typer.Argument(..., help="The ID of the job to be removed.")):
    """Removes a job from the schedule."""
    job = scheduler.remove_job(job_id)
    if job:
        print(f"Successfully removed job {job.id}")
    else:
        print(f"Error: Job with ID '{job_id}' not found.")


@app.command()
def list():
    """Lists all the jobs in the schedule."""
    if not scheduler.job_map:
        print("No jobs in the schedule.")
        return

    for job_id, job in scheduler.job_map.items():
        print(f"ID: {job_id}, Next Run: {job.next_run}, Schedule: {job.schedule}, Function: {job.func.__name__}")


@app.command()
def run():
    """Runs the scheduler."""
    print("Starting scheduler...")
    scheduler.start()
    print("Scheduler started. Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping scheduler...")
        scheduler.stop()
        print("Scheduler stopped.")


if __name__ == "__main__":
    app()
