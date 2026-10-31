# Neon

## Access

- Interface: MCP Jungle server `neon`.
- Authentication: managed by MCP Jungle.
- Credential source: server configuration; application connection string is a Railway secret.

## Common tasks

### Inspect production

Use `describe_project` and `list_postgres_endpoints` with IDs from
`.agents/infra/production/neon.md`.

### Check suspend and compute usage

Read `suspend_timeout_seconds`, `last_active` and `suspended_at` with
`get_postgres_endpoint`. `list_operations` shows each `start_compute` and
`suspend_compute`, which gives the real active cycles. `describe_project`
returns `active_time_seconds`, `compute_time_seconds` (CU-seconds) and
`consumption_period_start`/`_end` of the running month; Neon marks these values
as approximate.

### Transfer the connection string

Call `get_connection_string` and pass the result directly to Railway variables
without printing it. Require `sslmode=verify-full` and the container CA bundle.
Use the direct host of the endpoint for the application, migrations and backups.

## Pitfalls

- `suspend_timeout_seconds=0` means the default of 300 s, not disabled; `-1`
  disables suspend. Free always suspends after 5 minutes and cannot change it.
- Keep compute fixed at 0.25 CU. Every database query keeps the compute active
  for 5 more minutes, so point frequent external monitors at `/health`, not
  `/ready`; an always-active endpoint exceeds the Free compute allowance.

## References

- https://neon.com/docs/connect/connect-from-any-app
- https://neon.com/docs/introduction/plans#scale-to-zero
