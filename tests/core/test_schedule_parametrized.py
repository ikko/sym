import pytest
import anyio
import datetime
import time
from symbol.core.schedule import Scheduler, ScheduledJob

# --- Test Functions ---

async def async_job(results, job_id):
    results.append(f"async_{job_id}_started")
    await anyio.sleep(0.1)
    results.append(f"async_{job_id}_finished")

def sync_job(results, job_id):
    results.append(f"sync_{job_id}_started")
    time.sleep(0.1)
    results.append(f"sync_{job_id}_finished")

# --- Fixtures ---

@pytest.fixture
async def scheduler():
    s = Scheduler()
    async with anyio.create_task_group() as tg:
        await s.start(tg)
        yield s
        await s.stop()

# --- Parametrized Tests ---

@pytest.mark.anyio
@pytest.mark.parametrize(
    "job_func, job_type",
    [(sync_job, "sync"), (async_job, "async")]
)
async def test_single_job_execution(scheduler, job_func, job_type):
    results = []
    now = datetime.datetime.now()
    schedule_time = now + datetime.timedelta(seconds=0.1)

    job = ScheduledJob(job_func, (results, "single"), {}, schedule_time)
    scheduler.add_job(job)

    await anyio.sleep(0.3)

    # Wait for the job to be executed
    timeout = 1.0  # seconds
    start_time = time.time()
    while f"{job_type}_single_finished" not in results and time.time() - start_time < timeout:
        await anyio.sleep(0.01)

    assert f"{job_type}_single_started" in results
    assert f"{job_type}_single_finished" in results

@pytest.mark.anyio
@pytest.mark.parametrize(
    "job_func, job_type",
    [(sync_job, "sync"), (async_job, "async")]
)
async def test_batch_job_execution(scheduler, job_func, job_type):
    results = []
    now = datetime.datetime.now()
    schedule_time1 = now + datetime.timedelta(seconds=0.1)
    schedule_time2 = now + datetime.timedelta(seconds=0.15)

    job1 = ScheduledJob(job_func, (results, "batch1"), {}, schedule_time1)
    job2 = ScheduledJob(job_func, (results, "batch2"), {}, schedule_time2)
    
    scheduler.add_jobs([job1, job2])

    await anyio.sleep(0.4)

    # Wait for the jobs to be executed
    timeout = 1.0  # seconds
    start_time = time.time()
    while (f"{job_type}_batch1_finished" not in results or f"{job_type}_batch2_finished" not in results) and time.time() - start_time < timeout:
        await anyio.sleep(0.01)

    assert f"{job_type}_batch1_started" in results
    assert f"{job_type}_batch1_finished" in results
    assert f"{job_type}_batch2_started" in results
    assert f"{job_type}_batch2_finished" in results

@pytest.mark.anyio
async def test_recurring_job(scheduler):
    results = []
    # Schedule to run every second
    job = ScheduledJob(sync_job, (results, "recurring"), {}, "* * * * * *", new_thread=False) # every second
    scheduler.add_job(job)

    await anyio.sleep(2.5)

    assert results.count("sync_recurring_started") >= 2
    assert results.count("sync_recurring_finished") >= 2
