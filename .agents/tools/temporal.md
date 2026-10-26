# Temporal

## Access

- Interface: Temporal Python SDK in the API and worker; MCP Jungle temporal-cloud for authorized diagnostics.
- Authentication: namespace-scoped API key and TLS.
- Credential source: `TEMPORAL_API_KEY` shared variable in Railway; never store key values here.

## Common tasks

### Resolve the production namespace

Read `.agents/infra/production/temporal.md`. Restrict workflow queries to this
application's report IDs and the task queue `reports-v1`.

### Synthetic deployment check

Use start_workflow with ReportWorkflow, reports-v1 and a fresh report UUID.
The single input object has report_id, values and delay_seconds. Check only that
workflow with get_workflow_result; verify the matching reports row through Neon.
This checks the worker/database path and does not replace the API HTTP smoke test.

## Pitfalls

- Never start the worker rollout before the API pre-deploy has completed.

## References

- https://docs.temporal.io/cloud
