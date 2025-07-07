import pytest
import anyio
from symbol.core.schedule import Scheduler, ScheduledJob
import datetime
import time
import logging

async def async_test_job(result_list):
    await anyio.sleep(0.01)
    result_list.append("async_job_executed")

def sync_test_job(result_list):
    result_list.append("sync_job_executed")

@pytest.fixture
async def scheduler():
    s = Scheduler()
    async with anyio.create_task_group() as tg:
        await s.start(tg)
        yield s
        await s.stop()



@pytest.mark.skip(reason="Temporarily skipping recurring job test")
@pytest.mark.anyio
async def test_sync_job_scheduling(scheduler, caplog):
    caplog.set_level(logging.DEBUG)
    results = []
    future_time = datetime.datetime.now() + datetime.timedelta(seconds=0.1)
    job = ScheduledJob(sync_test_job, (results,), {}, future_time)
    scheduler.add_job(job)

    await anyio.sleep(0.2)

    assert "sync_job_executed" in results
    assert f"ScheduledJob {job.id} initialized. Next run: {job.next_run}" in caplog.text
    assert f"Executing job: {job.id}" in caplog.text
    assert f"One-off job {job.id} executed and removed." in caplog.text

@pytest.mark.skip(reason="Temporarily skipping recurring job test")
@pytest.mark.anyio
async def test_recurring_async_job(scheduler, caplog):
    caplog.set_level(logging.DEBUG)
    results = []
    job = ScheduledJob(async_test_job, (results,), {}, "* * * * *")
    scheduler.add_job(job)

    await anyio.sleep(2.5)

    scheduler.remove_job(job.id)

    assert len(results) >= 2
    assert all(res == "async_job_executed" for res in results)
    assert f"ScheduledJob {job.id} initialized. Next run: {job.next_run}" in caplog.text
    assert f"Executing job: {job.id}" in caplog.text
    assert f"Job {job.id} rescheduled for: {job.next_run}" in caplog.text
