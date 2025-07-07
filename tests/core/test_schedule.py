import pytest
import datetime
import time
import logging
import os
import anyio

from symbol.core.schedule import Scheduler, ScheduledJob
from symbol.core.base_symbol import Symbol

# --- Helper functions for testing jobs ---

async def async_test_job(result_list):
    await anyio.sleep(0.01) # Simulate async work
    result_list.append("async_job_executed")

def sync_test_job(result_list):
    result_list.append("sync_job_executed")

# --- Fixtures ---

@pytest.fixture
def scheduler_instance():
    s = Scheduler()
    yield s
    s.stop()

@pytest.fixture
def temp_schedule_file(tmp_path):
    return tmp_path / "test_schedule.json"

@pytest.fixture
def file_scheduler(temp_schedule_file):
    s = Scheduler(schedule_file=str(temp_schedule_file))
    yield s
    s.stop()
    if os.path.exists(temp_schedule_file):
        os.remove(temp_schedule_file)

# --- ScheduledJob Tests ---

def test_scheduled_job_init_datetime():
    now = datetime.datetime.now()
    job = ScheduledJob(sync_test_job, (), {}, now)
    assert job.next_run == now
    assert job.id is not None

def test_scheduled_job_init_date():
    today = datetime.date.today()
    job = ScheduledJob(sync_test_job, (), {}, today)
    assert job.next_run == datetime.datetime.combine(today, datetime.time.min)

def test_scheduled_job_init_time():
    test_time = datetime.time(10, 30, 0)
    job = ScheduledJob(sync_test_job, (), {}, test_time)
    expected_datetime = datetime.datetime.combine(datetime.date.today(), test_time)
    if expected_datetime < datetime.datetime.now():
        expected_datetime += datetime.timedelta(days=1)
    assert job.next_run == expected_datetime

def test_scheduled_job_init_cron_string():
    job = ScheduledJob(sync_test_job, (), {}, "* * * * *")
    assert job.next_run is not None
    # Basic check: next_run should be in the future
    assert job.next_run > datetime.datetime.now()

def test_scheduled_job_init_iso_string():
    iso_str = "2025-12-25T10:00:00"
    job = ScheduledJob(sync_test_job, (), {}, iso_str)
    assert job.next_run == datetime.datetime.fromisoformat(iso_str)

def test_scheduled_job_init_symbol():
    sym = Symbol("2025-01-01T00:00:00")
    job = ScheduledJob(sync_test_job, (), {}, sym)
    assert job.next_run == datetime.datetime(2025, 1, 1, 0, 0, 0)

def test_scheduled_job_init_unsupported_type():
    with pytest.raises(TypeError, match="Unsupported schedule type"):
        ScheduledJob(sync_test_job, (), {}, 123)

def test_scheduled_job_calculate_next_run_past_datetime():
    past_time = datetime.datetime.now() - datetime.timedelta(days=1)
    job = ScheduledJob(sync_test_job, (), {}, past_time)
    assert job.next_run is None

def test_scheduled_job_lt():
    now = datetime.datetime.now()
    job1 = ScheduledJob(sync_test_job, (), {}, now + datetime.timedelta(seconds=10))
    job2 = ScheduledJob(sync_test_job, (), {}, now + datetime.timedelta(seconds=5))
    job3 = ScheduledJob(sync_test_job, (), {}, now + datetime.timedelta(seconds=15))

    assert job2 < job1
    assert job1 < job3
    assert not (job1 < job2)

def test_scheduled_job_to_from_dict():
    now = datetime.datetime.now().replace(microsecond=0) # Remove microseconds for exact comparison
    job = ScheduledJob(sync_test_job, (1, "test"), {"key": "value"}, now, new_process=True, id="test_id")
    job_dict = job.to_dict()
    
    # Manually adjust func string for comparison as it includes module path
    job_dict["func"] = "tests.core.test_schedule.sync_test_job"

    recreated_job = ScheduledJob.from_dict(job_dict)

    assert recreated_job.id == job.id
    assert recreated_job.func.__name__ == job.func.__name__
    assert recreated_job.args == job.args
    assert recreated_job.kwargs == job.kwargs
    # For datetime, direct comparison might fail due to microsecond differences or timezone issues
    # Compare ISO format strings for robustness
    assert recreated_job.next_run.isoformat() == job.next_run.isoformat()
    assert recreated_job.new_process == job.new_process
    assert recreated_job.new_thread == job.new_thread

