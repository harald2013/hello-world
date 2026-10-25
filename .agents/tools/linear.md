# Linear

How this repository uses Linear, in every environment. Maintained by agents
under the `tool-context` rule from the development MCP server. Record only
working, current usage. Never store secrets; name only where they come from.
Identifiers and structure per environment live in `.agents/infra/`.

## Access

- Interface: Linear MCP, server `linear`, through MCP Jungle with tools named
  `linear__…`
- Authentication: configured in MCP Jungle
- Credential source: MCP Jungle configuration

## Common tasks

### Read a ticket

`get_issue(id="TIL-<number>")`.

### Start the branch for a ticket

The branch is `feature/til-<number>-<short-feature-name>`; create it with
`python3 -B scripts/git_start.py <repository> TIL-<number> <short-feature-name>`.
Do not use Linear's `gitBranchName`, which follows another pattern.

### Find team and project IDs

Read [shared/linear.md](../infra/shared/linear.md) instead of listing teams
or projects.

## Pitfalls

- `git_start.py` keeps the case of the ticket argument; pass `til-<number>`
  or rename the branch to lowercase.

## References

- [AGENTS.md](../../AGENTS.md#workflow)
