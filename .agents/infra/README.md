# Infrastructure

Entry point to the infrastructure of this repository. Maintained by agents
under the `tool-context` rule from the development MCP server. Usage per tool
is in `.agents/tools/<tool>.md`; artifacts per environment are in
`.agents/infra/<env>/<tool>.md` and, for artifacts identical in every
environment, in `.agents/infra/shared/<tool>.md`. Never store secrets.

## Environments

| Environment | Purpose | Branch |
| --- | --- | --- |
| local | Synthetic-data stack from `compose.yml`; never deployed | feature branch |
| staging | Individual images on wh-coolify with synthetic data | image tags `sha-<commit>` from `main` or `feature/**` |
| production | Railway, Neon, Temporal Cloud and Cloudflare R2 | main |

## System

Every component of the system and the artifact that runs it per environment.
`local` names the Compose service; there is no local inventory.

| Component | Purpose | Source | local | staging | production |
| --- | --- | --- | --- | --- | --- |
| api | Authenticated HTTP API that stores reports and starts their workflows; also serves the static browser UI under `/ui/` | Image: `ghcr.io/harald2013/report-example-api` | compose `api` | coolify `api` | railway `api` |
| migration | One-off schema migration from the API image before the API starts | Image: `ghcr.io/harald2013/report-example-api` | compose `migrate` | one-off coolify task in the `api` container | railway `api` (pre-deploy) |
| worker | Temporal worker that computes reports and writes results | Image: `ghcr.io/harald2013/report-example-worker` | compose `worker` | coolify `worker` | railway `worker` |
| backup | Scheduled job that dumps the database to object storage and prunes old dumps | Image: `ghcr.io/harald2013/report-example-backup` | – | – | railway `backup` → cloudflare `report-example/production/` |
| database | PostgreSQL for reports | Image: `postgres` / Managed: neon | compose `postgres` | coolify `postgres` | neon `reports` |
| workflow engine | Temporal server and namespace for report workflows | Image: `temporalio/auto-setup` / Managed: temporal | compose `temporal` | coolify `temporal` | temporal `default-namespace.rq4it` |
| workflow UI | Temporal web UI | Image: `temporalio/ui` / Managed: temporal | compose `temporal-ui` | coolify `temporal-ui` | temporal Cloud UI |
| DNS | Routes the public API domain to the platform | Managed: world4you | – | – | world4you `api.report-example` |

## Tools per environment

| Environment | Tool | Instance or account | MCP server | Inventory |
| --- | --- | --- | --- | --- |
| production | railway | Default Workspace, Hobby | `railway` | [production/railway.md](production/railway.md) |
| production | neon | DefaultOrga, Free | `neon` | [production/neon.md](production/neon.md) |
| production | temporal | Temporal Cloud | `temporal-cloud` | [production/temporal.md](production/temporal.md) |
| production | cloudflare | Cloudflare account, R2 EU | none; S3 | [production/cloudflare.md](production/cloudflare.md) |
| production | world4you | Customer account, zone ratzberger.net | none; web interface | [production/world4you.md](production/world4you.md) |
| staging | coolify | Instance wh-coolify, server localhost, destination localhost-report-example-staging | `coolify-wh-coolify` | [staging/coolify.md](staging/coolify.md) |
| shared | github | Account harald2013 | none, `gh` CLI | [shared/github.md](shared/github.md) |
| shared | linear | Workspace tilia-at, team Tilia | `linear` | [shared/linear.md](shared/linear.md) |

## Connections

### staging

- All staging applications use the Coolify destination
  `localhost-report-example-staging` (Docker network `report-example-staging`)
  on wh-coolify and reach each other through their network aliases. They share
  no network with the IDP resources on the same server
  ([staging/coolify.md](staging/coolify.md#destinations)).
- The workflow `Report example · Container images` publishes
  `ghcr.io/harald2013/report-example-api` and
  `ghcr.io/harald2013/report-example-worker`; the Coolify applications `api` and
  `worker` run these image repositories.
- API https://wh-coolify.tail8fba42.ts.net:15100/ and Temporal UI
  https://wh-coolify.tail8fba42.ts.net:15101/ are tailnet-only through
  Tailscale Serve to fixed container addresses.
- The bearer token is the shared variable `API_TOKEN` of the Coolify
  environment `staging`; use it inside the API container instead of reading it.

### shared

- Linear tickets `TIL-<number>` map to branches `feature/til-<number>-<name>`
  and PRs against `main`.

### production

- The image workflow also publishes `ghcr.io/harald2013/report-example-backup`
  for the Railway scheduled backup service. API and worker use the same image
  repositories as staging; tested digests are promoted without rebuilding.
- Railway API and worker use Neon `reports` and Temporal Cloud namespace
  `default-namespace.rq4it`.
- Railway backup job writes only to Cloudflare R2 prefix
  `report-example/production/`.
- World4You DNS routes `api.report-example.ratzberger.net` to the Railway
  custom domain of the service `api`.

## Deployment documentation

Procedures and dated acceptance evidence live outside `.agents/` and are only
linked here; they are not live platform state.

- [Operations](../../deploy/operations.md): release and rollback
- [Staging](../../deploy/staging.md): Coolify setup
- [Production](../../deploy/production.md): Railway, Neon, Temporal Cloud and R2 setup
- [Staging acceptance](../../deploy/staging-acceptance.md) and
  [production setup](../../deploy/production-setup.md): dated evidence
- [UI rollout](../../deploy/ui-acceptance.md): dated evidence for the browser UI
  in staging and production
- [Rename to report-example](../../deploy/rename-acceptance.md): dated evidence
  for the switch to the renamed image repositories
