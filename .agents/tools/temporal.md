# Temporal

## Access

- Interface: Temporal Python SDK in the API and worker; MCP Jungle temporal-cloud for authorized diagnostics.
- Authentication: namespace-scoped API key and TLS.
- Credential source: TEMPORAL_API_KEY in Railway; never store key values here.

## Common tasks

### Resolve the production namespace

Read `.agents/infra/production/temporal.md`. Always restrict workflow queries to
this application's report IDs and task queue.

## Pitfalls

- A connected MCP workflow tool does not provide namespace or billing administration.
- Never start the worker rollout before the API pre-deploy has completed.

## References

- https://docs.temporal.io/cloud
