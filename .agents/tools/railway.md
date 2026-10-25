# Railway

## Access

- Interface: MCP Jungle server `railway`.
- Authentication: managed by MCP Jungle.
- Credential source: MCP server configuration; application secrets belong in Railway variables.

## Common tasks

### Inspect production

Read `.agents/infra/production/railway.md`; use `describe_environment` with explicit project and environment IDs.

### Prepare an image service

Create an empty service, configure it and its variables, then attach the tested image. Stage worker image changes until API migration and readiness succeed.

## Pitfalls

- `accept_deploy` commits the entire environment patch: inspect it first.
- Never print `list_variables` values; sealed variables must not be recreated.
- Image registry credentials cannot be supplied through this MCP; set them in the dashboard if needed.

### Verify a scheduled image job

A successful cron deployment only proves the schedule was registered. Verify
execution logs separately. For a one-off check, stage cronSchedule=null and the
normal image start command, inspect the patch and accept it; restore the twelve-
hour schedule after the check. Do not treat a redeploy without execution logs as
a completed backup.

## References

- https://docs.railway.com/deployments/healthchecks
