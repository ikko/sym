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
    """
    what: Dynamically imports a function from a string.
    why: To allow specifying job functions by their string path.
    how: Splits string into module and function names, imports, and gets attribute.
    when: When adding a job via CLI.
    by (caller(s)): add command.
    how often: Infrequently.
    how much: Minimal.
    what is it like: Resolving a function by name.
    how, what, why and when to improve: Handle more complex function paths.
    """
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
    what: Initializes the scheduler CLI application.
    why: To set up the global scheduler instance.
    how: Creates a Scheduler instance, optionally loading from a file.
    when: Upon CLI application startup.
    by (caller(s)): Typer framework.
    how often: Once per CLI invocation.
    how much: Minimal.
    what is it like: Setting up the main application context.
    how, what, why and when to improve: N/A.
    """
    global scheduler
    scheduler = Scheduler(schedule_file=schedule_file)


@app.command()
def add(
    func_str: str = typer.Argument(..., help="The function to be executed (e.g., 'my_module.my_function')."),
    schedule: str = typer.Argument(..., help="The schedule on which the job should be run (cron or ISO 8601)."),
):
    """
    what: Adds a new job to the schedule.
    why: To register a job for execution by the scheduler.
    how: Parses function string, creates ScheduledJob, adds to scheduler.
    when: When the 'add' command is invoked.
    by (caller(s)): User via CLI.
    how often: Infrequently.
    how much: Minimal.
    what is it like: Submitting a new task.
    how, what, why and when to improve: Add more job configuration options.
    """
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
    """
    what: Removes a job from the schedule.
    why: To cancel a previously registered job.
    how: Calls `scheduler.remove_job` with the job ID.
    when: When the 'remove' command is invoked.
    by (caller(s)): User via CLI.
    how often: Infrequently.
    how much: Minimal.
    what is it like: Deleting a task.
    how, what, why and when to improve: Add confirmation prompt.
    """
    job = scheduler.remove_job(job_id)
    if job:
        print(f"Successfully removed job {job.id}")
    else:
        print(f"Error: Job with ID '{job_id}' not found.")


@app.command()
def list():
    """
    what: Lists all jobs in the schedule.
    why: To view currently registered jobs and their status.
    how: Iterates through `scheduler.job_map` and prints job details.
    when: When the 'list' command is invoked.
    by (caller(s)): User via CLI.
    how often: Frequently.
    how much: Depends on number of jobs.
    what is it like: Displaying a task list.
    how, what, why and when to improve: Add filtering, sorting, more details.
    """
    if not scheduler.job_map:
        print("No jobs in the schedule.")
        return

    for job_id, job in scheduler.job_map.items():
        print(f"ID: {job_id}, Next Run: {job.next_run}, Schedule: {job.schedule}, Function: {job.func.__name__}")


@app.command()
def run():
    """
    what: Runs the scheduler.
    why: To start the job execution process.
    how: Calls `scheduler.start`, enters an infinite loop, handles Ctrl+C.
    when: When the 'run' command is invoked.
    by (caller(s)): User via CLI.
    how often: Infrequently.
    how much: Minimal to start, then continuous.
    what is it like: Starting a background service.
    how, what, why and when to improve: Implement graceful shutdown.
    """
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
