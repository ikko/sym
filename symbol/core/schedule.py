"""This module provides the core scheduling logic for the Symbol project.

It includes the Scheduler class, which is responsible for managing the schedule of jobs,
and the ScheduledJob class, which represents a single scheduled job.
"""
import asyncio
import pendulum
import heapq
import threading
import time
import uuid
from typing import Callable, Any, Optional, Union

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
        schedule: Union[str, pendulum.DateTime, pendulum.Date, pendulum.Time, Symbol],
        new_process: bool = False,
        new_thread: bool = True,
        id: Optional[str] = None,
    ):
        self.id = id or str(uuid.uuid4())
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.schedule = schedule
        self.new_process = new_process
        self.new_thread = new_thread
        self.next_run: Optional[pendulum.DateTime] = None
        self._calculate_next_run()

    def _calculate_next_run(self, base_time: Optional[pendulum.DateTime] = None):
        """Calculates the next run time for the job."""
        now = base_time or pendulum.now()
        
        schedule = self.schedule
        if isinstance(schedule, str):
            if croniter.is_valid(schedule):
                self.next_run = croniter(schedule, now).get_next(pendulum.DateTime)
            else:
                try:
                    # Attempt to parse as an ISO datetime string
                    self.next_run = pendulum.parse(schedule)
                except ValueError:
                    raise ValueError(f"Schedule string '{schedule}' is not a valid cron or ISO 8601 format.")
        elif isinstance(schedule, pendulum.DateTime):
            self.next_run = schedule
        elif isinstance(schedule, pendulum.Date):
            self.next_run = pendulum.datetime(schedule.year, schedule.month, schedule.day)
        elif isinstance(schedule, pendulum.Time):
            today = pendulum.today()
            self.next_run = today.at(schedule.hour, schedule.minute, schedule.second)
            if self.next_run < now: # If time is already past today, schedule for tomorrow
                self.next_run = self.next_run.add(days=1)
        elif isinstance(schedule, Symbol):
            try:
                self.next_run = pendulum.parse(schedule.name)
            except ValueError:
                raise ValueError(f"Symbol name '{schedule.name}' is not a valid ISO 8601 datetime string.")
        else:
            raise TypeError(f"Unsupported schedule type: {type(schedule)}")

        # Ensure one-off jobs in the past are not scheduled to run
        if not isinstance(self.schedule, str) and self.next_run and self.next_run < now:
            self.next_run = None # Mark as not to be run

    def __lt__(self, other: "ScheduledJob") -> bool:
        if self.next_run is None:
            return False
        if other.next_run is None:
            return True
        return self.next_run < other.next_run

    def to_dict(self) -> dict:
        """Serializes the job to a dictionary."""
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
        """Deserializes a job from a dictionary."""
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
        self._schedule: list[ScheduledJob] = []
        self._lock = threading.RLock()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self.job_map: dict[str, ScheduledJob] = {}
        self.schedule_file = schedule_file
        if self.schedule_file:
            self.load_schedule()

    def add_job(self, job: ScheduledJob):
        """Adds a job to the schedule."""
        with self._lock:
            if job.next_run: # Only schedule jobs that have a future run time
                heapq.heappush(self._schedule, job)
                self.job_map[job.id] = job
                if self.schedule_file:
                    self.save_schedule()

    def remove_job(self, job_id: str) -> Optional[ScheduledJob]:
        """Removes a job from the schedule by its ID."""
        with self._lock:
            job = self.job_map.pop(job_id, None)
            if job:
                self._schedule.remove(job)
                heapq.heapify(self._schedule)
                if self.schedule_file:
                    self.save_schedule()
            return job

    def _run(self):
        """The main loop of the scheduler."""
        while self._running:
            with self._lock:
                if not self._schedule:
                    time_to_sleep = 1
                else:
                    now = pendulum.now()
                    next_job = self._schedule[0]
                    
                    if now >= next_job.next_run:
                        job_to_run = heapq.heappop(self._schedule)
                        
                        # Run the job
                        if asyncio.iscoroutinefunction(job_to_run.func):
                            asyncio.run(job_to_run.func(*job_to_run.args, **job_to_run.kwargs))
                        else:
                            job_to_run.func(*job_to_run.args, **job_to_run.kwargs)

                        # Reschedule if it's a recurring job (cron string)
                        if isinstance(job_to_run.schedule, str) and croniter.is_valid(job_to_run.schedule):
                            job_to_run._calculate_next_run(base_time=now)
                            self.add_job(job_to_run)
                        else:
                            # One-off job, remove from map
                            self.job_map.pop(job_to_run.id, None)
                        
                        continue # Check for next job immediately

                    time_to_sleep = (next_job.next_run - now).total_seconds()

            time.sleep(max(0, time_to_sleep))

    def start(self):
        """Starts the scheduler."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stops the scheduler."""
        if not self._running:
            return
        self._running = False
        if self._thread:
            self._thread.join()

    def save_schedule(self):
        """Saves the schedule to a file."""
        if not self.schedule_file:
            return
        with self._lock:
            with open(self.schedule_file, "wb") as f:
                f.write(orjson.dumps([job.to_dict() for job in self.job_map.values()]))

    def load_schedule(self):
        """Loads the schedule from a file."""
        if not self.schedule_file:
            return
        try:
            with open(self.schedule_file, "rb") as f:
                jobs_data = orjson.loads(f.read())
                for job_data in jobs_data:
                    job = ScheduledJob.from_dict(job_data)
                    self.add_job(job)
        except FileNotFoundError:
            pass