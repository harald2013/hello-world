from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from reports.models import ReportJob


@workflow.defn
class ReportWorkflow:
    @workflow.run
    async def run(self, job: ReportJob) -> dict:
        retries = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=30),
            maximum_attempts=10,
        )
        await workflow.execute_activity(
            "begin_report",
            job,
            start_to_close_timeout=timedelta(seconds=20),
            retry_policy=retries,
        )
        await workflow.sleep(timedelta(seconds=job.delay_seconds))
        return await workflow.execute_activity(
            "complete_report",
            job,
            start_to_close_timeout=timedelta(seconds=20),
            retry_policy=retries,
        )
