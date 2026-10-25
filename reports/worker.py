import asyncio
import signal
from datetime import timedelta

from temporalio import activity
from temporalio.worker import Worker

from reports.config import Settings, connect_temporal
from reports.models import ReportJob, summarize
from reports.store import Store
from reports.workflows import ReportWorkflow


class ReportActivities:
    def __init__(self, store: Store):
        self.store = store

    @activity.defn(name="begin_report")
    async def begin(self, job: ReportJob):
        await self.store.begin(job.report_id, job.values)

    @activity.defn(name="complete_report")
    async def complete(self, job: ReportJob) -> dict:
        result = summarize(job.values)
        await self.store.complete(job.report_id, result)
        return result


async def main():
    settings = Settings.from_env()
    store = Store(settings.database_url)
    await store.ready()
    client = await connect_temporal(settings)
    activities = ReportActivities(store)
    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set)
    async with Worker(
        client,
        task_queue=settings.task_queue,
        workflows=[ReportWorkflow],
        activities=[activities.begin, activities.complete],
        graceful_shutdown_timeout=timedelta(seconds=15),
    ):
        await stop.wait()


if __name__ == "__main__":
    asyncio.run(main())
