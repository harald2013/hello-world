# Neon

## Access

- Interface: MCP Jungle server `neon`.
- Authentication: managed by MCP Jungle.
- Credential source: server configuration; application connection string is a Railway secret.

## Common tasks

### Inspect production

Use list_projects and list_postgres_endpoints with IDs from `.agents/infra/production/neon.md`.

### Transfer the connection string

Call get_connection_string and pass the result directly to Railway variables without printing it. Require sslmode=verify-full and the container CA bundle.

## Pitfalls

- Free accounts reject explicitly setting suspend_timeout_seconds during project creation (HTTP 412). Omit the setting and read the actual endpoint configuration.
- Keep initial compute fixed at 0.25 CU and watch the Free compute allowance.

## References

- https://neon.com/docs/connect/connect-from-any-app
