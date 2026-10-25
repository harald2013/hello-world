# Coolify

How this repository uses Coolify, in every environment. Maintained by agents
under the `tool-context` rule from the development MCP server. Record only
working, current usage. Never store secrets; name only where they come from.
Identifiers and structure per environment live in `.agents/infra/`.

## Access

- Interface: Coolify MCP through MCP Jungle, server `coolify-workhorse`, and
  the Coolify API where the MCP lacks a field
- Authentication: Coolify API token
- Credential source: MCP Jungle configuration

## Common tasks

### Resolve UUIDs

Read [staging/coolify.md](../infra/staging/coolify.md) instead of listing
projects or applications.

### Check all staging applications at once

`environments(action="get", project_uuid="paxi2fhovbegez4lh7gxdgjj", name="staging")`
returns every application with image, network alias and port mapping.

### Update an image version

Read the application live with `get_application(uuid=<uuid>)`, change only
the image tag, deploy, and verify the result in Coolify. Version-only changes
do not touch the inventory.

## Pitfalls

- The MCP tool supports neither `ports_mappings` nor command health checks;
  see [staging](../../deploy/staging.md#konfiguration-der-installierten-coolify-version).
- Stop PostgreSQL before replacing it; never run two PostgreSQL containers
  against the same volume.
- Never publish ports on all host interfaces, not even temporarily.
- `compose.yml` is for local use only; staging uses individual image
  applications.

## References

- [Staging](../../deploy/staging.md)
- [ADR 0005](../../docs/adr/0005-stateful-staging-updates.md)
