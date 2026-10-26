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
| production | Railway, Temporal Cloud and Neon ([production](../../deploy/production.md)) | main |

## Tools per environment

| Environment | Tool | Instance or account | MCP server | Inventory |
| --- | --- | --- | --- | --- |
| production | temporal | Temporal Cloud | `temporal-cloud` | [production/temporal.md](production/temporal.md) |
| production | r2 | Cloudflare R2 EU | none; S3 | [production/r2.md](production/r2.md) |
| production | neon | DefaultOrga | `neon` | [production/neon.md](production/neon.md) |
| production | railway | Default Workspace | `railway` | [production/railway.md](production/railway.md) |
| staging | coolify | Instance workhorse, server localhost | `coolify-workhorse` | [staging/coolify.md](staging/coolify.md) |
| shared | github | Account harald2013 | none, `gh` CLI | [shared/github.md](shared/github.md) |
| shared | linear | Workspace tilia-at, team Tilia | `linear` | [shared/linear.md](shared/linear.md) |

Stable resource identifiers are listed in the linked inventories. Deployment
procedures and dated acceptance evidence are kept separately in `deploy/`.
Read [operations](../../deploy/operations.md) for release and rollback steps,
[staging](../../deploy/staging.md) for Coolify, and
[production](../../deploy/production.md) for Railway. The dated evidence is in
[staging acceptance](../../deploy/staging-acceptance.md),
[production setup](../../deploy/production-setup.md); it is not live platform state.

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

### production

- The image workflow also publishes `ghcr.io/harald2013/hello-world-backup`
  for the Railway scheduled backup service. API and worker use the same image
  repositories as staging; tested digests are promoted without rebuilding.
- Railway API and worker use Neon reports and Temporal Cloud namespace default-namespace.rq4it.
- Railway backup job writes only to Cloudflare R2 prefix report-example/production/.
- World4You DNS routes the custom API domain to the Railway service.
