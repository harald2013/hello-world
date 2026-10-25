import asyncio
import os
from datetime import timedelta
from uuid import uuid4

import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Replayer, Worker

from reports.models import ReportJob
from reports.worker import ReportActivities
from reports.workflows import ReportWorkflow


class MemoryStore:
    def __init__(self):
        self.started = asyncio.Event()
        self.attempts = 0
        self.result = None

    async def begin(self, report_id, values):
        self.attempts += 1
        if self.attempts == 1:
            raise ConnectionError("temporary database failure")
        self.started.set()

    async def complete(self, report_id, result):
        self.result = result


@pytest.mark.asyncio
async def test_retry_timer_worker_restart_and_history_replay():
    async with await WorkflowEnvironment.start_time_skipping(
        test_server_existing_path=os.getenv("TEMPORAL_TEST_SERVER"),
    ) as env:
        store = MemoryStore()
        activities = ReportActivities(store)
        queue = f"test-{uuid4()}"
        worker_options = {
            "task_queue": queue,
            "workflows": [ReportWorkflow],
            "activities": [activities.begin, activities.complete],
            "graceful_shutdown_timeout": timedelta(seconds=5),
            # Force reconstruction from history rather than sticky-cache routing.
            "max_cached_workflows": 0,
        }
        async with Worker(env.client, **worker_options):
            handle = await env.client.start_workflow(
                ReportWorkflow.run,
                ReportJob(str(uuid4()), [10, 20, 30], 5),
                id=f"report-test-{uuid4()}",
                task_queue=queue,
            )
            await asyncio.wait_for(store.started.wait(), timeout=20)
        # A new worker must recover the original execution from server history.
        async with Worker(env.client, **worker_options):
            # Keep this short timer on wall-clock time: automatic time skipping
            # can race with worker replacement on the lightweight test server.
            with env.auto_time_skipping_disabled():
                result = await asyncio.wait_for(handle.result(), timeout=30)
        assert result == {"count": 3, "sum": 60, "min": 10, "max": 30, "mean": 20}
        assert store.result == result
        assert store.attempts >= 2
        await Replayer(workflows=[ReportWorkflow]).replay_workflow(
            await handle.fetch_history()
        )
