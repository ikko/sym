import pytest
import anyio
from core.schedule import Scheduler, ScheduledJob
import datetime
import time
import logging

async def async_test_job(results_list):
    await anyio.sleep(0.01)
    results_list.append("async_job_executed")

def sync_test_job(results_list):
    results_list.append("sync_job_executed")

@pytest.fixture
async def scheduler():
    s = Scheduler()
    async with anyio.create_task_group() as tg:
        await s.start(tg)
        yield s
        await s.stop()



@pytest.mark.anyio
async def test_sync_job_scheduling(scheduler, caplog):
    caplog.set_level(logging.DEBUG)
    results = []
    future_time = datetime.datetime.now() + datetime.timedelta(seconds=0.1)
    job = ScheduledJob(sync_test_job, (results,), {}, future_time)
    scheduler.add_job(job)

    await anyio.sleep(0.2)

    # Wait for the job to be executed
    timeout = 1.0  # seconds
    start_time = time.time()
    while "sync_job_executed" not in results and time.time() - start_time < timeout:
        await anyio.sleep(0.01)

    assert "sync_job_executed" in results
    assert f"ScheduledJob {job.id} initialized." in caplog.text
    assert f"Executing job: {job.id}" in caplog.text
    assert f"One-off job {job.id} executed and removed." in caplog.text

@pytest.mark.anyio
async def test_recurring_async_job(scheduler, caplog):
    caplog.set_level(logging.DEBUG)
    results = []
    job = ScheduledJob(async_test_job, (results,), {}, "* * * * * *")
    scheduler.add_job(job)

    await anyio.sleep(2.5)

    # Wait for at least 2 executions
    timeout = 5.0  # seconds
    start_time = time.time()
    while len(results) < 2 and time.time() - start_time < timeout:
        await anyio.sleep(0.01)

    scheduler.remove_job(job.id)

    assert len(results) >= 2
    assert all(res == "async_job_executed" for res in results)
    assert f"ScheduledJob {job.id} initialized." in caplog.text
    assert f"Executing job: {job.id}" in caplog.text
    assert f"Job {job.id} rescheduled for: {job.next_run}" in caplog.text
