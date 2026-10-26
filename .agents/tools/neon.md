# Neon

## Access

- Interface: MCP Jungle server `neon`.
- Authentication: managed by MCP Jungle.
- Credential source: server configuration; application connection string is a Railway secret.

## Common tasks

### Inspect production

Use `describe_project` and `list_postgres_endpoints` with IDs from
`.agents/infra/production/neon.md`.

### Transfer the connection string

Call `get_connection_string` and pass the result directly to Railway variables
without printing it. Require `sslmode=verify-full` and the container CA bundle.
Use the direct host of the endpoint for the application, migrations and backups.

## Pitfalls

- Keep compute fixed at 0.25 CU and watch the Free compute allowance; automatic
  suspend is not configured (`suspend_timeout_seconds=0`).

## References

- https://neon.com/docs/connect/connect-from-any-app