# --- Scheduler Tests ---

@pytest.mark.anyio
async def test_scheduler_add_remove_job(scheduler_instance):
    results = []
    job = ScheduledJob(sync_test_job, (results,), {}, datetime.datetime.now() + datetime.timedelta(seconds=0.1))
    scheduler_instance.add_job(job)
    assert job.id in scheduler_instance.job_map
    assert len(scheduler_instance._schedule) == 1

    removed_job = scheduler_instance.remove_job(job.id)
    assert removed_job.id == job.id
    assert job.id not in scheduler_instance.job_map
    assert len(scheduler_instance._schedule) == 0

@pytest.mark.anyio
async def test_scheduler_run_one_off_sync_job(scheduler_instance, caplog):
    caplog.set_level(logging.DEBUG)
    results = []
    future_time = datetime.datetime.now() + datetime.timedelta(seconds=0.1)
    job = ScheduledJob(sync_test_job, (results,), {}, future_time)
    scheduler_instance.add_job(job)

    scheduler_instance.start()
    await anyio.sleep(0.5) # Give scheduler time to run
    scheduler_instance.stop()

    assert "sync_job_executed" in results
    assert f"One-off job {job.id} executed and removed." in caplog.text

@pytest.mark.anyio
async def test_scheduler_run_one_off_async_job(scheduler_instance, caplog):
    caplog.set_level(logging.DEBUG)
    results = []
    future_time = datetime.datetime.now() + datetime.timedelta(seconds=0.1)
    job = ScheduledJob(async_test_job, (results,), {}, future_time)
    scheduler_instance.add_job(job)

    scheduler_instance.start()
    await anyio.sleep(0.5) # Give scheduler time to run
    scheduler_instance.stop()

    assert "async_job_executed" in results
    assert f"One-off job {job.id} executed and removed." in caplog.text

@pytest.mark.anyio
async def test_scheduler_recurring_job(scheduler_instance, caplog):
    caplog.set_level(logging.DEBUG)
    results = []
    # Schedule to run every second
    job = ScheduledJob(sync_test_job, (results,), {}, "* * * * *")
    scheduler_instance.add_job(job)

    scheduler_instance.start()
    await anyio.sleep(3.0) # Let it run for a few seconds
    scheduler_instance.stop()

    assert len(results) >= 2 # Should have run at least twice
    assert all(res == "sync_job_executed" for res in results)
    assert f"Job {job.id} rescheduled for:" in caplog.text

@pytest.mark.anyio
async def test_scheduler_empty_schedule_sleep(scheduler_instance, caplog):
    caplog.set_level(logging.DEBUG)
    scheduler_instance.start()
    await anyio.sleep(1.5) # Let it sleep for empty schedule
    scheduler_instance.stop()
    assert "Schedule is empty. Sleeping for 1 second." in caplog.text

def test_scheduler_save_load_schedule(file_scheduler, temp_schedule_file):
    results1 = []
    job1 = ScheduledJob(sync_test_job, (results1,), {}, datetime.datetime.now() + datetime.timedelta(seconds=10), id="job1")
    file_scheduler.add_job(job1)

    results2 = []
    job2 = ScheduledJob(async_test_job, (results2,), {}, "* * * * *", id="job2")
    file_scheduler.add_job(job2)

    file_scheduler.save_schedule()
    file_scheduler.stop()

    # Create a new scheduler instance and load the schedule
    new_scheduler = Scheduler(schedule_file=str(temp_schedule_file))
    new_scheduler.load_schedule()
    new_scheduler.start()

    assert "job1" in new_scheduler.job_map
    assert "job2" in new_scheduler.job_map
    assert new_scheduler.job_map["job1"].next_run.isoformat() == job1.next_run.isoformat()
    # For cron jobs, next_run will be recalculated, so just check if it's not None
    assert new_scheduler.job_map["job2"].next_run is not None

    new_scheduler.stop()