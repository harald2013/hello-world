# Infrastructure

Entry point to the infrastructure of this repository. Maintained by agents
under the `tool-context` rule from the development MCP server. Usage per tool
is in `.agents/tools/<tool>.md`; artifacts per environment are in
`.agents/infra/<env>/<tool>.md` and, for artifacts identical in every
environment, in `.agents/infra/shared/<tool>.md`. Never store secrets.

## Environments

| Environment | Purpose | Branch |
| --- | --- | --- |
| local | Synthetic-data stack from `compose.yml`; never deployed to Coolify | feature branch |
| staging | Individual images on workhorse with synthetic data ([staging](../../deploy/staging.md)) | image tags `sha-<commit>` from `main` or `feature/**` |
| production | Render, Temporal Cloud and Neon ([production](../../deploy/production.md)); not provisioned yet | main |

## Tools per environment

| Environment | Tool | Instance or account | MCP server | Inventory |
| --- | --- | --- | --- | --- |
| staging | coolify | Instance workhorse, server localhost | `coolify-workhorse` | [staging/coolify.md](staging/coolify.md) |
| shared | github | Account harald2013 | none, `gh` CLI | [shared/github.md](shared/github.md) |
| shared | linear | Workspace tilia-at, team Tilia | `linear` | [shared/linear.md](shared/linear.md) |

Production resources on Render, Temporal Cloud and Neon do not exist yet.
Create `production/<tool>.md` when they are provisioned.

## Connections

### staging

- The workflow `Report example · Container images` publishes
  `ghcr.io/harald2013/hello-world-api` and
  `ghcr.io/harald2013/hello-world-worker`; the Coolify applications `api` and
  `worker` run these image repositories.
- API https://workhorse.tail8fba42.ts.net:18443/ and Temporal UI
  https://workhorse.tail8fba42.ts.net:18444/ are tailnet-only through
  Tailscale Serve.
- The bearer token is the runtime secret `API_TOKEN` of the Coolify
  application `api`; read it there only when needed.

### shared

- Linear tickets `TIL-<number>` map to branches `feature/til-<number>-<name>`
  and PRs against `main`.
