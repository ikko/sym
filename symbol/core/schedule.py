"""This module provides the core scheduling logic for the Symbol project.

It includes the Scheduler class, which is responsible for managing the schedule of jobs,
and the ScheduledJob class, which represents a single scheduled job.
"""
import anyio
import datetime
import heapq
import threading
import time
import uuid
from typing import Callable, Any, Optional, Union
import inspect
import logging

import orjson
from croniter import croniter

from ..core.base_symbol import Symbol


class ScheduledJob:
    """Represents a single scheduled job."""

    def __init__(
        self,
        func: Callable[..., Any],
        args: tuple,
        kwargs: dict,
        schedule: Union[str, datetime.datetime, datetime.date, datetime.time, Symbol],
        new_process: bool = False,
        new_thread: bool = True,
        id: Optional[str] = None,
    ):
        """
        what: Initializes a ScheduledJob instance.
        why: To encapsulate job details and scheduling parameters.
        how: Stores function, arguments, schedule, and calculates next run time.
        when: When a new job is created for the scheduler.
        by (caller(s)): Scheduler.add_job, Scheduler.from_dict.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Creating a task entry.
        how, what, why and when to improve: N/A.
        """
        self.id = id or str(uuid.uuid4())
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.schedule = schedule
        self.new_process = new_process
        self.new_thread = new_thread
        self.next_run: Optional[datetime.datetime] = None
        self._calculate_next_run()
        logging.debug(f"ScheduledJob {self.id} initialized. Next run: {self.next_run}")

    def _calculate_next_run(self, base_time: Optional[datetime.datetime] = None):
        """
        what: Calculates the next run time for the job.
        why: To determine when the job should be executed next.
        how: Parses schedule string (cron/ISO 8601) or datetime objects.
        when: Upon job initialization and after recurring job execution.
        by (caller(s)): ScheduledJob.__init__, Scheduler._run.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Setting a future alarm.
        how, what, why and when to improve: Handle more complex scheduling patterns.
        """
        now = base_time or datetime.datetime.now()
        logging.debug(f"Calculating next run for job {self.id} at base_time {now}")

        if isinstance(self.schedule, str):
            # Handle cron string
            try:
                self.next_run = croniter(self.schedule, now).get_next(datetime.datetime)
            except (ValueError, KeyError):
                # Handle ISO 8601 string
                try:
                    parsed_time = datetime.datetime.fromisoformat(self.schedule)
                    self.next_run = parsed_time
                except ValueError:
                    raise ValueError(f"Schedule string '{self.schedule}' is not a valid cron or ISO 8601 format.")
        elif isinstance(self.schedule, datetime.datetime):
            self.next_run = self.schedule
        elif isinstance(self.schedule, datetime.date):
            self.next_run = datetime.datetime.combine(self.schedule, datetime.time.min)
        elif isinstance(self.schedule, datetime.time):
            today = datetime.date.today()
            combined_datetime = datetime.datetime.combine(today, self.schedule)
            self.next_run = combined_datetime
            if self.next_run < now:
                self.next_run += datetime.timedelta(days=1) # Schedule for next day if time has passed today
        elif isinstance(self.schedule, Symbol):
            try:
                parsed_time = datetime.datetime.fromisoformat(self.schedule.name)
                self.next_run = parsed_time
            except ValueError:
                raise ValueError(f"Symbol name '{self.schedule.name}' is not a valid ISO 8601 datetime string.")
        else:
            raise TypeError(f"Unsupported schedule type: {type(self.schedule)}")

        

    def __lt__(self, other: "ScheduledJob") -> bool:
        """
        what: Compares two ScheduledJob instances.
        why: To enable sorting in the heapq (priority queue).
        how: Compares based on their `next_run` times.
        when: When jobs are added to or managed in the scheduler's heap.
        by (caller(s)): heapq operations.
        how often: Frequently.
        how much: Minimal.
        what is it like: Prioritizing tasks by deadline.
        how, what, why and when to improve: N/A.
        """
        if self.next_run is None:
            return False
        if other.next_run is None:
            return True
        return self.next_run < other.next_run

    def to_dict(self) -> dict:
        """
        what: Serializes the job to a dictionary.
        why: To persist job data for saving and loading.
        how: Extracts job attributes into a dictionary.
        when: When saving the scheduler's state.
        by (caller(s)): Scheduler.save_schedule.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Packaging job details.
        how, what, why and when to improve: Handle more complex function serialization.
        """
        return {
            "id": self.id,
            "func": f"{self.func.__module__}.{self.func.__name__}",
            "args": self.args,
            "kwargs": self.kwargs,
            "schedule": self.schedule,
            "new_process": self.new_process,
            "new_thread": self.new_thread,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ScheduledJob":
        """
        what: Deserializes a job from a dictionary.
        why: To reconstruct job instances from persisted data.
        how: Reconstructs function from module and name, creates ScheduledJob.
        when: When loading the scheduler's state.
        by (caller(s)): Scheduler.load_schedule.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Unpacking job details.
        how, what, why and when to improve: Handle more complex function deserialization.
        """
        func_str = data["func"]
        module_name, func_name = func_str.rsplit('.', 1)
        module = __import__(module_name, fromlist=[func_name])
        func = getattr(module, func_name)
        return cls(
            id=data["id"],
            func=func,
            args=tuple(data["args"]),
            kwargs=data["kwargs"],
            schedule=data["schedule"],
            new_process=data["new_process"],
            new_thread=data["new_thread"],
        )


class Scheduler:
    """Manages the schedule of jobs."""

    def __init__(self, schedule_file: Optional[str] = None):
        """
        what: Initializes the Scheduler.
        why: To set up the job management system.
        how: Initializes internal data structures and loads schedule if file provided.
        when: Upon Scheduler instantiation.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Setting up a control center.
        how, what, why and when to improve: N/A.
        """
        self._schedule: list[ScheduledJob] = []
        self._lock = anyio.Lock()
        self._running = False
        self.job_map: dict[str, ScheduledJob] = {}
        self.schedule_file = schedule_file
        if self.schedule_file:
            # Load schedule asynchronously, but __init__ is sync. Need to handle this.
            # For now, we'll assume load_schedule is called from an async context or wrapped.
            pass # Will address load_schedule later

    async def add_job(self, job: ScheduledJob):
        """
        what: Adds a job to the schedule.
        why: To register a job for future execution.
        how: Pushes job onto a min-heap, adds to job map, saves schedule.
        when: When a new job needs to be scheduled.
        by (caller(s)): Scheduler.add_jobs, ScheduledJob._calculate_next_run, external code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Adding a task to a to-do list.
        how, what, why and when to improve: Optimize for high-frequency additions.
        """
        async with self._lock:
            heapq.heappush(self._schedule, job)
            self.job_map[job.id] = job
            if self.schedule_file:
                await self.save_schedule()

    async def add_jobs(self, jobs: list[ScheduledJob]):
        """
        what: Adds multiple jobs to the schedule.
        why: To efficiently register a batch of jobs.
        how: Iterates through jobs, calls `add_job` for each.
        when: When multiple jobs need to be scheduled.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Depends on number of jobs.
        what is it like: Adding multiple tasks to a list.
        how, what, why and when to improve: Optimize for very large batches.
        """
        async with self._lock:
            for job in jobs:
                heapq.heappush(self._schedule, job)
                self.job_map[job.id] = job
            if self.schedule_file:
                await self.save_schedule()

    async def remove_job(self, job_id: str) -> Optional[ScheduledJob]:
        """
        what: Removes a job from the schedule.
        why: To cancel or unregister a job.
        how: Removes from job map, rebuilds heap, saves schedule.
        when: When a job needs to be removed.
        by (caller(s)): External code.
        how often: Infrequently.
        how much: Minimal.
        what is it like: Deleting a task from a list.
        how, what, why and when to improve: Optimize for high-frequency removals.
        """
        async with self._lock:
            job = self.job_map.pop(job_id, None)
            if job:
                # Rebuild the heap without the removed job
                self._schedule = [j for j in self.job_map.values()]
                heapq.heapify(self._schedule)
                if self.schedule_file:
                    await self.save_schedule()
            return job

    async def _run(self):
        """
        what: The main execution loop of the scheduler.
        why: To continuously check and execute scheduled jobs.
        how: Loops, sleeps until next job, executes job, reschedules recurring jobs.
        when: When the scheduler is started.
        by (caller(s)): Scheduler.start.
        how often: Continuously while scheduler is running.
        how much: Minimal when idle, depends on job execution.
        what is it like: A clock ticking and triggering events.
        how, what, why and when to improve: More precise sleep, better error handling.
        """
        logging.debug("Scheduler _run started.")
        while self._running:
            await anyio.sleep(0) # Yield control to the event loop
            time_to_sleep = 1 # Default sleep time

            async with self._lock:
                if not self._schedule:
                    logging.debug("Schedule is empty. Sleeping for 1 second.")
                    time_to_sleep = 1
                else:
                    now = datetime.datetime.now()
                    next_job = self._schedule[0]
                    logging.debug(f"Current time: {now}, Next job scheduled for: {next_job.next_run}")
                    
                    if next_job.next_run is not None and now >= next_job.next_run:
                        job_to_run = heapq.heappop(self._schedule)
                        logging.debug(f"Job {job_to_run.id} popped from heap. Next run: {job_to_run.next_run}")
                        logging.debug(f"Executing job: {job_to_run.id}")
                        
                        # Run the job
                        if inspect.iscoroutinefunction(job_to_run.func):
                            logging.info(f"Running async job {job_to_run.id}")
                            await job_to_run.func(*job_to_run.args, **job_to_run.kwargs)
                        else:
                            logging.info(f"Running sync job {job_to_run.id}")
                            await anyio.to_thread.run_sync(job_to_run.func, *job_to_run.args, **job_to_run.kwargs)

                        # Reschedule if it's a recurring job (cron string)
                        if isinstance(job_to_run.schedule, str) and croniter.is_valid(job_to_run.schedule):
                            job_to_run._calculate_next_run(base_time=now)
                            if job_to_run.next_run:
                                await self.add_job(job_to_run)
                                logging.debug(f"Job {job_to_run.id} rescheduled for: {job_to_run.next_run}")
                            else:
                                logging.debug(f"Job {job_to_run.id} is a recurring job but has no future runs. Removing.")
                                self.job_map.pop(job_to_run.id, None)
                        else:
                            # One-off job, remove from map
                            self.job_map.pop(job_to_run.id, None)
                            logging.debug(f"One-off job {job_to_run.id} executed and removed.")
                        
                        continue # Check for next job immediately

                    logging.debug(f"Next job {next_job.id} not due yet. Next run: {next_job.next_run}, Current time: {now}")
                    time_to_sleep = max(0, (next_job.next_run - now).total_seconds()) if next_job.next_run else 1
                    logging.debug(f"Next job not due yet. Sleeping for {time_to_sleep:.2f} seconds.")
            
            await anyio.sleep(max(0.01, time_to_sleep))

            

    async def start(self, task_group: anyio.abc.TaskGroup):
        """
        what: Starts the scheduler.
        why: To begin monitoring and executing scheduled jobs.
        how: Sets running flag, starts `_run` in a task group.
        when: When the scheduler needs to be activated.
        by (caller(s)): External code.
        how often: Once per scheduler instance.
        how much: Minimal.
        what is it like: Turning on a machine.
        how, what, why and when to improve: N/A.
        """
        if self._running:
            return
        self._running = True
        task_group.start_soon(self._run)

    async def stop(self):
        """
        what: Stops the scheduler.
        why: To halt job monitoring and execution.
        how: Sets running flag to False.
        when: When the scheduler needs to be deactivated.
        by (caller(s)): External code.
        how often: Once per scheduler instance.
        how much: Minimal.
        what is it like: Turning off a machine.
        how, what, why and when to improve: Ensure graceful shutdown of active jobs.
        """
        if not self._running:
            return
        self._running = False

    async def save_schedule(self):
        """
        what: Saves the schedule to a file.
        why: To persist the current state of scheduled jobs.
        how: Serializes job data to JSON, writes to file in a thread.
        when: After modifications to the schedule.
        by (caller(s)): add_job, add_jobs, remove_job.
        how often: Infrequently.
        how much: Depends on number of jobs.
        what is it like: Saving a configuration.
        how, what, why and when to improve: Optimize for large schedules.
        """
        if not self.schedule_file:
            return
        async with self._lock:
            # File I/O is blocking, so run in a thread
            await anyio.to_thread.run_sync(self._write_schedule_to_file)

    def _write_schedule_to_file(self):
        """
        what: Synchronous helper to write schedule to file.
        why: To perform blocking file I/O outside the event loop.
        how: Opens file, serializes job map to JSON, writes bytes.
        when: Called by `save_schedule` in a separate thread.
        by (caller(s)): save_schedule.
        how often: Infrequently.
        how much: Depends on schedule size.
        what is it like: Writing data to disk.
        how, what, why and when to improve: N/A.
        """
        with open(self.schedule_file, "wb") as f:
            f.write(orjson.dumps([job.to_dict() for job in self.job_map.values()]))

    async def load_schedule(self):
        """
        what: Loads the schedule from a file.
        why: To restore previously saved job configurations.
        how: Reads JSON from file in a thread, deserializes, adds jobs.
        when: Upon scheduler initialization or explicit load request.
        by (caller(s)): Scheduler.__init__ (indirectly), external code.
        how often: Infrequently.
        how much: Depends on schedule size.
        what is it like: Loading a configuration.
        how, what, why and when to improve: Optimize for large schedules.
        """
        if not self.schedule_file:
            return
        try:
            async with self._lock:
                jobs_data = await anyio.to_thread.run_sync(self._read_schedule_from_file)
                for job_data in jobs_data:
                    job = ScheduledJob.from_dict(job_data)
                    await self.add_job(job) # add_job is now async
        except FileNotFoundError:
            pass

    def _read_schedule_from_file(self) -> list[dict]:
        """
        what: Synchronous helper to read schedule from file.
        why: To perform blocking file I/O outside the event loop.
        how: Opens file, reads bytes, deserializes JSON.
        when: Called by `load_schedule` in a separate thread.
        by (caller(s)): load_schedule.
        how often: Infrequently.
        how much: Depends on schedule size.
        what is it like: Reading data from disk.
        how, what, why and when to improve: N/A.
        """
        with open(self.schedule_file, "rb") as f:
            return orjson.loads(f.read())