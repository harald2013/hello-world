# Coolify

Reference for the Coolify instance that hosts the `staging` environment of
this repository.

A UUID is the identifier Coolify uses in its API and MCP tools.

## Instance wh-coolify

URL: http://wh-coolify:8000/

Reach this instance through MCP Jungle under the server name `coolify-wh-coolify`. Its tools are named `coolify-wh-coolify__…`.

The objects below nest. The server runs the applications. The project contains the environment. The environment contains the resources.

```
wh-coolify
└── server localhost
    └── project report-example
        └── environment staging
            ├── postgres
            ├── temporal
            ├── temporal-ui
            ├── api
            └── worker
```

The resources are on the Docker network `report-example-staging` (`ob9mjye7qpm4k1ytlvdwongd`).

### Servers

| Name | UUID | Description |
| --- | --- | --- |
| localhost | kisymismhd6tci7xrbjb1r1y | wh-coolify, reachable at host.docker.internal |

### Projects

| Name | UUID | Description |
| --- | --- | --- |
| report-example | mxu2fn0yhgpp6xfooibg56ru | Portable report example, synthetic staging data |

### Environments

| Name | UUID | Description |
| --- | --- | --- |
| staging | gxgtic2h6zlchftuzyqnodhg | Independent image applications |

### Resources

| Name | UUID | Kind | Deployment | Description |
| --- | --- | --- | --- | --- |
| postgres | 1gvjtntleypij9lvcfdid5yk | application | Image: `postgres` | Staging postgres; network alias `report-postgres`; not exposed |
| temporal | uf0runx9tuaasz0boge5mpb2 | application | Image: `temporalio/auto-setup` | Staging temporal; network alias `report-temporal`; not exposed |
| temporal-ui | ggb4ntoezlha1g7arkrkvmvy | application | Image: `temporalio/ui` | Temporal UI; network alias `report-temporal-ui`; https://wh-coolify.tail8fba42.ts.net:15101/ (tailnet only) |
| api | mtyncf8p2yaqsnjyg72adga6 | application | Image: `ghcr.io/harald2013/report-example-api` | Staging API; network alias `report-api`; https://wh-coolify.tail8fba42.ts.net:15100/ (tailnet only) |
| worker | ekvdn0bmgy3bilxcnvgamcvt | application | Image: `ghcr.io/harald2013/report-example-worker` | Staging worker; network alias `report-worker`; not exposed |

## Project additions

The network `report-example-staging` has the fixed subnet `172.30.0.0/24`.
No application publishes a host port. Tailscale Serve on wh-coolify forwards
to fixed container addresses, set as `--ip` in the custom Docker options:

| Resource | Address | Tailnet port |
| --- | --- | --- |
| api | 172.30.0.13:8000 | 15100 |
| temporal-ui | 172.30.0.12:8080 | 15101 |

The tailnet ports use the block 15100–15119.

PostgreSQL uses the persistent volume
`1gvjtntleypij9lvcfdid5yk-report-example-postgres-data` (storage UUID
`cgccmjqd5a0ebmcpw3fdrhnx`) at `/var/lib/postgresql/data`. PostgreSQL uses
consistent container naming and must stop before replacement.

### Configuration

Shared variables of the environment `staging`; each application variable
references them through Coolify's `environment.<NAME>` reference in double
braces.

| Name | Scope | Secret | Source |
| --- | --- | --- | --- |
| APP_ENV | shared | no | Coolify shared variable |
| TEMPORAL_ADDRESS | shared | no | Coolify shared variable |
| TEMPORAL_NAMESPACE | shared | no | Coolify shared variable |
| TEMPORAL_TASK_QUEUE | shared | no | Coolify shared variable |
| TEMPORAL_TLS | shared | no | Coolify shared variable |
| POSTGRES_PASSWORD | shared | yes | Coolify shared variable; postgres `POSTGRES_PASSWORD`, temporal `POSTGRES_PWD` |
| DATABASE_URL | shared | yes | Coolify shared variable; api, worker |
| API_TOKEN | shared | yes | Coolify shared variable; api, worker |

### Retired instance workhorse

The former staging project `report-example` (`paxi2fhovbegez4lh7gxdgjj`) on
workhorse is stopped, not deleted. Its PostgreSQL volumes
`report-example-postgres-data-v2` and
`fsew7ydowsjgjbbnickyi65b-report-example-postgres-data` are retained. Do not
start these applications; their deletion is a separate decision.
