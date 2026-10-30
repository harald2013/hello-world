# Coolify

How this repository uses Coolify, in every environment. Maintained by agents
under the `tool-context` rule from the development MCP server. Record only
working, current usage. Never store secrets; name only where they come from.
Identifiers and structure per environment live in `.agents/infra/`.

## Access

- Interface: Coolify MCP through MCP Jungle, server `coolify-wh-coolify`; the
  Coolify UI for fields the MCP does not send
- Authentication: Coolify API token
- Credential source: MCP Jungle configuration
- Host steps on wh-coolify (Docker networks, Tailscale Serve) are done by the
  user; agents have no SSH access there

## Common tasks

### Resolve UUIDs

Read [staging/coolify.md](../infra/staging/coolify.md) instead of listing
projects or applications.

### Check all staging applications at once

`environments(action="get", project_uuid="mxu2fn0yhgpp6xfooibg56ru", name="staging")`
returns every application with image, network alias and Docker options.

### Update an image version

Read the application live with `get_application(uuid=<uuid>)`, change only
the image tag, deploy, and verify the result in Coolify. Version-only changes
do not touch the inventory.

### Run a command in the API container

`scheduled_tasks(action="run_once", resource="application", uuid=<api>,
container="api", command=...)` runs a one-off command and returns its stdout.
Use it for the schema job (`python -m reports.store`) and for authenticated
checks that read `API_TOKEN` from the container environment, so the token
never reaches stdout. Commands are limited to 255 characters and may run more
than once; keep them idempotent.

### Check staging without the API token

Read `/ready` and `/ui/` over the tailnet HTTPS URL. An unauthenticated
`POST /reports` must return 401.

## Pitfalls

- `create_dockerimage` assigns a public sslip.io domain; clear it with
  `update(domains="")` right after creation.
- `env_vars` `bulk_update` returns resolved values of shared-variable
  references; create variables one by one with `create`, which returns only
  the UUID.
- The MCP drops `health_check_type`, `health_check_command` and
  `is_consistent_container_name_enabled`; set them in the Coolify UI and read
  them back with `get_application`.
- The Coolify API rejects IP-prefixed `ports_mappings`; publish no host ports
  and use the fixed container addresses from the inventory.
- Stop PostgreSQL before replacing it; never run two PostgreSQL containers
  against the same volume.
- Never publish ports on all host interfaces, not even temporarily.
- `compose.yml` is for local use only; staging uses individual image
  applications.

## References

- [Staging](../../deploy/staging.md)
- [ADR 0005](../../docs/adr/0005-stateful-staging-updates.md)
- [ADR 0008](../../docs/adr/0008-staging-on-wh-coolify.md)
