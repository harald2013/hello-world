# World4You

How this repository uses World4You, in every environment. Maintained by
agents under the `tool-context` rule from the development MCP server. Record
only working, current usage. Never store secrets; name only where they come
from. Identifiers and structure per environment live in `.agents/infra/`.

## Access

- Interface: World4You web interface; agents have no API or MCP access
- Authentication: the user's World4You login
- Credential source: the user; agents never handle it

## Common tasks

### Route a custom domain to Railway

Read the CNAME target and the ownership TXT record from Railway's custom
domain configuration, ask the user to set both in the zone `ratzberger.net`,
then check ownership, propagation and certificate status in Railway.

## Pitfalls

- Record names in the web interface are relative to the zone, for example
  `api.report-example` for `api.report-example.ratzberger.net`.

## References

- [production/world4you.md](../infra/production/world4you.md)
