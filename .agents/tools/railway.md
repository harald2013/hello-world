# Railway

## Access

- Interface: MCP Jungle server `railway`.
- Authentication: managed by MCP Jungle.
- Credential source: MCP server configuration; application secrets belong in Railway variables.

## Common tasks

### Inspect production

Read `.agents/infra/production/railway.md`; use `describe-environment` with
explicit project and environment IDs. It lists services, image sources,
regions, replicas, cron schedules and shared variable names without values.

### Prepare an image service

Create an empty service, configure it and its variables, then attach the tested
image. Stage worker image changes until API migration and readiness succeed.

### Run the backup job once

Stage `cronSchedule=null` with the normal image start command, inspect the
patch and accept it; check the execution logs, then restore the twelve-hour
schedule. Switching between cron and one-off operation needs a fresh staged
configuration commit; redeploying an older cron build alone did not run the job.

## Pitfalls

- Tool-wide pitfalls are served by `get_agent_rules(["railway"])`.

## References

- https://docs.railway.com/deployments/healthchecks
